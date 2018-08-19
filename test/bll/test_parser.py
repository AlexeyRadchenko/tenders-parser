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
        next_page_exist = html.find('ul', {'class': 'pagination'})
        self.assertEqual(True, bool(next_page_exist))
        html_items_list = html.find('div', {'id': 'listOutBuyTender'}).find_all('article')
        self.assertEqual(10, len(html_items_list))
        result = self.parser.get_part_data(html_items_list)
        self.assertEqual(10, len(result))
        true_result = {
            'type': 'Отбор',
            'id': '8977',
            'link': 'http://zakupki.gazprom-neft.ru/tenderix/view.php?ID=8977',
            'number': '3-38015-306-18',
            'target_place': 'г. Владивосток',
            'status': 'Объявлен',
            'name': 'Отбор организации, способной оказать услуги по приёму, \nответственному хранению и последующей доставке получателям в \nДальневосточный федеральный округ нефтепродуктов (техническое масло).',
            'customer': 'ООО «Газпромнефть-СМ»'
        }
        self.assertEqual(true_result, result[0])

    def test_get_tender_lots_data(self):
        with open(self.path_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        result = self.parser.get_tender_lots_data(html)
        self.assertEqual(1, len(result))
        true_result = [{
            'processing_time': None,
            'sub_start_date': ('20.08.2018 10:00', None),
            'info_msg': None,
            'sub_close_date': ('03.09.2018 13:00', None),
            'order_view_date': ('03.09.2018 16:00', None),
            'number': 1,
            'publication_date': ('20.08.2018 10:00', None),
            'volume': None,
            'lot_subject': None,
            'name': None
        }]
        self.assertEqual(true_result, result)

    def test_get_org_data(self):
        with open(self.path_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        result = self.parser.get_org_data(html)
        true_result = {
            'email': 'tenderSM_KK@gazprom-neft.ru',
            'name': 'ООО «Газпромнефть-СМ»',
            'phone': '+7 (495) 642-99-69доб. 1479',
            'region': 77
        }
        self.assertEqual(true_result, result)

    def test_get_attachments(self):
        with open(self.path_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        result = self.parser.get_attachments(html)
        self.assertEqual(2, len(result))
        true_result = {
            'real_name': 'Информационное письмо по отбору.pdf',
            'size': '519.68 КБ',
            'url': 'http://zakupki.gazprom-neft.ru/tenderix/auth/?backurl=%2Ftenderix%2Fview.php%3FID%3D8977%23files',
            'display_name': 'Информационное письмо по отбору.pdf',
            'publication_date': ('20.08.2018 10:00', None)
        }
        self.assertEqual(true_result, result[0])


if __name__ == '__main__':
    unittest.main()
