import unittest

from src.bll.parser import Parser
from bs4 import BeautifulSoup


class Unittest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(base_url='')
        self.path_tender_list = 'test/files_2/tenders_list.html'

    def test_get_part_data(self):
        with open(self.path_tender_list) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        html_items_list = html.find('div', {'data-id': 'tab-1'}).find_all('div', {'class': 'tenders-item'})
        self.assertEqual(10, len(html_items_list))
        result = self.parser.get_part_data(html_items_list, 0, 'http://www.uralchem.ru/purchase/tenders/', 'PAGEN_1', 1)
        self.assertEqual(10, len(result))
        #print(result[0])
        true_result = {
            'name': 'Уведомление\n о проведении конкурентной процедуры в форме запроса предложений с целью\n заключения договора на разработку рабочей документации на ремонт здания\n отделения сложных минеральных удобрения цеха аммофоса №2 по Заключению №\n А-ЗС-64747-17 АО «Воскресенские минеральные удобрения»',
            'link': 'http://www.uralchem.ru/purchase/tenders/?PAGEN_1=1',
            'customer': '“АО ХК Уралхим”',
            'status': 1,
            'org': 'АО «Воскресенские минеральные удобрения»',
            'publication_date': ('25.09.2018 09:30:00', None),
            'sub_close_date': '18.10.2018 17:30:00',
            'attachments': [{
                'publication_date': ('25.09.2018 09:30:00', None),
                'url': 'http://www.uralchem.ru/upload/iblock/0da/278_18-ot-25.09.2018-Uvedomlenie-o-provedenie-UKP-razrabotka-rabochey-dokumentatsii-na-remont-zdaniya-OSMU-tsekha-amm_2.pdf',
                'real_name': '278_18-ot-25.09.2018-Uvedomlenie-o-provedenie-UKP-razrabotka-rabochey-dokumentatsii-na-remont-zdaniya-OSMU-tsekha-amm_2.pdf',
                'display_name': '278_18-ot-25.09.2018-Uvedomlenie-o-provedenie-UKP-razrabotka-rabochey-dokumentatsii-na-remont-zdaniya-OSMU-tsekha-amm_2'
            }],
            'number': 'УХ72135676',
            'id': 'УХ72135676_1'
        }
        self.assertEqual(true_result, result[0])

    def test_get_attachments(self):
        with open(self.path_tender_list) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        html_items_list = html.find('div', {'data-id': 'tab-1'}).find_all('div', {'class': 'tenders-item'})
        result = self.parser.get_attachments(html_items_list[0])
        #print(result)
        self.assertEqual(1, len(result))
        true_result = [{
            'publication_date': ('25.09.2018 09:30:00', None),
            'url': 'http://www.uralchem.ru/upload/iblock/0da/278_18-ot-25.09.2018-Uvedomlenie-o-provedenie-UKP-razrabotka-rabochey-dokumentatsii-na-remont-zdaniya-OSMU-tsekha-amm_2.pdf',
            'real_name': '278_18-ot-25.09.2018-Uvedomlenie-o-provedenie-UKP-razrabotka-rabochey-dokumentatsii-na-remont-zdaniya-OSMU-tsekha-amm_2.pdf',
            'display_name': '278_18-ot-25.09.2018-Uvedomlenie-o-provedenie-UKP-razrabotka-rabochey-dokumentatsii-na-remont-zdaniya-OSMU-tsekha-amm_2'
        }]
        self.assertEqual(true_result, result)


if __name__ == '__main__':
    unittest.main()