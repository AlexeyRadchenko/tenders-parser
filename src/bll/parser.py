from src.tools import Tools, REGION_MAP
import re
from hashlib import sha256


class Parser:
    """
    Класс для парсинга страниц
    """
    def __init__(self, base_url=None):
        self.tools = Tools()
        self.base_url = base_url

    @staticmethod
    def get_map_tender_data(tender_div):
        data_block = tender_div.find('dl')
        data_name_list = data_block.find_all('dt')
        data_value_list = data_block.find_all('dd')
        data_map = {}
        for index, name in enumerate(data_name_list):
            data_map[name.text] = data_value_list[index].text
        return data_map

    @staticmethod
    def item_filter(item_data):
        regex = re.compile(r'ГП\d+')
        if (item_data.get('Предмет') and regex.search(item_data.get('Предмет'))) or \
                (item_data.get('Номер процедуры') and regex.search(item_data.get('Номер процедуры'))) or \
                'https://etp.gpb.ru' == item_data.get('Место рассмотрения'):
            return False
        else:
            return True

    @staticmethod
    def clear_date_str(date_str):
        if not date_str:
            return None
        try:
            date = re.search(r'\d\d\.\d\d\.\d\d\d\d', date_str).group(0)
        except AttributeError:
            return None

        try:
            time = re.search(r'\d\d:\d\d:\d\d', date_str).group(0)
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

    def get_hash_from_name_pub_date(self, data_html):
        name_str = data_html.find('h4').text
        pub_date = data_html.find('p', {'class': 'date'}).find('strong').text
        hashing_str = (pub_date + name_str).encode('utf-8')
        return 'УМ{}_1'.format(int(sha256(hashing_str).hexdigest(), 16) % 10 ** 8)

    def get_tender_status(self, sub_start_date, sub_close_date, scoring_date):
        sub_start_datetime_utc = self.tools.get_utc_epoch(sub_start_date)
        sub_close_datetime_utc = self.tools.get_utc_epoch(sub_close_date)
        scoring_datetime_utc = self.tools.get_utc_epoch(scoring_date)
        now_date_time = self.tools.get_utc()
        if now_date_time >= scoring_datetime_utc:
            return 3
        elif now_date_time >= sub_close_datetime_utc:
            return 2
        elif now_date_time >= sub_start_datetime_utc:
            return 1
        elif sub_start_datetime_utc == sub_close_datetime_utc and now_date_time < sub_close_datetime_utc:
            return 1
        else:
            return 0

    def get_part_data(self, data_list):
        """парсим строки пришедшие в запросе возвращаем список первичных данных"""
        item_list = []
        for item_data in data_list:
            item_data_map = self.get_map_tender_data(item_data)
            if self.item_filter(item_data_map):
                sub_start_close_date = item_data_map.get('Срок приёма заявок').split(' - ')
                item_list.append({
                    'id': self.get_hash_from_name_pub_date(item_data),
                    'name': item_data.find('h4').text,
                    'region': 66,
                    'customer': 'ПАО Уралмашзавод',
                    'sub_start_date': self.tools.get_utc_epoch(sub_start_close_date[0]),
                    'sub_close_date': self.tools.get_utc_epoch(sub_start_close_date[1]),
                    'scoring_date': self.tools.get_utc_epoch(
                        self.clear_date_str(item_data_map.get('Дата подведения итогов'))[0]
                    ),
                    'type': item_data_map.get('Способ'),
                    'currency': item_data_map.get('Валюта'),
                    'subject': item_data_map.get('Предмет'),
                    'scoring_place': item_data_map.get('Место рассмотрения'),
                    'fio': item_data_map.get('ФИО ответственного'),
                    'phone': item_data_map.get('Телефон ответственного'),
                    'email': item_data_map.get('E-mail ответственного'),
                    'publication_date': self.tools.get_utc_epoch(
                        item_data.find('p', {'class': 'date'}).find('strong').text),
                    'status': self.get_tender_status(
                        sub_start_close_date[0], sub_start_close_date[1],
                        self.clear_date_str(item_data_map.get('Дата подведения итогов'))[0]
                    ),
                })
        return item_list
