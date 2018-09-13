import unittest

from src.bll.parser import Parser
from bs4 import BeautifulSoup


class Unittest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(base_url='http://supply.evraz.com')
        self.path_tender_list = '../files/tender_list.html'
        self.path_tender_data = '../files/tender_data.html'
        self.source_url = 'http://supply.evraz.com'

    def test_get_part_data(self):
        with open(self.path_tender_list) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        items_div_list = html.find_all('div', {'class': 'panel-body'})
        result_url_list = []
        for div in items_div_list:
            links = div.find_all('a')
            result_url_list.extend([self.source_url + url.attrs['url'] for url in links])
        self.assertEqual(71, len(result_url_list))
        true_result = 'http://supply.evraz.com/lot/?ID=227689'
        self.assertEqual(true_result, result_url_list[4])

    def test_get_tender_lots_data(self):
        with open(self.path_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
            result = self.parser.get_tender_lots_data(html, 'http://supply.evraz.com/?IDLot=226646')
        self.assertEqual(16, len(result))
        true_result = {
            'customer': 'АО «ЕВРАЗ ЗСМК»',
            'attachments': ('410.7z', '410.7z', 'http://supply.evraz.comhttp://supply.evraz.com/upload/iblock/a0a/410.7z'),
            'tender_process_start': '01.05.2018',
            'name': 'Склад импортного оборудования. Помещения в здании УПУ \nинв.№240000000003-00.  Космическое шоссе 16 корпус 88: Полигон \nавтопогрузчиков',
            'tech_part_date': '29.09.2018 17:00:00',
            'commercial_part_date': '30.09.2018 17:00:00',
            'link': 'http://supply.evraz.com/?IDLot=226646',
            'dop_info': '3. Для участия в выборной процедуре по закупке работ/услуг Вам необходимо пройти предквалификацию. Участник не прошедший предквалификацию к выборным процедурам не допускается. По вопросу прохождения предквалификации обращаться по тел. 59-45-10. Вся информация касаемо предквалификации расположена по ссылке: http://supply.evraz.com',
            'region': 42,
            'contacts': ('Медведев Дмитрий Герардович', '59-48-59', 'Dmitry.Medvedev@evraz.com'),
            'tender_process_end': '20.05.2018',
            'number': '18/410-5',
            'status': 1,
            'id': '226646_1',
            'sending_order': '1. Техническая часть предоставляется Специалисту ЦВП по электронной почте (эл. адрес указан в заказе)2. Коммерческая часть предоставляется в закрытом конверте вздание «УЗРС» АО «ЕВРАЗ ЗСМК» каб.№319. Иногородним организациям отправку конверта осуществлять по почте на следующий адрес: 654043, Россия, Кемеровская обл., г. Новокузнецк, ш. Космическое 16. При оформлении конверта учесть следующие требования:На лицевой стороне конверта необходимо указать - от кого, предмет работ (в соответствии с предметом работ, который указан на сайте АО «ЕВРАЗ ЗСМК»)и номер работы. На обратной стороне конверта в местах его склеивания обязательно поставить печать, расписаться руководителю и указать дату. ',
            'publication_date': '12.04.2018'
        }
        self.assertEqual(true_result, result)

    def test_get_tender_attachments(self):
        with open(self.path_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        result = self.parser.get_tender_attachments(html.find_all('div', class_='text-block')[-1])
        self.assertEqual(3, len(result))
        true_result = ('410.7z',
                       '410.7z',
                       'http://supply.evraz.comhttp://supply.evraz.com/upload/iblock/a0a/410.7z'
                       )
        self.assertEqual(true_result, result)

    def test_get_fio_phone_email(self):
        with open(self.path_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        result = self.parser.get_fio_phone_email(html.find_all('div', class_='text-block')[-1])
        true_result = (
            'Медведев Дмитрий Герардович',
            '59-48-59',
            'Dmitry.Medvedev@evraz.com'
        )
        self.assertEqual(true_result, result)


if __name__ == '__main__':
    unittest.main()