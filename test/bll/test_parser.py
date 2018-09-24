import unittest

from src.bll.parser import Parser
from bs4 import BeautifulSoup


class Unittest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(base_url='')
        self.path_after_active_tender_list = '../files/after_active_tender_list.html'
        self.path_after_active_tender_data = '../files/after_active_tender_data.html'
        self.path_after_arc_tender_list = '../files/after_arc_tender_list.html'
        self.path_before_active_tender_list = '../files/before_active_tender_list.html'
        self.path_before_arc_tender_list = '../files/before_arc_tender_list.html'

    def test_get_part_data(self):
        with open(self.path_after_active_tender_list) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        html_items_list = html.find('table', {'class': 'lot_list'}).find_all('a')
        item_list = [item.attrs['href'] for item in html_items_list]
        self.assertEqual(99, len(item_list))
        result = item_list[10]
        #print(result)
        true_result = 'https://tenders.irkutskoil.ru/tender/lot_2375.php'
        self.assertEqual(true_result, result)

    def test_get_active_after_tender_data(self):
        with open(self.path_after_active_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        result = self.parser.get_active_after_tender_data(html, 'https://tenders.irkutskoil.ru/tender/lot_2383.php')
        #print(result)
        true_result = {
            'link': 'https://tenders.irkutskoil.ru/tender/lot_2383.php',
            'name': 'Запасные части к турбокомпрессорному оборудованию ATLAS COPCO и компрессору Quincy GDP-37LT',
            'attachments': [{'size': None, 'url': 'https://tenders.irkutskoil.ru/tender/lotfile/lotinvite_2383.docx',
              'publication_date': ('19.09.2018 17:42', 8), 'display_name': 'Извещение',
              'real_name': 'lotinvite_2383'},
             {'size': None, 'url': 'https://tenders.irkutskoil.ru/tender/lotfile/lotoffer_2383.xlsx',
              'publication_date': ('19.09.2018 17:42', 8),
              'display_name': 'Форма коммерческого предложения', 'real_name': 'lotoffer_2383'},
             {'size': None, 'url': 'https://tenders.irkutskoil.ru/tender/lotfile/lot2383_doc1.pdf',
              'publication_date': ('19.09.2018 17:42', 8),
              'display_name': 'Инструкция. Упаковка_ маркировка материалов_ оборудования и запасных частей',
              'real_name': 'lot2383_doc1'},
             {'size': None, 'url': 'https://tenders.irkutskoil.ru/tender/lotfile/lot2383_doc2.xls',
              'publication_date': ('19.09.2018 17:42', 8), 'display_name': 'форма заявки',
              'real_name': 'lot2383_doc2'},
             {'size': None, 'url': 'https://tenders.irkutskoil.ru/tender/lotfile/lot2383_doc3.docx',
              'publication_date': ('19.09.2018 17:42', 8), 'display_name': 'договор ИНК',
              'real_name': 'lot2383_doc3'},
             {'size': None, 'url': 'https://tenders.irkutskoil.ru/tender/lotfile/lot2383_doc4.docx',
              'publication_date': ('19.09.2018 17:42', 8), 'display_name': 'договор ООО _ИНК-СЕРВИС_',
              'real_name': 'lot2383_doc4'}], 'customer': 'ООО "Иркутская нефтяная компания"',
             'status': 1,
             'number': 'ДС-1130-18',
             'sub_start_date': ('19.09.2018 17:42', 8),
             'sub_close_date': ('02.10.2018 23:59', 8),
             'region': 38, 'id': 'ДС-1130-18_1'
        }

        self.assertEqual(true_result, result)

    def test_get_arc_after_tender_list(self):
        with open(self.path_after_arc_tender_list) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        items_html = html.find('table', {'class': 'lot_list'})
        result = self.parser.get_arc_after_tender_list(items_html)
        #print(result[0])
        self.assertEqual(20, len(result))
        true_result = {
            'number': 'Т-161-18',
            'status': 4,
            'data_type': 'arc_after',
            'id': 'Т-161-18_1',
            'end_date': '19.09.2018 15:27, (Иркутск) GMT +08:00',
            'name': 'Выполнение реконструкции действующей ВЛ 35кВ УКПГ-ДНС-УПН (СМР, ПНР, поставка материалов)',
            'winner': None
        }
        self.assertEqual(true_result, result[0])

    def test_get_active_before_tender_list_with_active(self):
        with open(self.path_before_active_tender_list) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        items_html = html.find('div', {'class': 'tenders'})
        result = self.parser.get_arc_before_tender_list(items_html)
        self.assertEqual(1, len(result))
        #print(result)
        true_result = {
            'name': 'Выполнение \nстроительства "под ключ" (СМР, ПНР) объекта: "Компрессорная станция для \nтранспорта и закачки в пласт сухого-отбензиненного газа на Марковском \nнефтегазоконденсатном месторождении"',
            'number': 'Т-470-17',
            'winner': '30-11-2017',
            'data_type': 'arc_before',
            'status': 4,
            'id': 'Т-470-17_1',
            'customer': 'ООО "Иркутская нефтяная компания"',
            'end_date': '17.07.2017'
        }
        self.assertEqual(true_result, result[0])

    def test_get_arc_before_tender_list_with_arc(self):
        with open(self.path_before_arc_tender_list) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        items_html = html.find('div', {'class': 'tenders'})
        result = self.parser.get_arc_before_tender_list(items_html)
        self.assertEqual(10, len(result))
        #print(result[5])
        true_result = {
            'status': 3,
            'end_date': '24.08.2017',
            'id': 'Т-246-17_1',
            'data_type': 'arc_before',
            'customer': 'ООО "Иркутская нефтяная компания"',
            'name': 'РВД, фитинги к РВД',
            'winner': 'ООО "СИБИРСКИЕ ТЕХНОЛОГИИ"; ЗАО "Энерпром-Гидропривод"; ООО "ТК "Каскад"; ',
            'number': 'Т-246-17'
        }
        self.assertEqual(true_result, result[5])


if __name__ == '__main__':
    unittest.main()
