from src.tools import Tools, ORG_REGION_MAP
import re


class Parser:
    """
    Класс для парсинга страниц
    """
    def __init__(self, base_url=None):
        self.tools = Tools()
        self.base_url = base_url

    @staticmethod
    def get_time_delta(delta_str):
        try:
            time_delta = int(re.search(r'UTC\+\d+', delta_str).group(0).replace('UTC+', ''))
        except AttributeError:
            return None
        return time_delta

    @staticmethod
    def clear_date_str(date_str, time_delta):
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

        return date_time_str, time_delta

    @staticmethod
    def get_lot_deadline(deadline_str):
        try:
            date = re.search(r'\d\d\.\d\d\.\d\d\d\d', deadline_str).group(0)
        except AttributeError:
            return deadline_str
        return date

    @staticmethod
    def get_id_from_url(url):
        num_str = re.search(r'\d+', url)
        if num_str:
            return num_str.group(0)

    def get_part_data(self, data_list):
        """парсим строки пришедшие в запросе возвращаем список первичных данных"""
        item_list = []
        for item_data in data_list:
            info_blocks = item_data.find_all('div', class_='grid__item')
            left_data = info_blocks[0].find_all('div')
            right_data = info_blocks[1].find_all('div')
            item_list.append({
                'id': self.get_id_from_url(item_data.find('a').attrs['href']),
                'number': item_data.find('a').text.replace('№ ', ''),
                'name': right_data[0].find_all('span')[1].text,
                'link': self.base_url + item_data.find('a').attrs['href'],
                'type': left_data[2].find_all('span')[1].text,
                'status': left_data[0].find_all('span')[1].text,
                'customer': right_data[3].find_all('span')[1].text,
                'target_place': right_data[4].find_all('span')[1].text,
            })
        return item_list

    @staticmethod
    def find_lot_form_data(lot_forms_data, search_str):
        #print(len(lot_forms_data), lot_forms_data)
        lot_blocks_map = {
            'Реестровый номер': lot_forms_data[0].find_all('div')[1].text,
            'Заказчик': lot_forms_data[1].find_all('div')[1].text,
            'Наименование закупки': lot_forms_data[2].find_all('div')[1].text,
            'Категория закупки конкурентной процедуры': lot_forms_data[4].find_all('div')[1].text,
            'Местное время': lot_forms_data[7].find_all('div')[1].text,
            'Дата и время начала приёма предложений': lot_forms_data[8].find('div', class_='four-sevenths').text,
            'Дата и время окончания приёма предложений': lot_forms_data[9].find('div', class_='four-sevenths').text,
            'Дата вскрытия': lot_forms_data[10].find('div', class_='four-sevenths').text,
            'Контактный телефон': lot_forms_data[11].find_all('div')[1].text,
            'Контактный e-mail': lot_forms_data[12].find_all('div')[1].text,
            'Информационное сообщение': lot_forms_data[14].find_all('div')[1].text if len(lot_forms_data) > 15 else None,
        }
        return lot_blocks_map[search_str]

        """for row in lot_blocks_map[block_name].find_all('div', class_='block__docs_container_cell'):
            cells = row.find_all('p')
            if cells[0].text.strip() == search_str:
                return ''.join(cells[1].findAll(text=True)).strip()
        return None"""

    @staticmethod
    def lots_exists(lots_table):
        if lots_table.find_all('tr')[1].find('td').text == ' - лотов нет -':
            return False
        else:
            return True

    def get_tender_lots_data(self, data_html):
        lots = []
        lots_table = data_html.find('table', {'id': 'table_spec'})
        table_rows = lots_table.find_all('tr')
        lots_exists = self.lots_exists(lots_table)
        lot_forms_divs = data_html.find('div', class_='tile').find('form').find_all('div', class_='form-group_indent_s')
        for num, lot_row in enumerate(table_rows[1:], start=1):
            data = lot_row.find_all('td')
            time_delta = self.get_time_delta(
                self.find_lot_form_data(lot_forms_divs, 'Местное время')
            )
            lots.append({
                'number': num,
                'name': data[1].text.replace('\n', '').replace('\t', '') if lots_exists else None,
                'processing_time': data[2].text.replace('\n', '').replace('\t', '') if lots_exists else None,
                'volume': data[3].text.replace('\n', '').replace('\t', '') if lots_exists else None,
                'lot_subject': data[4].text.replace('\n', '').replace('\t', '') if lots_exists else None,
                'publication_date': self.clear_date_str(
                    self.find_lot_form_data(lot_forms_divs, 'Дата и время начала приёма предложений'),
                    time_delta
                ),
                'sub_start_date': self.clear_date_str(
                    self.find_lot_form_data(lot_forms_divs, 'Дата и время начала приёма предложений'),
                    time_delta
                ),
                'sub_close_date': self.clear_date_str(
                    self.find_lot_form_data(lot_forms_divs, 'Дата и время окончания приёма предложений'),
                    time_delta
                ),
                'order_view_date': self.clear_date_str(
                    self.find_lot_form_data(lot_forms_divs, 'Дата вскрытия'),
                    time_delta
                ),
                'info_msg': self.find_lot_form_data(lot_forms_divs, 'Информационное сообщение'),
            })
        return lots

    @staticmethod
    def get_customer_region(customer):
        clear_name = re.search(r'«[^»]+', customer)
        if clear_name:
            return ORG_REGION_MAP[clear_name.group(0).lstrip('«')]

    def get_org_data(self, data_html):
        lot_forms_divs = data_html.find('div', class_='tile').find('form').find_all('div', class_='form-group_indent_s')
        org = {
            'name': self.find_lot_form_data(lot_forms_divs, 'Заказчик'),
            'phone': self.find_lot_form_data(lot_forms_divs, 'Контактный телефон'),
            'email': self.find_lot_form_data(lot_forms_divs, 'Контактный e-mail'),
            'region': self.get_customer_region(self.find_lot_form_data(lot_forms_divs, 'Заказчик'))
        }
        return org

    def clear_attachment_display_name(self, name):
        return re.search(r'(.+?)(\.[^.]*$|$)', name).group(0)

    def get_attachments(self, data_html):
        """
        Получение прикрепленных файлов
        """
        attachments = []
        attachments_table = data_html.find('table', {'id': 'files'})
        files = attachments_table.find('tbody').find_all('tr')
        lot_forms_divs = data_html.find('div', class_='tile').find('form').find_all('div', class_='form-group_indent_s')
        time_delta = self.get_time_delta(
            self.find_lot_form_data(lot_forms_divs, 'Местное время')
        )
        for file in files:
            data = file.find_all('td')

            attachments.append({
                'display_name': data[0].find('a').text,
                'url': self.base_url + data[0].find('a').attrs['href'],
                'real_name': data[0].find('a').text,
                'publication_date': self.clear_date_str(
                    self.find_lot_form_data(lot_forms_divs, 'Дата и время начала приёма предложений'),
                    time_delta
                ),
            })
        return attachments
