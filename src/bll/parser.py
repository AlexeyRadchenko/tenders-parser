from src.tools import Tools, REGION_MAP
import re
from bs4 import BeautifulSoup
from hashlib import md5


class Parser:
    """
    Класс для парсинга страниц
    """
    def __init__(self, base_url=None):
        self.tools = Tools()
        self.base_url = base_url

    @staticmethod
    def get_tender_name(name_str):
        html = BeautifulSoup(name_str, 'lxml')
        return html.find('a').text

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

    def get_tender_status(self, date_str):
        date_deadline = self.tools.get_utc_epoch(self.clear_date_str(date_str)[0])
        current_time = self.tools.get_utc()
        if current_time < date_deadline:
            return 1
        else:
            return 3

    def get_email(self, contacts_str):
        html = BeautifulSoup(contacts_str, 'lxml')
        return html.find('a').attrs['href'].replace('mailto:', '')

    def get_phone(self, contacts_str):
        html = BeautifulSoup(contacts_str, 'lxml')
        return html.find('span').text

    def get_real_name_doc(self, url):
        name = re.search('[^/]+$', url)
        return name.group(0) if name else None

    def get_attachments(self, data_str):
        html = BeautifulSoup(data_str, 'lxml')
        attachments = [{
            'displayName': html.find('a').text,
            'href': self.base_url + html.find('a').attrs['href'],
            'realName': self.get_real_name_doc(html.find('a').attrs['href']),
            'publicationDateTime': self.tools.get_utc(),
            'size': None,
        }]
        return attachments

    def get_hash_from_url(self, data_str):
        html = BeautifulSoup(data_str, 'lxml')
        url_str = html.find('a').attrs['href'].encode('utf-8')
        return md5(url_str).hexdigest()

    def get_part_data(self, data_list):
        """парсим строки пришедшие в запросе возвращаем список первичных данных"""
        item_list = []
        for item_data in data_list:
            item_list.append({
                'id': self.get_hash_from_url(item_data['subject_procurement']),
                'name': self.get_tender_name(item_data['subject_procurement']),
                'sub_close_date': self.tools.get_utc_epoch(self.clear_date_str(item_data['deadline'])[0]),
                'submit_type': item_data['how_apply'],
                'type': item_data['method_carrying'],
                'status': self.get_tender_status(item_data['deadline']),
                'region': None,
                'customer': item_data['customer'],
                'email': self.get_email(item_data['contacts']),
                'phone': self.get_phone(item_data['contacts']),
                'attachments': self.get_attachments(item_data['subject_procurement']),
                'publication_date': self.tools.get_utc(),
                'customer_address': item_data['address'],
            })
        return item_list
