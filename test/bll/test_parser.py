import unittest

from src.bll.parser import Parser
import json


class Unittest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(base_url='')
        self.path_tender_list = 'test/files/tender_list.json'

    def test_get_part_data(self):
        with open(self.path_tender_list) as data_file:
            data = json.load(data_file)
        self.assertEqual(2, len(data['data']))
        result = self.parser.get_part_data(data['data'])
        del result[0]['publication_date']
        del result[0]['attachments'][0]['publicationDateTime']
        true_result = {
            'id': 'd64e9bb0269eb876777f89ba401e29e6',
            'status': 3,
            'customer': 'ДПиУТМП',
            'region': None,
            'customer_address': '123100, г. Москва, 1-й Красногвардейский проезд, д.15',
            'name': 'Выполнение работ по тиражированию и развитию системы взаимодействия с поставщиками SAP SRМ',
            'attachments': [
                {'href': '/upload/iblock/d11/K-Priglasheniyu.rar',
                 'size': None,
                 'realName': 'K-Priglasheniyu.rar',
                 'displayName': 'Выполнение работ по тиражированию и развитию системы взаимодействия с поставщиками SAP SRМ'}
            ],
            'email': 'ootp@nirnik.ru',
            'type': 'Запрос предложений',
            'sub_close_date': 1535662800000,
            'submit_type': 'В Системе управления закупками SRM Норникель',
            'phone': '+7(495)787-76-67 доб.5280'
        }
        self.assertEqual(true_result, result[0])


if __name__ == '__main__':
    unittest.main()
