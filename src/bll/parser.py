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

    @staticmethod
    def clear_double_data_str(data_str):
        if not data_str or data_str == 'Цена не указана' or data_str == 'Не установлен':
            return None
        elif '(сумма блокируется)' in data_str:
            data_str = data_str.replace('(сумма блокируется)', '').strip()
        return float(data_str.split('\n')[0].replace(' ', '').replace(',', '.'))

    def get_tender_number(self, html):
        tender_name = html.find('div', {'class': 'item-text'}).find('a').text
        tender_sub_end_date = html.find('div', {'class': 'item-data'}).findAll(text=True)[4].replace('\t', '').strip()
        hashing_str = (tender_name + tender_sub_end_date).encode('utf-8')
        return 'УХ{}'.format(int(sha256(hashing_str).hexdigest(), 16) % 10 ** 8)

    def get_status(self, html):
        tender_sub_end_date = self.tools.get_utc_epoch(
            html.find('div', {'class': 'item-data'}).findAll(text=True)[4].replace('\t', '').strip()
        )
        if not tender_sub_end_date:
            return 0
        current_date = self.tools.get_utc()
        if current_date < tender_sub_end_date:
            return 1
        else:
            return 3

    def get_attachments(self, html):
        """
        Получение прикрепленных файлов
        """
        attachments = list()
        url = html.find('div', {'class': 'item-text'}).find('a').attrs['href']
        if not url:
            return attachments
        name_ext = re.search(r'[^/]+$', url)
        ext = re.search(r'.[^.]+$', url)
        if name_ext:
            name_ext = name_ext.group(0)
        if ext:
            ext = ext.group(0)
        attachments.append({
            'display_name': name_ext.replace(ext, ''),
            'url': self.base_url + url,
            'real_name': name_ext,
            'publication_date': self.clear_date_str(html.find('div', {'class': 'item-data'}).findAll(text=True)[1]),
        })
        #print(attachments)
        return attachments

    def get_part_data(self, data_list, tender_type, url):
        """парсим строки пришедшие в запросе возвращаем список первичных данных"""
        item_list = []
        for item_data in data_list:
            number = self.get_tender_number(item_data)
            org = item_data.find('div', {'class': 'item-affiliate'})
            item_list.append({
                'id': '{}_1'.format(number),
                'number': number,
                'name': item_data.find('div', {'class': 'item-text'}).find('a').text,
                'status': self.get_status(item_data),
                'customer': '“АО ХК Уралхим”' if tender_type == 0 else 'ООО “Уралхим”',
                'sub_close_date': item_data.find(
                    'div', {'class': 'item-data'}).findAll(text=True)[4].replace('\t', '').strip(),
                'org': org.find('a').text if org else None,
                'publication_date': self.clear_date_str(
                    item_data.find('div', {'class': 'item-data'}).findAll(text=True)[1]),
                'attachments': self.get_attachments(item_data),
                'link': url
            })
        return item_list
