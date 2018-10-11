from src.tools import Tools, REGION_MAP
import re


class Parser:
    """
    Класс для парсинга страниц
    """
    def __init__(self, base_url=None):
        self.tools = Tools()
        self.base_url = base_url

    def item_filter(self, column):
        url = column.find('a')
        if url:
            return re.sub(r'\s(\d)', '',  url.text), '{}{}{}'.format(self.base_url, '/pls/tzp/', url.attrs['href'])
        else:
            return re.search(r'\d+-\d+', column.text).group(), None

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
        if not data_str:
            return None
        return float(data_str.replace(' ', '').replace(',', '.'))

    @staticmethod
    def clear_customer_name(name):
        return re.sub(r'^\d+', '', name)

    @staticmethod
    def get_attachment_real_name_display_name_size(name):
        size = re.search(r'\(.+\)', name)
        if size:
            size = size.group(0)
        else:
            size = ''
        real_name = name.replace(size, '').strip()
        display_name = real_name[:-4]
        return real_name, display_name, size[1:-1]

    @staticmethod
    def get_file_id(js_link):
        fid = re.search(r'\(\d+', js_link)
        if fid:
            return fid.group(0).replace('(', '')

    def get_part_data(self, data_list):
        """парсим строки пришедшие в запросе возвращаем список первичных данных"""
        item_list = []
        for item_data in data_list:
            table_columns = item_data.find_all('td')
            item_number, url = self.item_filter(table_columns[1])
            if item_number:
                #print(item_number)
                item_list.append({
                    'id': '{}_1'.format(item_number),
                    'number': item_number,
                    'name': table_columns[2].text,
                    'link': url,
                    'status': table_columns[3].text,
                    'customer': table_columns[4].text,
                    'price': self.clear_double_data_str(table_columns[5].text),
                    'currency': table_columns[6].text,
                    'publication_date': table_columns[7].text,
                    'sub_start_date': table_columns[8].text,
                    'sub_close_date': table_columns[9].text,
                })
        return item_list

    def find_conditions_main_report(self, table_rows):
        all_text = [row.findAll(text=True)[0] for row in table_rows]
        sub_date = all_text[1].split(': ')
        sub_end_or_score = all_text[2].split(': ')

        conditions = {
            'publication_date': self.clear_date_str(table_rows[0].findAll(text=True)[0].split(': ')[1]),
            'sub_start_date': self.clear_date_str(sub_date[1]) if 'приема предложений' in sub_date[0] else None,
            'sub_close_date': self.clear_date_str(sub_end_or_score[1]) if 'приема предложений' in sub_end_or_score[0] else None,
            'score_date': self.clear_date_str(sub_end_or_score[1]) if 'проведения торгов' in sub_end_or_score[0] else None,
            'info': ' '.join([text for text in all_text if ': ' not in text])
        }
        return conditions

    def find_main_report_row(self, table_rows, search_row):
        for i, row in enumerate(table_rows):
            row_data = row.find('td').findAll(text=True)
            #print(row_data)
            if row_data and row_data[0] == 'Товары, работы, услуги':
                break
            if row_data and row_data[0].strip() == search_row and search_row == 'Условия проведения:':
                return self.find_conditions_main_report(table_rows[i + 1].find('table').find_all('tr'))
            elif row_data and row_data[0].strip() == search_row:
                return row_data[1]
        return None

    def get_main_report_parsed_data(self, html):
        table_rows = html.find_all('tr')
        header = table_rows[1].find('span').text
        main_report = {
            'name': header,
            'type': self.find_main_report_row(table_rows, 'Тип торгов:'),
            'status': self.find_main_report_row(table_rows, 'Статус:'),
            'customer': self.clear_customer_name(self.find_main_report_row(table_rows, 'Заказчик:')),
            'conditions': self.find_main_report_row(table_rows, 'Условия проведения:'),
            'fio': self.find_main_report_row(table_rows, 'Контактное лицо заказчика:'),
        }
        return main_report

    def get_tender_objects_parsed_data(self, html):
        try:
            table_rows = html.find_all('tbody')[1].find_all('tr')
        except IndexError:
            table_rows = html.find('tbody').find_all('tr')
        items = []
        for row in table_rows:
            row_values = row.find_all('td')
            if row_values[0].text != '1':
                return None
            items.append({
                'num': row_values[0].text,
                'name': row_values[1].text,
                'quantity': row_values[2].text,
                'measure': row_values[3].text,
                'notice': row_values[4].text.replace('\\r\\n', '') if len(row_values) >= 5 else None,
            })
        return items

    def find_tender_conditions_row(self, table_rows, search_row):
        for row in table_rows:
            row_data = row.findAll(text=True)
            if row_data[0] == search_row:
                return row_data[1]
        return None

    def find_attachments_from_tender_conditions(self, table_rows, pub_date):
        donwload_url = 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?' \
                       'p_flow_id=220&p_flow_step_id=2155&' \
                       'p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01={}&x02=87539780000&x03=87507700000'
        attachments = []
        for row in table_rows:
            row_data = row.find_all('td')[1]
            link = row_data.find('a')
            if link:
                real, display, size = self.get_attachment_real_name_display_name_size(link.text)
                attachments.append({
                    'display_name': display,
                    'url': donwload_url.format(self.get_file_id(link.attrs['href'])),
                    'real_name': real,
                    'publication_date': pub_date,
                    'size': size
                })
        return attachments

    def get_tender_conditions_parsed_data(self, html, pub_date):
        table_rows = html.find_all('tr')
        tender_conditions = {
            'delivery_place': self.find_tender_conditions_row(table_rows, 'Место поставки'),
            'delivery_terms': self.find_tender_conditions_row(table_rows, 'Условия и сроки поставки'),
            'payment_terms': self.find_tender_conditions_row(table_rows, 'Условия и сроки оплаты'),
            'requirements_bidders': self.find_tender_conditions_row(table_rows, 'Требования к участникам торгов'),
            'price_terms': self.find_tender_conditions_row(table_rows, 'Цена'),
            'sub_time_terms': self.find_tender_conditions_row(table_rows, 'Время подачи ценового предложения'),
            'contract_sign_time': self.find_tender_conditions_row(table_rows, 'Срок заключения контракта'),
            'price_bidders_terms': self.find_tender_conditions_row(table_rows, 'Требование к цене'),
            'info_bidders': self.find_tender_conditions_row(table_rows, 'Информация для поставщиков'),
            'additional_terms': self.find_tender_conditions_row(table_rows, 'Дополнительные условия'),
            'delivery_requirements': self.find_tender_conditions_row(table_rows, 'Требования к поставке'),
            'attachments': self.find_attachments_from_tender_conditions(table_rows, pub_date),
        }
        return tender_conditions

    def get_tender_data(self, data_html, item):
        tables = data_html.find('table').find('table').find_all('table')
        other_reports_tables = data_html.find('table').find('table').find_all('table', {'class': 'ReportTbl'})
        #instance_id = html.find('input', {'id', 'pInstance'}).attrs['value']
        main_report = tables[2]
        tender_objects = other_reports_tables[0]
        tender_conditions = other_reports_tables[1]
        #conditions = other_reports_tables[2]

        main_report_parserd_data = self.get_main_report_parsed_data(main_report)
        #print('main_data', main_report_parserd_data)
        tender_objects_parsed_data = self.get_tender_objects_parsed_data(tender_objects)
        #print('obj', tender_objects_parsed_data)
        tender_conditions_parsed_data = self.get_tender_conditions_parsed_data(
            tender_conditions, main_report_parserd_data['conditions']['publication_date'])
        #print(tender_conditions_parsed_data)
        #conditions_parserd_data = self.get_conditions_parsed_data(conditions)

        
        tender = {
            'id': item['id'],
            'number': item['number'],
            'name': main_report_parserd_data['name'],
            'type': main_report_parserd_data['type'],
            'status': main_report_parserd_data['status'],
            'customer': main_report_parserd_data['customer'],
            'price': item['price'],
            'delivery_place': tender_conditions_parsed_data['delivery_place'],
            'delivery_terms': tender_conditions_parsed_data['delivery_terms'],
            'positions': tender_objects_parsed_data,
            'sub_start_date': item['sub_start_date'] if item['sub_start_date'] else main_report_parserd_data['conditions']['sub_start_date'][0],
            'sub_close_date': main_report_parserd_data['conditions']['sub_close_date'],
            'scoring_date': main_report_parserd_data['conditions']['score_date'],
            'sub_order': main_report_parserd_data['conditions']['info'],
            'fio': main_report_parserd_data['fio'],
            'publication_date': main_report_parserd_data['conditions']['publication_date'],
            'attachments': tender_conditions_parsed_data['attachments'],
            'link': item['link'],
            'tender_conditions': tender_conditions_parsed_data,
        }
        return tender
