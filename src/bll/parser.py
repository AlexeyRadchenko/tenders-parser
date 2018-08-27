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
            date = re.search(r'\d\d\d\d-\d\d-\d\d', date_str).group(0)
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

    def get_part_data(self, data_list):
        """парсим строки пришедшие в запросе возвращаем список первичных данных"""
        item_list = []
        for item_data in data_list:
            item_list.append({
                'id': item_data['id'],
                'number': item_data['registry_number'],
                'name': item_data['title'],
                'link': '{}{}{}'.format(self.base_url, '/#com/procedure/view/procedure/', item_data['id']),
                'publication_date': self.clear_date_str(item_data['date_published2']),
                'type': item_data['procedure_type'],
                'price': item_data['total_price'],
                'org': item_data['full_name'],
                'currency': item_data['currency_name'],
            })
        return item_list

    @staticmethod
    def get_region_from_address(address_str):
        for key in REGION_MAP.keys():
            if key in address_str.lower():
                return REGION_MAP[key]

    @staticmethod
    def get_lot_postitions(positions):
        lot_positions = []
        for pos in positions:
            lot_positions.append({
                'name': pos['name'],
                'quantity': pos['quantity'],
                'trade_mark': pos['trademark'],
                'units_symbol': pos['okei_symbol'],
                'okdp?': pos['category_code'],
            })
        return lot_positions

    def get_tender_lots_data(self, tender_data_dict):
        lots = []
        for num, lot in enumerate(tender_data_dict['lots'], start=1):
            lots.append({
                'number': num,
                'name': lot['subject'],
                'type': tender_data_dict['procedure_type_vocab'],
                'customers': [
                    {
                        'guid': None,
                        'name': customer['full_name'],
                        'region': self.get_region_from_address(customer['address'])
                    }
                    for customer in lot['lot_customers']
                ],
                'customers_inn_kpp_name_region': [
                    (
                        customer['inn'],
                        customer['kpp'],
                        customer['full_name'],
                        self.get_region_from_address(customer['address']),
                    ) for customer in lot['lot_customers']],
                'org_region': self.get_region_from_address(tender_data_dict['org_postal_address']),
                'sub_close_date': self.clear_date_str(lot['date_end_registration']),
                'scoring_date': self.clear_date_str(lot['date_end_second_parts_review']),
                'last_edit_date': self.clear_date_str(tender_data_dict['date_last_edited']),
                'price': lot['start_price'],
                'delivery_volume': ' '.join([delivery['quantity'] for delivery in lot['lot_delivery_places']]),
                'delivery_place': ' '.join([delivery['address'] for delivery in lot['lot_delivery_places']]),
                'delivery_datetime': ' '.join([delivery['req_dlv_date'] for delivery in lot['lot_delivery_places']]),
                'delivery_term': ' '.join([delivery['term'] for delivery in lot['lot_delivery_places']]),
                'delivery_basis': ' '.join([delivery['basis'] for delivery in lot['lot_delivery_places']]),
                'delivery_comment': ' '.join([delivery['comment'] for delivery in lot['lot_delivery_places']]),
                'org': tender_data_dict['org_full_name'],
                'org_address': tender_data_dict['org_postal_address'],
                'org_fio': tender_data_dict['organizer_user_full_name'],
                'org_phone': tender_data_dict['contact_phone'],
                'org_email': tender_data_dict['contact_email'],
                'positions': self.get_lot_postitions(lot['lot_units']),
                'attachments': [{
                        'displayName': file['descr'],
                        'realName': file['name'],
                        'size': file['size'],
                        'publicationDateTime': self.tools.get_utc_epoch(self.clear_date_str(file['date'])[0]),
                        'href': '{}{}'.format(self.base_url, file['link'])
                    }
                    for file in tender_data_dict['common_files']
                ],
                'status': lot['lot_step'],
                'currency': lot['currency_vocab']
            })
        return lots
