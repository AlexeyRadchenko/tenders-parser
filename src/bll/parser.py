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
    def clear_date_str(date_str):
        if not date_str:
            return None
        try:
            date = re.search(r'\d\d\.\d\d\.\d\d', date_str).group(0)
            time = re.search(r'\d\d:\d\d', date_str).group(0)
        except AttributeError:
            return None
        return '{} {}'.format(date, time)

    @staticmethod
    def clear_double_data_str(data_str):
        if not data_str or data_str == 'Цена не указана' or data_str == 'Не установлен':
            return None
        elif '(сумма блокируется)' in data_str:
            data_str = data_str.replace('(сумма блокируется)', '').strip()
        return float(data_str.split('\n')[0].replace(' ', '').replace(',', '.'))

    @staticmethod
    def find_lot_row(lot_div, search_str):
        lot_data_strings = lot_div.find_all('p')
        for row in lot_data_strings:
            row_values = row.findAll(text=True)
            if row_values[0].strip() == search_str:
                # return ''.join(cells[1].findAll(text=True)).strip()
                return row_values[1:]
        return None

    def get_tech_part_date(self, info_block):
        tech_part_date = self.find_lot_row(info_block, 'Дата продления Технической части:')
        if not tech_part_date:
            tech_part_date = self.find_lot_row(info_block, 'Дата принятия Технической части:')
        return tech_part_date

    def get_commercial_part_date(self, info_block):
        commercial_part_date = self.find_lot_row(info_block, 'Дата продления Коммерческой части:')
        if not commercial_part_date:
            commercial_part_date = self.find_lot_row(info_block, 'Дата принятия Коммерческой части:')
        return commercial_part_date

    def get_tender_status(self, info_block):
        tech_part_date = self.get_tech_part_date(info_block)
        clear_tech_date = self.tools.get_utc_epoch(tech_part_date[0])
        current_date = self.tools.get_utc()
        if clear_tech_date > current_date:
            return 1
        else:
            return 3

    def get_tender_lots_data(self, data_html):
        info_block = data_html.find_all('div', class_='text-block')[-1]
        # print(self.find_lot_row(info_block, 'Дополнительная информация:'))
        lot = {
            'name': data_html.find('div', class_='info-lot').find('p').text,
            'status': self.get_tender_status(info_block),
            'customer': 'АО «ЕВРАЗ ЗСМК»',
            'region': 42,
            'dop_info': ''.join(self.find_lot_row(info_block, 'Дополнительная информация:')),
            'tender_poccess_start': self.find_lot_row(info_block, 'Дата начала работ:')[0],
            'tender_proccess_end': self.find_lot_row(info_block, 'Дата окончания работ:')[0],
            'tech_part_date': self.get_tech_part_date(info_block),
            'commercial_part_date': self.get_commercial_part_date(info_block),
            'odrder_submission': self.get_order_submission(info_block),

            'sub_close_date': self.clear_date_str(
                self.find_lot_row(lot_div,
                                  'Этапы закупочной процедуры', 'Дата и время окончания срока приема заявок'),
            ),
            'price': self.clear_double_data_str(
                'odrder_submission'
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
            )
        ),
        'trade_date': self.clear_date_str(
            self.find_lot_row(lot_div, 'Этапы закупочной процедуры', 'Дата и время проведения')
        ),
        'currency': currency,
        'positions': self.get_lot_positions(lot_div),
        'okpd2': self.get_lot_okpd_okved(lot_div, okpd2=True),
        }
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
            'address': org_data_list[2].find_all('p')[1].text,
            'fio': org_data_list[6].find_all('p')[1].text,
            'phone': org_data_list[3].find_all('p')[1].text,
            'fax': org_data_list[4].find_all('p')[1].text,
            'email': org_data_list[5].find_all('p')[1].text,
            'place': org_data_list[7].find_all('p')[1].text,
            'region': self.get_region_from_address(org_data_list[2].find_all('p')[1].text, )
        }
        return org

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
                'display_name': file.find('a').text,
                'url': file.find('a').attrs['href'],
                'real_name': file.find('a').text,
                'publication_date': file.find('time').text,
            })
        return attachments