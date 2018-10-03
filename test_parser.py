import unittest

from src.bll.parser import Parser
from bs4 import BeautifulSoup


class Unittest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(base_url='')
        self.path_tender_list = 'test/files/tenders_list.html'
        self.path_zp_tender_data = 'test/files/zp_tender_data.html'
        self.path_tn_tender_data = 'test/files/tn_tender_data.html'
        self.path_rd_tender_data = 'test/files/rd_tender_data.html'

    def test_get_part_data(self):
        with open(self.path_tender_list) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        html_items_list = html.find('table', {'class': 'a-IRR-table'}).find_all('tr')[1:]
        self.assertEqual(15, len(html_items_list))
        result = self.parser.get_part_data(html_items_list)
        #print(result)
        self.assertEqual(15, len(result))
        true_result = {
            'price': None, 
            'status': 'Опубликован', 
            'id': 'ЗП-181001-89_1', 
            'customer': '333ООО "ТаграС-РемСервис"', 
            'sub_close_date': '08.10.2018 15:00', 
            'currency': 'руб.', 
            'publication_date': '01.10.2018 11:54', 
            'link': '/pls/tzp/https://etp.tatneft.ru/pls/tzp/f?p=220:2155:17126238532881::::P2155_REQ_ID,P2155_PREV_PAGE:2094282300021,562', 
            'number': 'ЗП-181001-89', 
            'sub_start_date': '', 
            'name': 'Поставка  насоса гидравлического для выполнения процессов ГРП с рабочим давлением 20 000 psi  (2013/13)'
            }

        self.assertEqual(true_result, result[0])

    def test_get_tender_data_zp(self):
        with open(self.path_zp_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        html_data = html.find('table', {'id': 'main'})
        result = self.parser.get_tender_data(
            html_data, {'id':'ЗП-181001-123_1', 'number': 'ЗП-181001-123', 'price': None})
        #print(result)
        self.assertEqual(17, len(result))
        true_result = {
            'delivery_terms': 'Срок\n поставки:в течении 8 рабочих дней с момента подписания договора, \nдоставка осуществляется силами и за счет Поставщика.Товар доставляется \nПокупателю в место назначения, указанный в договоре, очищенный от всех \nпошлин и рисков.', 
            'publication_date': ('01.10.2018 15:22', None), 
            'fio': 'Галимов Ф. С.', 
            'positions': [
                {'num': '1', 
                'measure': 'шт.', 
                'notice': 'Согласно спецификации', 
                'name': 'Насос вставной 25-175 RHBC 14-4-2-2', 
                'quantity': '3'}, 
                {'num': '2', 
                'measure': 'шт.', 
                'notice': 'Согласно спецификации', 
                'name': 'Башмак якорный', 
                'quantity': '3'}], 
            'scoring_date': None, 
            'type': 'Запрос предложений', 
            'status': 'Опубликован, прием предложений', 
            'name': 'Поставка нефтепромыслового глубинно-насосного оборудования(359)', 
            'customer': 'ПАО "МАКойл", г. Нурлат', 
            'price': None, 
            'sub_order': ' - информация по заказу доступна всем пользователям  - к участию допускаются все зарегистрированные организации  - к участию автоматически допускаются все участники, подавшие заявки на участие  - допускаются специальные предложения (аналоги, замены)  - необходимо указать цены по всем позициям заказа', 
            'number': 'ЗП-181001-123', 
            'id': 'ЗП-181001-123_1', 
            'sub_close_date': ('04.10.2018 15:00', None), 
            'sub_start_date': ('01.10.2018 14:12', None), 
            'attachments': [
                {'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2094428860021&x02=87539780000&x03=87507700000', 
                'size': '596,99 KB', 
                'publication_date': ('01.10.2018 15:22', None), 
                'real_name': 'Приглашение.pdf', 
                'display_name': 'Приглашение'}, 
                {'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2094429040021&x02=87539780000&x03=87507700000', 
                'size': '165,55 KB', 
                'publication_date': ('01.10.2018 15:22', None), 
                'real_name': 'спецификация.pdf', 
                'display_name': 'спецификация'}, 
                {'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2094428780021&x02=87539780000&x03=87507700000', 
                'size': '473,1 KB', 
                'publication_date': ('01.10.2018 15:22', None), 
                'real_name': 'условие поставки.pdf', 
                'display_name': 'условие поставки'
                }], 
            'delivery_place': '423040, РТ, г. Нурлат, улица им.А.К.Самаренкина, д.8'
        }
        self.assertEqual(true_result, result)
    
    def test_get_tender_data_tn(self):
        with open(self.path_tn_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        html_data = html.find('table', {'id': 'main'})
        result = self.parser.get_tender_data(
            html_data, {'id':'ТН-181001-142_1', 'number': 'ТН-181001-142', 'price': None})
        #print(result)    
        self.assertEqual(17, len(result))
        true_result = {
            'delivery_terms': 'Срок\n поставки - 3 календарных дня (либо график поставки). Доставка за счёт \nпродавца. В случае необходимости Поставщик обязуется осуществлять \nсамодекларирование по исполнению договорных обязательств (Поставщик \nформирует основные вехи исполнения заказа, график контрольных сроков и \nпредоставляет информацию по его исполнению).', 
            'sub_order': ' - информация по заказу доступна всем пользователям  - к участию допускаются все зарегистрированные организации  - к участию автоматически допускаются все участники, подавшие заявки на участие  - допускаются специальные предложения (аналоги, замены)  - допускаются частичные предложения (по части позиций заказа)', 
            'scoring_date': None, 
            'customer': 'ООО "Гарант", г. Нижнекамск', 
            'sub_close_date': ('04.10.2018 15:00', None), 
            'type': 'Тендер', 
            'delivery_place': 'АО\n "ТАНЕКО", РФ, Республика Татарстан, г. Нижнекамск, Промзона Комплекс \nНПиНХЗ, Строительный городок, Установка получения элементарной серы.', 
            'attachments': [
                {'size': '356,65 KB', 
                'display_name': 'Приглашение', 
                'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2094531380021&x02=87539780000&x03=87507700000', 
                'real_name': 'Приглашение.jpg', 
                'publication_date': ('01.10.2018 16:13', None)
                }, 
                {'size': '17,08 KB', 
                'display_name': 'Спецификация.', 
                'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2094531680021&x02=87539780000&x03=87507700000', 
                'real_name': 'Спецификация.docx', 
                'publication_date': ('01.10.2018 16:13', None)
                }, 
                {'size': '415,35 KB', 
                'display_name': 'Условия поставки', 
                'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2094531770021&x02=87539780000&x03=87507700000', 
                'real_name': 'Условия поставки.jpg', 
                'publication_date': ('01.10.2018 16:13', None)
                }, 
                {'size': '19,52 KB', 
                'display_name': 'Анкета поставщика.', 
                'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2094531720021&x02=87539780000&x03=87507700000', 
                'real_name': 'Анкета поставщика.docx', 
                'publication_date': ('01.10.2018 16:13', None)}, 
                {'size': '35,5 KB', 
                'display_name': 'Гарантийное письмо', 
                'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2094531750021&x02=87539780000&x03=87507700000', 
                'real_name': 'Гарантийное письмо.doc', 
                'publication_date': ('01.10.2018 16:13', None)}, 
                {'size': '66,5 KB', 
                'display_name': 'Договор поставки', 
                'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2094531360021&x02=87539780000&x03=87507700000', 
                'real_name': 'Договор поставки.doc', 
                'publication_date': ('01.10.2018 16:13', None)
                }], 
            'publication_date': ('01.10.2018 16:13', None), 
            'status': 'Опубликован, прием предложений', 
            'positions': [
                {'measure': 'м2', 
                'quantity': '1', 
                'num': '1', 
                'name': 'Панель подвесная ARMSTRONG BAJKAL 90RH (Board-24мм) (600х600х12)', 
                'notice': '20шт/7,2м2'
                }, 
                {'measure': 'м2', 
                'quantity': '1', 
                'num': '2', 
                'name': 'Панель подвесная ARMSTRONG OASIS 90RH (Board-24мм) (600х600х12)', 
                'notice': '20шт/7,2м2'
                }, 
                {'measure': 'м2', 
                'quantity': '1', 
                'num': '3', 
                'name': 'Панель подвесная ARMSTRONG RETAIL 90RH (Board-24мм) (600х600х12)', 
                'notice': '20шт/7,2м2'
                }, 
                {'measure': 'м2', 
                'quantity': '1', 
                'num': '4', 
                'name': 'Панель подвесная ARMSTRONG SCALA (Board-24мм) (600х600х12)', 
                'notice': '20шт/7,2м2'
                }, 
                {'measure': 'уп.', 
                'quantity': '1', 
                'num': '5', 
                'name': 'Направляющая основная 3,6 GL Премиум 24мм h-33мм белый', 
                'notice': '20шт/уп'
                }, 
                {'measure': 'уп.', 
                'quantity': '1', 
                'num': '6', 
                'name': 'Планка 0,6 GL Премиум 24мм h-26мм белый', 
                'notice': '60шт/уп'
                }, 
                {'measure': 'уп.',
                 'quantity': '1', 
                 'num': '7', 
                 'name': 'Планка 1,2 GL Премиум 24мм h-26мм белый', 
                 'notice': '60шт/уп'
                 }, 
                 {'measure': 'уп.', 
                 'quantity': '1', 
                 'num': '8', 
                 'name': 'Плинтус GL 19х19 L=3м толщ.0,40мм белый стальной (45шт/135пм/уп) кромка Board', 
                 'notice': ''
                 },
                {'measure': 'уп.', 
                'quantity': '1', 
                'num': '9', 
                'name': 'Подвес (евро) GL 500мм, d=3,0мм, 2-х дырочный', 
                'notice': '100шт/уп'
                }, 
                {'measure': 'уп.', 
                'quantity': '1', 
                'num': '10', 
                'name': 'Анкер-клин потолочный 6х40 (100шт/уп)', 'notice': ''
                }, 
                {'measure': 'уп.', 
                'quantity': '1', 
                'num': '11', 
                'name': 'Дюбель с шурупом 6х40', 
                'notice': 'грибовидный борт, 200шт/кор'
                }
            ], 
            'number': 'ТН-181001-142', 
            'sub_start_date': ('01.10.2018 15:05', None), 
            'id': 'ТН-181001-142_1', 
            'price': None, 
            'name': 'Поставка подвесных панелей (для нужд АО "ТАНЕКО") (1054; 10871-ИсхП)', 
            'fio': 'Куликов(Подрядчик Танеко) А. И.'
        }
        self.assertEqual(true_result, result)
    
    def test_get_tender_data_rd(self):
        with open(self.path_rd_tender_data) as data_file:
            html = BeautifulSoup(data_file, 'lxml')
        html_data = html.find('table', {'id': 'main'})
        result = self.parser.get_tender_data(
            html_data, {'id':'РД-180925-7_1', 'number': 'РД-180925-7', 'price': 3232346.00})
        #print(result)
        self.assertEqual(17, len(result))
        true_result = {
            'delivery_place': 'Бугульминская\n база управления “Татнефтеснаб” ПАО «Татнефть» им. В.Д. Шашина, Почтовый\n адрес: РФ, Республика Татарстан, 423232, г. Бугульма, ул. Нефтяников, \nд. 33. телефон (8-85-594) 7-30-59, факс 7-29-60. Код ЕЛС 1003209020. Код\n грузополучателя 1215. Станция назначения: Бугульма, Куйбышевской ж/д \nдля всех видов отправок. Код станции 648607. ОКПО 00136352.', 
            'positions': [
                {'num': '1', 
                 'notice': 'Трубы по ГОСТ 550-75 из стали 15Х5М \nдолжны соответствовать требованиям: 1.Партия должна состоять из труб \nодной плавки и иметь единый документ о качестве с указанием химического \nсостава и сведений о термообработке.  2. Группа «А». 3.Термообработка. \n4. Гидроиспытание. 5. Контроль неразрушающими методами (рентген или УЗД)\n по всей поверхности. 6. Испытание на загиб и раздачу. 7.Испытание на \nсплющивание для труб.',
                 'quantity': '1925',
                 'name': 'Труба 25х2,5х12500 ст.15Х5М ГОСТ 550-75',
                 'measure': 'м'
                }, 
                {'num': '2', 
                 'notice': 'Трубы по ГОСТ 550-75 из стали 15Х5М \nдолжны соответствовать требованиям: 1.Партия должна состоять из труб \nодной плавки и иметь единый документ о качестве с указанием химического \nсостава и сведений о термообработке.  2. Группа «А». 3.Термообработка. \n4. Гидроиспытание. 5. Контроль неразрушающими методами (рентген или УЗД)\n по всей поверхности. 6. Испытание на загиб и раздачу. 7.Испытание на \nсплющивание для труб.',
                 'quantity': '3081',
                 'name': 'Труба 25х2,5х13000 ст.15Х5М ГОСТ 550-75',
                 'measure': 'м'
                 },
                {'num': '3',
                 'notice': 'Трубы по ГОСТ 550-75 из стали 15Х5М \nдолжны соответствовать требованиям: 1.Партия должна состоять из труб \nодной плавки и иметь единый документ о качестве с указанием химического \nсостава и сведений о термообработке.  2. Группа «А». 3.Термообработка. \n4. Гидроиспытание. 5. Контроль неразрушающими методами (рентген или УЗД)\n по всей поверхности. 6. Испытание на загиб и раздачу. 7.Испытание на \nсплющивание для труб.',
                 'quantity': '2713,5',
                 'name': 'Труба 25х2,5х13500 ст.15Х5М ГОСТ 550-75',
                 'measure': 'м'
                 },
                {'num': '4',
                 'notice': 'Трубы по ГОСТ 550-75 из стали 15Х5М \nдолжны соответствовать требованиям: 1.Партия должна состоять из труб \nодной плавки и иметь единый документ о качестве с указанием химического \nсостава и сведений о термообработке.  2. Группа «А». 3.Термообработка. \n4. Гидроиспытание. 5. Контроль неразрушающими методами (рентген или УЗД)\n по всей поверхности. 6. Испытание на загиб и раздачу. 7.Испытание на \nсплющивание для труб.',
                 'quantity': '126',
                 'name': 'Труба 25х2,5х14000 ст.15Х5М ГОСТ 550-75',
                 'measure': 'м'
                 }
            ],
            'status': 'Опубликован',
            'fio': 'Шевченко Т. Ю.',
            'sub_order': ' - информация по заказу доступна всем пользователям  - к участию допускаются только приглашенные организации  - к участию автоматически допускаются все участники, подавшие заявки на участие  - специальные предложения (аналоги, замены) НЕ допускаются  - необходимо указать цены по всем позициям заказа',
            'number': 'РД-180925-7',
            'customer': 'БМЗ',
            'delivery_terms': 'Поставка\n не более 45 календарных дней. Доставка за счёт продавца. В случае \nнеобходимости Поставщик обязуется осуществлять самодекларирование по \nисполнению договорных обязательств (Поставщик формирует основные вехи \nисполнения заказа, график контрольных сроков и предоставляет информацию \nпо его исполнению). ',
            'price': 3232346.0,
            'scoring_date': ('02.10.2018 10:30', None),
            'sub_start_date': None,
            'attachments': [
                {'real_name': 'Приглашение.pdf',
                 'publication_date': ('01.10.2018 08:54', None),
                 'size': '471,78 KB',
                 'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2093909700021&x02=87539780000&x03=87507700000',
                 'display_name': 'Приглашение'
                 },
                {'real_name': 'Спецификация.xls',
                 'publication_date': ('01.10.2018 08:54', None),
                 'size': '54,5 KB',
                 'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2093910220021&x02=87539780000&x03=87507700000',
                 'display_name': 'Спецификация'
                 },
                {'real_name': 'Условия поставки.pdf',
                 'publication_date': ('01.10.2018 08:54', None),
                 'size': '148,01 KB',
                 'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2093909440021&x02=87539780000&x03=87507700000',
                 'display_name': 'Условия поставки'
                 },
                {'real_name': 'Анкета ТН.docx',
                 'publication_date': ('01.10.2018 08:54', None),
                 'size': '19,56 KB',
                 'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2093910260021&x02=87539780000&x03=87507700000',
                 'display_name': 'Анкета ТН.'
                 },
                {'real_name': 'Гарантийное письмо ТН.doc',
                 'publication_date': ('01.10.2018 08:54', None),
                 'size': '36 KB',
                 'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2093910340021&x02=87539780000&x03=87507700000',
                 'display_name': 'Гарантийное письмо ТН'
                 },
                {'real_name': 'Макет договора.doc',
                 'publication_date': ('01.10.2018 08:54', None),
                 'size': '675 KB',
                 'url': 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show?p_flow_id=220&p_flow_step_id=2155&p_request=APPLICATION_PROCESS=APX_CARD_FILE_DOWNLOAD&x01=2093909480021&x02=87539780000&x03=87507700000',
                 'display_name': 'Макет договора'
                 }
            ],
            'id': 'РД-180925-7_1',
            'sub_close_date': None,
            'type': 'Редукцион',
            'publication_date': ('01.10.2018 08:54', None),
            'name': 'Поставка труб (согл-836383615-1) (2486/ИсхОрг(335))'
        }
        self.assertEqual(true_result, result)


if __name__ == '__main__':
    unittest.main()
