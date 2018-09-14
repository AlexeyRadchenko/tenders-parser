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
    def find_lot_row(lot_div, search_str):
        lot_data_strings = lot_div.find_all('p')
        for row in lot_data_strings:
            row_values = row.findAll(text=True)
            if search_str == 'Техническая документация к лоту:' and row_values[0].strip() == search_str:
                return row
            elif row_values[0].strip() == search_str:
                return row_values[1:]
        return None

    def get_tech_part_date_for_status(self, info_block):
        tech_part_date = self.find_lot_row(info_block, 'Дата продления Технической части:')
        if not tech_part_date:
            tech_part_date = self.find_lot_row(info_block, 'Дата принятия Технической части:')
        return self.get_first(tech_part_date)

    def get_commercial_part_date_for_status(self, info_block):
        commercial_part_date = self.find_lot_row(info_block, 'Дата продления Коммерческой части:')
        if not commercial_part_date:
            commercial_part_date = self.find_lot_row(info_block, 'Дата принятия Коммерческой части:')
        return self.get_first(commercial_part_date)

    def get_tender_status(self, info_block):
        tech_part_date = self.get_tech_part_date_for_status(info_block)
        commercial_date = self.get_commercial_part_date_for_status(info_block)
        utc_tech_date = self.tools.get_utc_epoch(tech_part_date)
        utc_commercial_date = self.tools.get_utc_epoch(commercial_date)
        current_date = self.tools.get_utc()
        if utc_tech_date > current_date or utc_commercial_date > current_date:
            return 1
        else:
            return 3

    def get_tender_dop_info(self, info_block, search_info=None):
        info_list = self.find_lot_row(info_block, 'Дополнительная информация:')
        if not info_list:
            return None
        for i, text in enumerate(info_list):
            if '\n3.' in text:
                if search_info == 'dop':
                    return ''.join(info_list[i:]).replace('\n', '').replace('\xa0', '')
                elif search_info == 'order':
                    return ''.join(info_list[:i]).replace('\n', '').replace('\xa0', '')

    def get_fio_phone_email(self, info_list):
        contacts_list = []
        name_lst = re.findall(r'[А-Я][а-я]+\s[А-Я][а-я]+\s[А-Я][а-я]+', info_list[0])
        phone_lst = re.findall(r'\d\d-\d\d-\d\d', info_list[1])
        email_lst = re.findall(r'[^@,]+@evraz.com', info_list[2])
        for i, name in enumerate(name_lst):
            contacts_list.append(
                (name, '(3843) ' + phone_lst[i] if phone_lst else None, email_lst[i] if email_lst else None)
            )
        return contacts_list

    def get_contacts(self, info_block):
        contacts = []
        info_list_cvp = self.find_lot_row(info_block, 'Специалист ЦВП:')
        info_list_tender_init = self.find_lot_row(info_block, 'Инициатор:')
        if info_list_cvp:
            contacts.extend(self.get_fio_phone_email(info_list_cvp))
        if info_list_tender_init:
            contacts.extend(self.get_fio_phone_email(info_list_tender_init))
        return contacts

    def get_tender_number(self, text):
        number = re.search(r'Лот[^.]+', text)
        if number:
            return number.group(0).replace('Лот', '').strip()

    def get_tender_attachments(self, info_block):
        doc_url = self.find_lot_row(info_block, 'Техническая документация к лоту:')
        if doc_url:
            display_name = re.search(r'^[^.]+', doc_url.find('a').text)
            if display_name:
                display_name = display_name.group(0)
            name = re.search(r'[^/.]+$', doc_url.find('a').attrs['href'])
            if name:
                name = name.group(0)
            url = self.base_url + doc_url.find('a').attrs['href']
            return display_name, name, url

    def get_first(self, data_list):
        return data_list[0] if data_list else None

    def get_tender_id_from_url(self, url):
        tender_id = re.search(r'\d+$', url)
        if tender_id:
            return tender_id.group(0)

    def get_tender_lots_data(self, data_html, url):
        info_block = data_html.find_all('div', class_='text-block')[-1]
        lot = {
            'id': self.get_tender_id_from_url(url) + '_1',
            'number': self.get_tender_number(data_html.find('li', class_='active').text),
            'name': data_html.find('div', class_='info-lot').find('p').text,
            'status': self.get_tender_status(info_block),
            'customer': 'АО «ЕВРАЗ ЗСМК»',
            'region': 42,
            'dop_info': self.get_tender_dop_info(info_block, 'dop'),
            'tender_process_start': self.get_first(self.find_lot_row(info_block, 'Дата начала работ:')),
            'tender_process_end': self.get_first(self.find_lot_row(info_block, 'Дата окончания работ:')),
            'tech_part_date': self.get_first(self.find_lot_row(info_block, 'Дата принятия Технической части:')),
            'extend_tech_part_date': self.get_first(self.find_lot_row(info_block, 'Дата продления Технической части:')),
            'commercial_part_date': self.get_first(self.find_lot_row(info_block, 'Дата принятия Коммерческой части:')),
            'extend_commercial_part_date': self.get_first(
                self.find_lot_row(info_block, 'Дата продления Коммерческой части:')
            ),
            'sending_order': self.get_tender_dop_info(info_block, 'order'),
            'contacts': self.get_contacts(info_block),
            'publication_date': self.get_first(self.find_lot_row(info_block, 'Дата публикации:')),
            'link': url,
            'attachments': self.get_tender_attachments(info_block)
        }
        return lot