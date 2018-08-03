import unittest

from src.bll.parser import Parser
from bs4 import BeautifulSoup


class Unittest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(base_url='')
        self.path_tender_list = '../files/tender_list.html'
        self.path_tender_data = '../files/tender_data.html'

    def test_get_part_data(self):
        with open(self.path_tender_list) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        html_items_list = html.find(
            'div', {'data-view': 'full'}).find_all('a')
        self.assertEqual(15, len(html_items_list))
        result = self.parser.get_part_data(html_items_list)
        #print(result)
        self.assertEqual(6, len(result))
        true_result = {
            'number': 'ГП831218',
            'name': 'Оборудование  диспетчеризации для асд (согласно тз) ', 
            'price': None, 
            'sub_close_date': '02.08.20 06:00', 
            'type': 'Попозиционные торги', 
            'link': 'https://etpgpb.ru/procedure/tender/etp/168292-oborudovanie-dispetcherizatsii-dlya-asd-soglasno-tz/'
        }
        self.assertEqual(true_result, result[0])

    def test_get_tender_lots_data(self):
        with open(self.path_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        result = self.parser.get_tender_lots_data(html)
        #print(result)
        self.assertEqual(1, len(result))
        true_result = [{
            'status': 'Прием заявок на участие', 
            'scoring_date': '03.09.20 23:00', 
            'trade_date': '03.09.20 09:00', 
            'positions': [{'name': '"Производство мебели для офисов и предприятий торговли"', 'quantity': '35'}], 
            'sub_close_date': '20.08.20 10:00', 
            'name': None, 
            'currency': 'RUB', 
            'customer': 'ПАО "НПО "Стрела"', 
            'guarantee_app': None, 
            'publication_date': '27.07.20 16:04', 
            'number': 1, 'okpd2': ['31.01.11 Мебель металлическая для офисов'], 
            'delivery_place': '300002, г. Тула, ул. Арсенальная, д.2.', 
            'order_view_date': None, 
            'scoring_datetime': '03.09.20 23:00', 
            'price': None, 
            'payment_terms': None, 
            'quantity': '35 шт.\n (в соответствии с техническим заданием и проектом Договора)'
        }]
        self.assertEqual(true_result, result)

    def test_get_attachments(self):
        with open(self.path_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        result = self.parser.get_attachments(html)
        #print(result)
        self.assertEqual(6, len(result))
        true_result = {
            'display_name': 'ТЗ',
            'publication_date': '27.07.2018', 
            'real_name': 'ТЗ.pdf', 
            'url': 'https://etp.gpb.ru/file/get/t/LotDocuments/id/548277/name/5b5b14624eb171.61672601'
        }
        self.assertEqual(true_result, result[0])

    def test_get_org_data(self):
        with open(self.path_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        result = self.parser.get_org_data(html)
        #print(result)
        true_result = {
            'phone': '7-472-393782', 
            'name': 'Публичное акционерное общество "Научно-производственное объединение "Стрела"', 
            'place': 'Тула', 
            'address': '300002, Российская Федерация, Тульская область, Тула, М. Горького, 6', 
            'fax': '7-4872-341104', 
            'fio': 'Минайлова Светлана Николаевна', 
            'email': 'zakupki@npostrela.net', 
            'region': 71
        }
        self.assertEqual(true_result, result)


if __name__ == '__main__':
    unittest.main()
