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
    def get_tender_number_from_url(url):
        return re.search(r'ID=\d+', url).group(0).lstrip('ID=')

    @staticmethod
    def get_start_close_datetime(date_str_list):
        find_str = re.findall(r'\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}:\d{2}', ' '.join(date_str_list))
        return find_str

    @staticmethod
    def get_price(data):
        price = data.find('div', class_='news-detail').find('p')
        if price:
            return price.findAll(text=True)
        else:
            return None

    def get_parsed_items_list(self, data_list):
        """парсим строки пришедшие в запросе возвращаем список первичных данных"""
        item_list = []
        for item_data in data_list[1:]:
            row_data = item_data.find_all('td')
            if not row_data[0].find('a', class_='outerlink'):
                start_and_close_submit = self.get_start_close_datetime(row_data[2].findAll(text=True))
                pub_and_chage = self.get_start_close_datetime(row_data[3].findAll(text=True))
                item_list.append({
                    'number': self.get_tender_number_from_url(row_data[0].find('a').attrs['href']),
                    'name': row_data[0].text.strip('\n'),
                    'link': self.base_url + row_data[0].find('a').attrs['href'],
                    'org_name': row_data[1].text.replace('\n', '').strip(),
                    'org_link': self.base_url + row_data[1].find('a').attrs['href'],
                    'start_sub_datetime': start_and_close_submit[0],
                    'close_sub_datetime': start_and_close_submit[1],
                    'publication_datetime': pub_and_chage[0],
                    'change_datetime': pub_and_chage[1],
                })
        return item_list

    def get_tender_lots_data(self, data_html):
        item_table = data_html.find_all('table', {'cellpadding': '10'})[0]
        tender = item_table.find('table')
        tender_table_rows = tender.find_all('tr')
        lots = [{
            'number': tender_table_rows[0].find_all('td')[1].text,
            'name': item_table.find('h1').text,
            'type': tender_table_rows[1].find_all('td')[1].text,
            'region': 2,
            'customer': [tender_table_rows[4].find_all('td')[1].text],
            'price': self.get_price(item_table),
            'tander_org': tender_table_rows[5].find_all('td')[1].text,
            'result': self.base_url + tender_table_rows[7].find('a').attrs['href'],
        }]
        return lots

    @staticmethod
    def clear_org_name(full_text, drop_text):
        return full_text.replace(drop_text, '').strip()

    def get_org_data(self, data_html):
        item_table = data_html.find_all('table', {'cellpadding': '10'})[0]
        tender = item_table.find('table')
        tender_table_rows = tender.find_all('tr')
        phone_email = tender_table_rows[3].find_all('td')[1].text
        org = {
            'name': tender_table_rows[4].find_all('td')[1].text,
            'fio': tender_table_rows[2].find_all('td')[1].text,
            'phone': phone_email,
            'email': phone_email,
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
                'publication_date': file.find('time').text,
            })
        return attachments
