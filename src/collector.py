from src.http import Http
from src.bll.mapper import Mapper
from src.bll.parser import Parser
from src.tools import Tools
from src.repository.mongodb import MongoRepository
from src.repository.rabbitmq import RabbitMqProvider
from settings import mongodb, rabbitmq, proxy


class Collector:
    """
    Класс с логикой сбора
    """
    def __init__(self, quantity=None, publish_date=None, base_url=None):
        # Инициализация классов и подключений
        self.http = Http(proxy)
        self.mapper = Mapper()
        self.parser = Parser(base_url)
        self.publish_date = publish_date
        self.quantity = quantity
        """
        self.repository = MongoRepository(mongodb['host'],
                                          mongodb['port'],
                                          mongodb['database'],
                                          mongodb['collection'])
        self.rabbitmq = RabbitMqProvider(rabbitmq['host'],
                                         rabbitmq['port'],
                                         rabbitmq['username'],
                                         rabbitmq['password'],
                                         rabbitmq['queue'])"""

    def collect(self):
        """
        Сбор тендеров
        Последовательность действий:
        *   Получение генератора списков
        *   Получение списка тендеров
        *   Итерация по каждому тендеру
        """
        # Получение генератора списка данных тендеров
        tender_data_list_gen = self.http.get_tender_list()
        # Обработка тендеров
        count = 0
        for tender_data_list in tender_data_list_gen:
            tender_items_list = self.parser.get_part_data(tender_data_list)
            total = len(tender_items_list)
            for i, item in enumerate(tender_items_list):
                if self.publish_date:
                    if self.publish_date.day == Tools.get_datatime_from_string(item['publication_date']).day:
                        print('[{}/{}] Processing tender number: {}'.format(i + 1, total, item))
                        self.process_tender(item)
                        count += 1
                    else:
                        continue
                else:
                    print('[{}/{}] Processing tender number: {}'.format(i+1, total, item))
                    self.process_tender(item)
                    count += 1
                if count == self.quantity:
                    break
            if count == self.quantity:
                break

    def process_tender(self, item):
        """
        Метод обработки тендера
        Последовательность действий:
        * Получаение данных тендера и парсинг (информация, лоты, прикрепленные файлы итп)
        * Проверяем в базе есть ли идентичная запись
        * Если что-то поменялось (статус), то обновляем в базе и отсылаем в очередь
          Иначе пропускаем
        """
        """
        # Получение HTML страницы с данными тендера
        tender_data_html = self.http.get_tender_data(item['link'])
        tender_lots = self.parser.get_tender_lots_data(tender_data_html)
        multilot = True if len(tender_lots) > 1 else False
        org = self.parser.get_org_data(tender_data_html)
        attachments = self.parser.get_attachments(tender_data_html)
        #print(item, tender_lots, org, attachments, multilot)

        for lot in tender_lots:
            tender_lot_id = '{}_{}'.format(item['number'], lot['number'])
            dbmodel = self.repository.get_one(tender_lot_id)
            if dbmodel is None or dbmodel['status'] != lot['status']:
            #if True:
                model = self.mapper.map(item, multilot, org, attachments, lot, tender_lot_id)
                #print(model)
                
                short_model = {
                    '_id': model['id'],
                    'status': model['status']
                }

                # добавляем/обновляем в MongoDB
               
                self.repository.upsert(short_model)
                print('Upserted in MongoDB')

                # отправляем в RabbitMQ
                self.rabbitmq.publish(model)
                print('Published to RabbitMQ')"""
