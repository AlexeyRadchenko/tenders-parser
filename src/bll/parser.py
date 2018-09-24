from src.tools import Tools, REGION_MAP
import re


class Parser:
    """
    Класс для парсинга страниц
    """
    def __init__(self, base_url=None):
        self.tools = Tools()
        self.base_url = base_url

    def get_arc_after_status(self, status_str):
        #print('_'+status_str+'_')
        if status_str == 'завершен':
            return 3
        elif status_str == 'отменен':
            return 4

    def get_arc_after_tender_list(self, html):
        arc_data = []
        data_rows = html.find_all('tr', {'class': 'Info'})
        names = html.find_all('tr', {'class': 'Name'})
        for i, row in enumerate(data_rows):
            row_values = row.find_all('td')
            arc_data.append({
                'id': '{}_1'.format(row_values[0].text.replace(' ', '')),
                'number': row_values[0].text,
                'name': names[i].find('h2').text,
                'end_date': row_values[1].text,
                'winner': row_values[2].text if row_values[2].text != '\xa0' else None,
                'status': self.get_arc_after_status(row_values[3].text),
                'data_type': 'arc_after',
            })
        return arc_data

    def get_active_after_tender_data(self, html, url):
        main_section = html.find('section', {'id': 'Content'})
        table_rows_data = main_section.find('tr', {'class': 'Info'}).find_all('td')
        attachments_data = main_section.find('div', {'class': 'defc'}).find_all('li')
        tender_data = {
            'id': '{}_1'.format(table_rows_data[0].text.replace('\xa0', '').replace(' ', '')),
            'name': main_section.find('h1').find('a').text,
            'number': table_rows_data[0].text.replace('\xa0', '').replace(' ', ''),
            'status': 1,
            'region': 38,
            'customer': 'ООО "Иркутская нефтяная компания"',
            'sub_start_date': self.clear_date_str(table_rows_data[1].text),
            'sub_close_date': self.clear_date_str(table_rows_data[2].text),
            'attachments': self.get_attachments(attachments_data, table_rows_data[1].text),
            'link': url,
        }
        return tender_data

    def get_arc_before_tender_list(self, html):
        arc_data = []
        tenders_data = html.find_all('div', {'class': 'tenders_item'})
        if not tenders_data:
            tenders_data = [html.find('div', {'class': 'tenders_item'})]
        for tender in tenders_data:
            head = tender.find('div', {'class': 'tenders_item_head'}).find('tr').find_all('td')
            content = tender.find('div', {'class': 'tenders_item_content'})
            arc_data.append({
                'id': '{}_1'.format(head[0].text.replace('\xa0', '').replace(' ', '')),
                'name': content.find('h2').find('a').text,
                'number': head[0].text,
                'status': 3 if head[3].text == 'Исполнен' else 4,
                'customer': 'ООО "Иркутская нефтяная компания"',
                'end_date': head[1].text.replace('\n', '').replace('\t', '').replace('-', '.'),
                'winner': head[2].text.replace('\n', '').replace('\t', ''),
                'data_type': 'arc_before',
            })
        return arc_data

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

    def get_file_real_name(self, url):
        name = re.search(r'[^\/]+$', url)
        if name:
            return name.group().split('.')[0]

    def get_attachments(self, data_html, tender_date):
        """
        Получение прикрепленных файлов
        """
        attachments = []
        for file in data_html[1:]:
            attachments.append({
                'display_name': file.findAll(text=True)[0].replace(': ', ''),
                'url': file.find('a').attrs['href'],
                'real_name': self.get_file_real_name(file.find('a').attrs['href']),
                'publication_date': self.clear_date_str(tender_date),
                'size': None
            })
        #print(attachments)
        return attachments



