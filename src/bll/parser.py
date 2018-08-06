from src.tools import Tools, REGION_MAP
import re


class Parser:
    """
    Класс для парсинга страниц
    """
    def __init__(self, base_url=None):
        self.tools = Tools()
        self.base_url = base_url

    @staticmethod
    def item_filter(item_data):
        """если номера тендера содержит букву возвращаем его """
        regex = re.compile(r'\D')
        number = item_data.find('p', {'itemprop': 'name'}).text.split()[-1]
        clear_number = number.strip()
        return clear_number if regex.match(clear_number) else None

    @staticmethod
    def clear_date_str(date_str):
        if not date_str:
            return None
        try:
            date = re.search(r'\d\d\.\d\d\.\d\d\d\d', date_str).group(0)
        except AttributeError:
            return None

        try:
            time = re.search(r'\d\d:\d\d', date_str).group(0)
        except AttributeError:
            time = ''

        date_time_str = '{} {}'.format(date, time).strip()


        try:
            if 'GMT' not in date_str:
                time_delta = int(re.search(r'\+\d\d', date_str).group(0).replace('\+', '').lstrip('0'))
            else:
                time_delta = int(
                    re.search(
                        r'\+\d+', date_str.replace(date, '').replace(time, '')).group(0).replace('\+', '').lstrip('0'))
        except AttributeError:
            return date_time_str, None
        return date_time_str, time_delta

    @staticmethod
    def clear_double_data_str(data_str):
        if not data_str or data_str == 'Цена не указана' or data_str == 'Не установлен':
            return None
        elif '(сумма блокируется)' in data_str:
            data_str = data_str.replace('(сумма блокируется)', '').strip()
        return float(data_str.split('\n')[0].replace(' ', '').replace(',', '.'))

    def get_part_data(self, data_list):
        """парсим строки пришедшие в запросе возвращаем список первичных данных"""
        item_list = []
        for item_data in data_list:
            item_number = self.item_filter(item_data)
            if item_number:
                #print(item_number)
                item_list.append({
                    'number': item_number,
                    'name': item_data.find('p', {'itemprop': 'description'}).text,
                    'link': self.base_url + item_data.attrs['href'],
                    'sub_close_date': self.clear_date_str(item_data.find(
                        'p', class_='block__related_details_date').text),
                    'type': item_data.find('p', class_='block__related_about_title').text,
                    'price': self.clear_double_data_str(item_data.find(
                        'div', class_='block__related_details_sum').find('span').text),
                })
        return item_list

    @staticmethod
    def find_lot_row(lot_div, block_name, search_str):
        lot_data_containers = lot_div.find_all('div', class_='block__docs_container')
        lot_blocks_map = {
            'Этапы закупочной процедуры': lot_data_containers[0],
            'Цена договора и требования к обеспечению': lot_data_containers[0],
            'Условия договора': lot_data_containers[3],
            'Заказчики, с которыми заключается договор': lot_data_containers[6],
            #'Классификатор ОКПД2': lot_data_containers[7],
            #'Классификатор ОКВЭД2': lot_data_containers[8],
            'Документация лота': lot_data_containers[9],
            #'Перечень товаров, работ, услуг': lot_data_containers[10]
        }
        for row in lot_blocks_map[block_name].find_all('div', class_='block__docs_container_cell'):
            cells = row.find_all('p')
            if cells[0].text.strip() == search_str:
                return ''.join(cells[1].findAll(text=True)).strip()
        return None

    def get_lot_delivery_place(self, lot_div):
        full_string = self.find_lot_row(
            lot_div, 'Условия договора', 'Место поставки товаров/выполнения работ/оказания услуг'
        )
        drop_string = lot_div.find('a', class_='price_nds price_nds--forPrint').text
        return full_string.replace(drop_string, '').strip()

    @staticmethod
    def get_lot_okpd_okved(lot_div, okpd2=False, okved2=False):
        if okpd2:
            data_container = lot_div.find_all('div', class_='block__docs_container')[7]
        elif okved2:
            data_container = lot_div.find_all('div', class_='block__docs_container')[8]
        else:
            return None
        items = data_container.find_all('div', class_='block__docs_container_cell')
        if len(items) == 1 and items[0].findAll(text=True)[0] == 'Отсутствуют':
            return None
        result = []
        for item in items:
            result.append('{} {}'.format(item.find('p').text, item.find('h4').text))
        return result

    @staticmethod
    def get_region_from_address(address):
        address = address.lower()
        for key, item in REGION_MAP.items():
            if address.find(key) != -1:
                return item

    @staticmethod
    def get_lot_positions(lot_div):
        positions_data = lot_div.find(
            'div', class_='block__docs_container block__docs_container_works'
        ).find_all('div', class_='block__docs_container_cell')
        positions = []
        for position in positions_data:
            positions.append({
                'name': position.find('h4').text,
                'quantity': position.find('span', class_='block__docs_container_info_number').text
            })
        return positions

    @staticmethod
    def get_currency_from_docs_container(data_html):
        return data_html.find(
            'div', class_='block__docs first'
        ).find_all('div', class_='block__docs_container_cell')[4].find(
            'span', class_='price_nds'
        ).text

    def get_tender_lots_data(self, data_html):
        lots_divs = data_html.find_all('div', class_='block__docs_lot_content')
        lots = []
        for num, lot_div in enumerate(lots_divs, start=1):
            currency = self.find_lot_row(lot_div, 'Цена договора и требования к обеспечению', 'Валюта')
            if not currency:
                currency = self.get_currency_from_docs_container(data_html)
            lots.append({
                'number': num,
                'name': self.find_lot_row(lot_div, 'Цена договора и требования к обеспечению', 'Предмет договора'),
                'status': self.find_lot_row(lot_div, 'Этапы закупочной процедуры', 'Текущий статус'),
                'customer': self.find_lot_row(
                    lot_div, 'Заказчики, с которыми заключается договор', 'Наименование заказчика'
                ),
                'sub_close_date': self.clear_date_str(
                    self.find_lot_row(lot_div,
                                      'Этапы закупочной процедуры', 'Дата и время окончания срока приема заявок')
                ),
                'price': self.clear_double_data_str(
                    self.find_lot_row(lot_div, 'Цена договора и требования к обеспечению', 'Начальная цена')
                ),
                'guarantee_app': self.clear_double_data_str(
                    self.find_lot_row(
                        lot_div, 'Цена договора и требования к обеспечению', 'Размер обеспечения заявки (в рублях)'
                    )
                ),
                'payment_terms': self.find_lot_row(
                    lot_div, 'Условия договора', 'Условия оплаты и поставки товаров/выполнения работ/оказания услуг'),
                'quantity': self.find_lot_row(
                    lot_div, 'Условия договора',
                    'Количество поставляемого товара/объем выполняемых работ/оказываемых услуг'
                ),
                'delivery_place': self.get_lot_delivery_place(lot_div),
                'order_view_date': self.clear_date_str(
                    self.find_lot_row(lot_div, 'Этапы закупочной процедуры', 'Дата и время вскрытия заявок')),
                'scoring_date': self.clear_date_str(
                    self.find_lot_row(lot_div, 'Этапы закупочной процедуры', 'Дата подведения итогов')
                ),
                'scoring_datetime': self.clear_date_str(
                    self.find_lot_row(lot_div, 'Этапы закупочной процедуры', 'Подведение итогов не позднее')
                ),
                'publication_date': self.clear_date_str(
                    ''.join(
                        data_html.find(
                            'div', class_='block__docs_container').find('p', class_='datePublished').findAll(text=True)
                    ),
                ),
                'trade_date': self.clear_date_str(
                    self.find_lot_row(lot_div, 'Этапы закупочной процедуры', 'Дата и время проведения')
                ),
                'currency': currency,
                'positions': self.get_lot_positions(lot_div),
                'okpd2': self.get_lot_okpd_okved(lot_div, okpd2=True),
            })
        print(lots[0]['payment_terms'])
        return lots

    @staticmethod
    def clear_org_name(full_text, drop_text):
        return full_text.replace(drop_text, '').strip()

    def get_org_data(self, data_html):
        org_data_list = data_html.find(
            'div', class_='block__docs_container organizationInfo'
        ).find_all('div', class_='block__docs_container_cell')

        org = {
            'name': self.clear_org_name(
                org_data_list[0].find('h3').text, org_data_list[0].find('h3').find('a').text
            ),
            'actual_address': org_data_list[1].find_all('p')[1].text,
            'post_address': org_data_list[2].find_all('p')[1].text,
            'fio': org_data_list[6].find_all('p')[1].text,
            'phone': org_data_list[3].find_all('p')[1].text,
            'fax': org_data_list[4].find_all('p')[1].text,
            'email': org_data_list[5].find_all('p')[1].text,
            'place': org_data_list[7].find_all('p')[1].text,
            'region': self.get_region_from_address(org_data_list[2].find_all('p')[1].text,)
        }
        return org

    def clear_attachment_display_name(self, name):
        return re.search(r'(.+?)(\.[^.]*$|$)', name).group(1)

    def get_attachments(self, data_html):
        """
        Получение прикрепленных файлов
        """
        attachments = []
        attachments_div = data_html.find('div', class_='block__docs_container block__docs_container_download')
        files = attachments_div.find_all('div', class_='block__docs_container_cell')
        if len(files) == 1 and files[0].find('p').text == 'Нет прикрепленных документов':
            return attachments
        for file in files:
            attachments.append({
                'display_name': self.clear_attachment_display_name(file.find('a').text),
                'url': file.find('a').attrs['href'],
                'real_name': file.find('a').text,
                'publication_date': self.clear_date_str(file.find('time').text),
            })
        #print(attachments)
        return attachments
