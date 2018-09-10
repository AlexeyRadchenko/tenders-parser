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
    def get_customer_model_list(customer):
        return [{
            'guid': None,
            'name': customer,
            'region': 66
        }]

    @staticmethod
    def get_global_search(item):
        return '{} {} {}'.format(
            item['name'] if item['name'] else '',
            item['customer'],
            item['type'] if item['type'] else ''
        )

    @staticmethod
    def get_tender_search(item):
        return '{} {}'.format(
            item['name'],
            item['customer']
        )

    def map(self, item):
        """
        Функция маппинга итоговой модели
        """

        model = {
            # Идентификатор тендера (Тендер+Лот)
            # Для каждого лота в тендере создается отдельная модель
            'id': item['id'],
            # Массив заказчиков
            # [{
            #   guid = идентификатор организации (str/None),
            #   name = название организации (str),
            #   region = регион организации (int/None),
            # }]
            'customers': self.get_customer_model_list(item['customer']),
            # массив документов
            'attachments': None,
            'globalSearch': self.get_global_search(item),
            'guaranteeApp': None,
            'href': None,
            'json': None,
            # Максимальная (начальная) цена тендера
            'maxPrice': None,
            'multilot': False,
            'number': None,
            # Массив ОКПД (если присутствует) ex. ['11.11', '20.2']
            'okdp': [],
            # Массив ОКПД2 (если присутствует)
            'okpd': [],
            # Массив ОКДП (если присутствует)
            'okpd2': [],
            'orderName': item['name'],
            'organisationsSearch': item['customer'],
            'placingWay': self.get_placingway(item['type']),
            'platform': {
                'href': 'https://www.uralmash.ru/',
                'name': 'Уралмашзавод',
            },
            # Дата публикации тендера UNIX EPOCH (UTC)
            'publicationDateTime': item['publication_date'],
            'region': item['region'],
            # Дата окончания подачи заявок UNIX EPOCH (UTC)
            'submissionCloseDateTime': item['sub_close_date'],
            # Дата начала подачи заявок UNIX EPOCH (UTC)
            'submissionStartDateTime': item['sub_start_date'],
            'tenderSearch': self.get_tender_search(item),
            # Дата маппинга модели в UNIX EPOCH (UTC) (milliseconds)
            'timestamp': self.tools.get_utc(),
            'status': item['status'],
            # Версия извещения
            # Если на площадке нет версии, то ставить 1
            'version': 1,
            'kind': 0,
            'type': 30,
            'group': None,
            'guaranteeContract': None,
            'preference': [],
            'ktru': [],
            'prepayment': None,
            'modification': {
                'modDateTime': None,
                'reason': None,
            },
            'futureNumber': None,
            'scoringDateTime': None,
            'biddingDateTime': item['bidding_date'],
            }

        model['json'] = self.get_json(model, item)
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

        if org_form in ['Аукцион на повышение', 'Аукцион на понижение']:
            return 15
        elif org_form in ['Запрос предложений', 'Сбор коммерческих предложений', 'Запрос коммерческих предложений',
                          'запрос коммерческих предложений', 'запрос предложений', 'Запрос коммерческих предлжений',
                          'сбор коммерческих предложений']:
            return 14
        elif org_form in ['Закупка партии', 'запрос заявок', 'Подача заявок',
                          'подача заявок', 'Конкурентные переговоры', 'Попозиционная закупка', 'попозиционная закупка']:
            return 16
        elif org_form in ['отсрочка платежа', 'отсрочка', 'кредит']:
            return 18
        elif org_form in ['Запрос котировок', 'Запрос ценовых котировок', 'Запрос цновых котировок', 'Запрос цен',
                          'запрос ценовых котировок', 'запрос котировок', 'Котировки', 'запрос ценовых предложений',
                          'Запро котировок', 'котировки', 'Запрос (ценовых) котировок',
                          ' запрос ценовых котировок (запрос цен',
                          ' запрос ценовых котировок (запрос цен), ', 'запрос ценовых котировок (запрос цен)']:
            return 4
        elif org_form in ['Предварительный отбор']:
            return 5
        elif org_form in ['Конкурс']:
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
    def get_currency_mod(item):
        """['Российский рубль', 'Доллар США (USD)', 'Евро (EUR)']"""
        if item['currency'] == 'Российский рубль':
            return Modification.CurRUB
        elif item['currency'] == 'Доллар США (USD)':
            return Modification.CurUSD
        elif item['currency'] == 'Евро (EUR)':
            return Modification.CurEUR

    def get_json(self, model, item):
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
                    customer_guid='58c7e4a60640fd10b742b69e',
                    customer_name=model['customers'][0]['name'],
                    currency=item['currency']
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
                        [item['name']],
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
                        name='PublicationtDateTime',
                        displayName='Дата размещения процедуры',
                        value=model['publicationDateTime'],
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='AcceptOrderEndDateTime',
                        displayName='Срок приёма заявок',
                        value=model['submissionCloseDateTime'],
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='BiddingEndDateTime',
                        displayName='Дата подведения итогов',
                        value=model['biddingDateTime'],
                        type=FieldType.DateTime,
                        modifications=[]
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
                    value=item['customer'],
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
                        value=item['fio'],
                        type=FieldType.String,
                        modifications=[Modification.HiddenLabel]
                        )
                    ).add_field(Field(
                        name='Phone',
                        displayName='Телефон',
                        value=item['phone'],
                        type=FieldType.String,
                        modifications=[]
                        )
                    ).add_field(Field(
                        name='Email',
                        displayName='Электронная почта',
                        value=item['email'],
                        type=FieldType.String,
                        modifications=[Modification.Email]
                        )
                    ).add_field(Field(
                        name='CustomerPlace',
                        displayName='Адрес местонахождения',
                        value='620012, г. Екатеринбург, пл. Первой пятилетки',
                        type=FieldType.String,
                        modifications=[]
                        )
                    )
                )
            ).to_json()
