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
    def clear_price(price_str):
        clear_price_str = re.search(r'(\d+\s\d+\s?)*,\d\d', price_str)
        if clear_price_str:
            return float(''.join(clear_price_str.group(0).replace(',', '.').split()))
        else:
            return None

    def get_price(self, data):
        price = data.find('div', class_='news-detail').find('p')
        if price:
            return self.clear_price(price.text)
        else:
            return None

    @staticmethod
    def find_tender_row(tender_table_rows, search_str):
        for row in tender_table_rows:
            row_cells = row.find_all('td')
            if row_cells[0].text.strip() == search_str:
                return row_cells[1].text
        return None

    def find_tender_link_row(self, tender_table_rows, search_str):
        for row in tender_table_rows:
            row_cells = row.find_all('td')
            if row_cells[0].text.strip() == search_str:
                return self.base_url + row_cells[1].find('a').attrs['href']
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
        customer = self.find_tender_row(tender_table_rows, 'Инициатор закупки:')
        tender_org = self.find_tender_row(tender_table_rows, 'Организатор закупки:')
        lots = [{
            'number_lot': self.find_tender_row(
                tender_table_rows, 'Номер лота:').replace('\t', '').replace('\n', '').strip(),
            'name': item_table.find('h1').text,
            'type': tender_table_rows[1].find_all('td')[1].findAll(text=True)[0].replace('\t', '').replace('\n', ''),
            'region': 2,
            'customer': customer.replace('\n', '') if customer else None,
            'price': self.get_price(item_table),
            'tander_org': tender_org.replace('\n', '').strip() if tender_org else None,
            'doc': self.find_tender_link_row(tender_table_rows, 'Закупочная документация:'),
            'result': self.find_tender_link_row(tender_table_rows, 'Закупочная документация:'),
        }]
        return lots

    @staticmethod
    def clear_org_name(full_text, drop_text):
        return full_text.replace(drop_text, '').strip()

    @staticmethod
    def get_phone_email(phone_email):
        phone_email = phone_email.replace('\t', '').replace('\n', '')
        email = re.search(r'\s\w+@[^@]+\.[^@]+', phone_email)
        if email:
            email = email.group(0).strip()
            phone = phone_email.replace(email, '').strip()
            return phone, email
        else:
            return phone_email.strip(), None

    def get_org_data(self, data_html):
        item_table = data_html.find_all('table', {'cellpadding': '10'})[0]
        tender = item_table.find('table')
        tender_table_rows = tender.find_all('tr')
        phone_email = self.get_phone_email(tender_table_rows[3].find_all('td')[1].text)
        org = {
            'name': tender_table_rows[4].find_all('td')[1].text.replace('\n', ''),
            'fio': tender_table_rows[2].find_all('td')[1].text.replace('\t', '').replace('\n', ''),
            'phone': phone_email[0],
            'email': phone_email[1],
        }
        return org

    def get_attachments(self, lot, item):
        doc_url, res_url = lot.get('doc'), lot.get('result')
        file_name_pattern = re.compile(r'[^%]+$')
        attachments = []
        if doc_url:
            file_name_doc = re.search(file_name_pattern, doc_url).group(0).replace('2F', '')
            attachments.append({
                'displayName': file_name_doc,
                'href': doc_url,
                'publicationDateTime': self.tools.get_utc_epoch(item['publication_datetime']),
                'realName': file_name_doc,
                'size': None
            })
        if res_url:
            file_name_res = re.search(file_name_pattern, doc_url).group(0).replace('2F', '')
            attachments.append({
                'displayName': file_name_res,
                'href': doc_url,
                'publicationDateTime': self.tools.get_utc_epoch(item['publication_datetime']),
                'realName': file_name_res,
                'size': None
            })
        return attachments
