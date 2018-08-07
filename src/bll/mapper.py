from src.tools import Tools
from sharedmodel.module import Root, Field, Customer
from sharedmodel.module.table import Cell, Head
from sharedmodel.module.enum import FieldType, Modification


class Mapper:
    """
    Класс-маппер (перевод из обработанных данных в модель для отправки в менеджер очередей RabbitMQ)
    """
    def __init__(self):
        self.tools = Tools()

    @staticmethod
    def get_organisations_search(lot):
        """на roseltorg.ru кпп не указано"""
        return lot['customer'] if lot['customer'] else ''

    @staticmethod
    def get_customer_model_list(lot, org):
        return [{
            'guid': None,
            'name': lot['customer'] if lot['customer'] else org['name'],
            'region': lot['region']
        }]

    @staticmethod
    def get_global_search(item, lot):
        return '{} {} {} {}'.format(
            item['number'],
            lot['name'] if lot['name'] else '',
            lot['customer'] if lot['customer'] else '',
            lot['type'] if lot['type'] else ''
        )

    @staticmethod
    def get_tender_search(item, lot):
        return '{} {} {}'.format(
            item['number'] if item['number'] else '',
            lot['name'] if lot['name'] else '',
            lot['customer'] if lot['customer'] else ''
        )

    def get_attachments(self, lot, item):
        attachments = [{
                'displayName': None,
                'href': lot['doc'],
                'publicationDateTime': self.tools.get_utc_epoch(item['publication_datetime']),
                'realName': None,
                'size': None
            }]
        return attachments

    def map(self, item, multilot, org, lot):
        """
        Функция маппинга итоговой модели
        """

        model = {
            # Идентификатор тендера (Тендер+Лот)
            # Для каждого лота в тендере создается отдельная модель
            'id': int(item['number']),
            # Массив заказчиков
            # [{
            #   guid = идентификатор организации (str/None),
            #   name = название организации (str),
            #   region = регион организации (int/None),
            # }]
            'customers': self.get_customer_model_list(lot, org),
            # массив документов
            'attachments': self.get_attachments(lot, item),
            'globalSearch': self.get_global_search(item, lot),
            'guaranteeApp': None,
            'href': item['link'],
            'json': None,
            # Максимальная (начальная) цена тендера
            'maxPrice': lot['price'],
            'multilot': multilot,
            'number': item['number'],
            # Массив ОКПД (если присутствует) ex. ['11.11', '20.2']
            'okdp': [],
            # Массив ОКПД2 (если присутствует)
            'okpd': [],
            # Массив ОКДП (если присутствует)
            'okpd2': [],
            'orderName': lot['name'],
            'organisationsSearch': self.get_organisations_search(lot),
            'placingWay': self.get_placingway(lot['type']),
            'platform': {
                'href': 'http://www.zakupki.bgkrb.ru',
                'name': 'Башкирская генерирующая компания',
            },
            # Дата публикации тендера UNIX EPOCH (UTC)
            'publicationDateTime': self.tools.get_utc_epoch(item['publication_datetime']),
            'region': lot['region'],
            # Дата окончания подачи заявок UNIX EPOCH (UTC)
            'submissionCloseDateTime': self.tools.get_utc_epoch(item['close_sub_datetime']),
            # Дата начала подачи заявок UNIX EPOCH (UTC)
            'submissionStartDateTime': self.tools.get_utc_epoch(item['start_sub_datetime']),
            'tenderSearch': self.get_tender_search(item, lot),
            # Дата маппинга модели в UNIX EPOCH (UTC) (milliseconds)
            'timestamp': self.tools.get_utc(),
            'status': 0,
            # Версия извещения
            # Если на площадке нет версии, то ставить 1
            'version': 1,
            'kind': 0,
            'type': 30,
            'ktru': [],
            'prepayment': 'double',
        }

        model['json'] = self.get_json(
            model,
            lot,
            org
        )
        return model

    def get_placingway(self, org_form):
        """
        Получение способа определения поставщика
        т.к. на площадке присутствуют не все виды, то
        задействованы только присутствующие
        #     Открытый конкурс = 1,
        #     Открытый аукцион = 2,
        #     Открытый аукцион в электронной форме = 3,
        #     Запрос котировок = 4,
        #     Предварительный отбор = 5,
        #     Закупка у единственного поставщика (подрядчика, исполнителя) = 6,
        #     Конкурс с ограниченным участием = 7,
        #     Двухэтапный конкурс = 8,
        #     Закрытый конкурс = 9,
        #     Закрытый конкурс с ограниченным участием = 10,
        #     Закрытый двухэтапный конкурс = 11,
        #     Закрытый аукцион = 12,
        #     Запрос котировок без размещения извещения = 13,
        #     Запрос предложений = 14,
        #     Электронный аукцион = 15,
        #     Иной многолотовый способ = 16,
        #     Сообщение о заинтересованности в проведении открытого конкурса = 17,
        #     Иной однолотовый способ = 18
        """

        if org_form in ['аукцион']:
            return 15
        elif org_form in ['запрос предложений']:
            return 14
        elif org_form in ['запрос цен']:
            return 16
        elif org_form in ['оперативные закупки', 'Конкурентные переговоры', 'квалификационный отбор']:
            return 18
        elif org_form in ['запрос котировок']:
            return 4
        elif org_form in ['конкурс']:
            return 1
        else:
            return 5000

    @staticmethod
    def get_status(string):
        """
        Получения статуса тендера
        при изменении статуса тендер должен отсылаться в RabbitMQ
        #   Без статуса = 0,
        #   Опубликован = 1,
        #   На рассмотрении комиссии = 2,
        #   Закрыт = 3,
        #   Отменен = 4,
        #   Приостановлен = 5,
        #   Исполнение завершено = 6,
        #   Исполняется = 7,
        #   Приостановлено определение поставщика = 8
        т.к. на площадке присутствуют не все виды, то 
        задействованы только присутствующие
        """

        if string is None or string.strip() == '':
            return 0
        elif string in ['Прием заявок на участие', ]:
            return 1
        elif string in ['Подведение итогов', 'Вскрытие конвертов', 'Рассмотрение первых частей заявок']:
            return 2
        elif string in ['Заключение договора', 'Проведение аукциона']:
            return 7
        elif string in ['Архив']:
            return 3
        elif string == 'Процедура отменена':
            return 4

    @staticmethod
    def get_currency_mod(lot_currency):
        if lot_currency == 'RUB':
            return Modification.CurRUB
        elif lot_currency == 'USD':
            return Modification.CurUSD
        elif lot_currency == 'EUR':
            return Modification.CurEUR

    def get_json(self, model, lot, org):
        """
        Получение модели для рендера
        Использует sharedmodel модуль

        В данной модели обязательно присутствие:
        * general - основная информация
        * customer - заказчик

        В данной модели должно быть как можно больше информации о тендере
        (сроки поставки, вскрытия конвертов итп)

        """
        return Root()\
            .add_customer(
                Customer().set_properties(
                    max_price=model['maxPrice'],
                    guarantee_app=model['guaranteeApp'],
                    guarantee_contract=None,
                    customer_guid=model['customers'][0]['guid'],
                    customer_name=model['customers'][0]['name'],
                )
            ).add_category(
                lambda c: c.set_properties(
                    name='ObjectInfo',
                    displayName='Информация об объекте закупки',
                ).add_table(
                    lambda t: t.set_properties(
                        name='Objects',
                        displayName='Объекты закупки'
                    ).set_header(
                        lambda th: th.add_cells([
                            Head(name='Name', displayName='Наименование')
                        ])
                    ).add_rows(
                        [lot['name']],
                        lambda el, row: row.add_cells([
                            Cell(
                                name='Name',
                                type=FieldType.String,
                                value=el,
                                modifications=[]
                            )
                        ])
                    )
                )
            ).add_category(
                lambda c: c.set_properties(
                    name='procedureInfo',
                    displayName='Порядок размещения заказа',
                    modifications=[]
                ).add_field(
                    Field(
                        name='AcceptOrderStartDateTime',
                        displayName='Дата начала приема заявок',
                        value=model['submissionStartDateTime'],
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='AcceptOrderEndDateTime',
                        displayName='Дата окончания приема заявок',
                        value=model['submissionCloseDateTime'],
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                )
            ).add_category(
                lambda c: c.set_properties(
                    name='Contacts',
                    displayName='Контактная информация',
                    modifications=[]
                ).add_field(Field(
                    name='Organization',
                    displayName='Организация',
                    value=org['name'],
                    type=FieldType.String,
                    modifications=[]
                    )
                ).add_array(
                    lambda ar: ar.set_properties(
                        name='Contacts',
                        displayName='Контакты',
                        modifications=[Modification.HiddenLabel]
                    ).add_field(Field(
                        name='FIO',
                        displayName='ФИО',
                        value=org['fio'],
                        type=FieldType.String,
                        modifications=[Modification.HiddenLabel]
                        )
                    ).add_field(Field(
                        name='Phone',
                        displayName='Телефон',
                        value=org['phone'],
                        type=FieldType.String,
                        modifications=[]
                        )
                    ).add_field(Field(
                        name='Email',
                        displayName='Электронная почта',
                        value=org['email'],
                        type=FieldType.String,
                        modifications=[Modification.Email]
                        )
                    ).add_field(Field(
                        name='CustomerPlace',
                        displayName='Адрес местонахождения',
                        value='Башкортостан',
                        type=FieldType.String,
                        modifications=[]
                        )
                    )
                )
            ).to_json()
