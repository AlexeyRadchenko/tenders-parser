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
            item_list.append({
                'id': item_data['id'],
                'number': item_data['registry_number'],
                'name': item_data['title'],
                'link': '{}{}{}'.format(self.base_url, '#com/procedure/view/procedure/', item_data['id']),
                'publication_date': self.clear_date_str(item_data['date_published2']),
                'type': item_data['procedure_type'],
                'price': item_data['total_price'],
                'org': item_data['full_name'],
                'currency': item_data['currency_name'],
            })
        return item_list

    @staticmethod
    def get_region_from_address(address_str):
        for key in REGION_MAP.keys():
            if key in address_str.lower():
                return REGION_MAP[key]

    def get_tender_lots_data(self, tender_data_dict):
        lots = []
        for num, lot in enumerate(tender_data_dict['lots'], start=1):
            lots.append({
                'number': num,
                'name': lot['lot_units'][0]['name'],
                'type': tender_data_dict['procedure_type_vocab'],
                'customer': lot['lot_customers'][0]['full_name'],
                'region': self.get_region_from_address(tender_data_dict['org_postal_address']),
                'sub_close_date': self.clear_date_str(lot['date_end_registration']),
                'price': lot['start_price'],
                'guarantee_app': self.clear_double_data_str(
                    self.find_lot_row(
                        lot_div, 'Цена договора и требования к обеспечению', 'Размер обеспечения заявки (в рублях)'
                    )
                ),
                'payment_terms': self.find_lot_row(
                    lot_div, 'Условия договора', 'Условия оплаты и поставки товаров/выполнения работ/оказания услуг'),
                'delivery_volume': lot['lot_delivery_places'][0]['quantity'],
                'delivery_place': lot['lot_delivery_places'][0]['address'],
                'delivery_datetime': self.clear_date_str(lot['lot_delivery_places'][0]['req_dlv_date']),
                'delivery_term': lot['lot_delivery_places'][0]['term'],
                'delivery_basis': lot['lot_delivery_places'][0]['basis'],
                'quantity': lot['lot_units'][0]['quantity'],
                'trade_mark': lot['lot_units'][0]['trade_mark'],
                'units_symbol': lot['lot_units'][0]['okei_symbol'],
                'org': tender_data_dict['org_full_name'],
                'org_address': tender_data_dict['org_postal_address'],
                'org_fio': tender_data_dict['organizer_user_full_name'],
                'org_phone':tender_data_dict['contact_phone'],
                'org_email': tender_data_dict['contact_email'],
                'order_view_date': self.clear_date_str(
                    self.find_lot_row(lot_div, 'Этапы закупочной процедуры', 'Дата и время вскрытия заявок')),
                'scoring_date': self.clear_date_str(lot['date_end_second_parts_review'])),
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
                'currency': lot['currency_vocab'],
                'positions': self.get_lot_positions(lot_div),
                'okpd2': self.get_lot_okpd_okved(lot_div, okpd2=True),
            })
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
