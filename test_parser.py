import unittest

from src.bll.parser import Parser
from bs4 import BeautifulSoup
import json


class Unittest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(base_url='https://zakupki.tmk-group.com')
        self.path_tender_list = 'test/files/tender_list.json'
        self.path_tender_data = 'test/files/tender_data.json'

    def test_get_part_data(self):
        with open(self.path_tender_list) as data_file:
            data = json.load(data_file)
        result = self.parser.get_part_data(data['result']['procedures'])
        self.assertEqual(25, len(result))
        true_result = {
            'currency': 'RUB',
            'price': '0.00',
            'type': 17,
            'number': 'COM27081800052',
            'publication_date': ('2018-08-27 16:09', 3),
            'id': 17901,
            'link': 'https://zakupki.tmk-group.com/#com/procedure/view/procedure/17901',
            'name': 'Закупка пасты очищающей и крема защитного для рук, только для поставщиков, '
                    'имеющих положительные акты испытаний на АО "ВТЗ".',
            'org': 'АО "ВТЗ"'
        }
        self.assertEqual(true_result, result[0])

    def test_get_tender_lots_data(self):
        with open(self.path_tender_data) as data_file:
            data = json.load(data_file)
        result = self.parser.get_tender_lots_data(data['result']['procedure'])
        self.assertEqual(1, len(result))
        true_result = [{
            'delivery_term': 'оплата после поставки материалов в течение 90 дней с даты получения'
                             ' счета-фактуры установленного образца',
            'last_edit_date': ('2018-04-20 06:47', 3),
            'delivery_comment': 'Наличие сертификатов качества предлагаемой продукции и документов,'
                                ' подтверждающих статус изготовителя либо официального дилера изготовителя обязательно'
                                ' (прикрепить к процедуре).\nВ коммерческом предложении прошу указывать СИЗы, '
                                'образцы которых были предоставлены на ПАО «СинТЗ» для проведения испытаний и по ним'
                                ' имеются положительные заключения – акты (КП и акты прикрепить к процедуре).\n',
            'customers': [{'region': 66, 'name': 'Публичное акционерное общество «Синарский трубный завод»',
                           'guid': None}],
            'org_phone': '7-3439-363935',
            'positions': [
                {
                    'okdp?': '3100.119100',
                    'name': '000000001600004290 Респиратор FFP1 до 4ПДК чашка б/клапана',
                    'units_symbol': 'ШТ',
                    'trade_mark': '',
                    'quantity': '50'
                },
                {
                    'okdp?': '3100.119100',
                    'name': '000000001600004291 Респиратор FFP1 до 4ПДК складной б/клап',
                    'units_symbol': 'ШТ',
                    'trade_mark': '',
                    'quantity': '160'
                },
                {
                    'okdp?': '3100.119100',
                    'name': '000000001600004292 Респиратор FFP1 до 4ПДК складной с клап',
                    'units_symbol': 'ШТ',
                    'trade_mark': '',
                    'quantity': '2795'
                },
                {
                    'okdp?': '3100.119100',
                    'name': '000000001600004294 Респиратор FFP3 до 50ПДК складной с клап',
                    'units_symbol': 'ШТ',
                    'trade_mark': '',
                    'quantity': '609'
                },
                {
                    'okdp?': '3100.119100',
                    'name': '000000001600004295 Респиратор FFP2 до 12ПДК складной с клап',
                    'units_symbol': 'ШТ',
                    'trade_mark': '',
                    'quantity': '50'
                },
                {
                    'okdp?': '3100.119100',
                    'name': '000000001600004492 Респиратор FFP2 до 12 ПДК чашка с клап.',
                    'units_symbol': 'ШТ',
                    'trade_mark': '',
                    'quantity': '200'
                }
            ],
            'org': 'Публичное акционерное общество «Синарский трубный завод»',
            'status': 'completed',
            'delivery_datetime': ' до 20.05.2018г',
            'customers_inn_kpp_name_region': [
                ('6612000551', None, 'Публичное акционерное общество «Синарский трубный завод»', 66)
            ],
            'delivery_basis': 'DAP',
            'org_region': 66,
            'org_fio': 'Нафикова  М. Н.',
            'currency': 'Российский рубль',
            'number': 1,
            'price': '92489.08',
            'scoring_date': ('2018-04-23 21:59', 3),
            'type': 'Попозиционный запрос предложений',
            'sub_close_date': ('2018-04-23 09:00', 3),
            'delivery_volume': '100%',
            'org_address': '623401, Российская Федерация, Свердловская область, г. Каменск-Уральский,'
                           ' ул. Заводской проезд, д. 1',
            'name': 'Закупка СИЗОД',
            'attachments': [{
                'size': 16028,
                'publicationDateTime': 1523942880000,
                'displayName': 'Информация о лоте процедуры',
                'realName': 'Шаблон_файла_для_импорта_лота_респираторы_новый.xlsx',
                'href': 'https://zakupki.tmk-group.com/file/get/t/LotDocuments/id/8542/name/'
                        '%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD_%D1%84%D0%B0%D0%B9%D0%BB%D0%B0_%D0%B4%D0%BB%D1%8F_%D0%B8%D0%BC%D0%BF%D0%BE%D1%80%D1%82%D0%B0_%D0%BB%D0%BE%D1%82%D0%B0_%D1%80%D0%B5%D1%81%D0%BF%D0%B8%D1%80%D0%B0%D1%82%D0%BE%D1%80%D1%8B_%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9.xlsx'
            }],
            'org_email': 'NafikovaMN@sintz.ru',
            'delivery_place': 'склад ПАО «СинТЗ»'
        }]
        self.assertEqual(true_result, result)


if __name__ == '__main__':
    unittest.main()
