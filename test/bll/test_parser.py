import unittest

from src.bll.parser import Parser
from bs4 import BeautifulSoup


class Unittest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(base_url='')
        self.path_tender_list = 'test/files/tenders_list.html'

    def test_get_part_data(self):
        with open(self.path_tender_list) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        html_items_list = html.find(
            'div', {'class': 'newsWrapper'}).find('div', {'class': 'row'}).find_all('div', {'class': 'newsItem'})
        self.assertEqual(10, len(html_items_list))
        result = self.parser.get_part_data(html_items_list)
        self.assertEqual(3, len(result))
        true_result = {
            'sub_start_date': 1535709600000, 'bidding_date': 1535983200000,
            'scoring_place': '620012, г. Екатеринбург, пл. Первой пятилетки', 'region': 66,
            'email': 'M.Plyushch@uralmash.ru', 'fio': 'Плющ Марина Александровна',
            'subject': 'Транспортно-экспедиционные услуги по доставке груза ПАО Уралмашзавод по маршруту г. Санкт-Петербург, Колпино, – г. Екатеринбург',
            'phone': '+7 (343) 327-59-74', 'publication_date': 1535328000000, 'status': 3,
            'name': 'Транспортно-экспедиционные услуги по доставке груза ПАО Уралмашзавод по маршруту г. Санкт-Петербург, Колпино, – г. Екатеринбург',
            'customer': 'ПАО Уралмашзавод', 'type': 'Запрос ценовых котировок', 'id': 'УМ62465995',
            'currency': 'Российский рубль', 'sub_close_date': 1535709600000
        }
        self.assertEqual(true_result, result[0])


if __name__ == '__main__':
    unittest.main()
