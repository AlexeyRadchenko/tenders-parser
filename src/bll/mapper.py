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
    def get_organisations_search(item):
        return '{} {} {}'.format(
            '4218000951',
            '421801001',
            item['customer']
        )

    @staticmethod
    def get_customer_model_list(customer):
        return [{
            'guid': None,
            'name': customer,
            'region': 42,
        }]

    @staticmethod
    def get_global_search(item):
        return '{} {}'.format(
            item['number'],
            item['name'] if item['name'] else '',
        )

    @staticmethod
    def get_tender_search(item):
        return '{} {}'.format(
            item['number'] if item['number'] else '',
            item['name'] if item['name'] else '',
        )

    def get_attachments(self, item):
        attachments = {
            'displayName': item['attachments'][0],
            'href': item['attachments'][2],
            'publicationDateTime': self.tools.get_utc_epoch(item['publication_date']),
            'realName': item['attachments'][1],
            'size': None
        }
        return attachments

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
            'attachments': self.get_attachments(item) if item.get('attachments') else None,
            'globalSearch': self.get_global_search(item),
            'guaranteeApp': None,
            'href': item['link'],
            'json': None,
            # Максимальная (начальная) цена тендера
            'maxPrice': None,
            'multilot': False,
            'number': item['number'],
            # Массив ОКПД (если присутствует) ex. ['11.11', '20.2']
            'okdp': [],
            # Массив ОКПД2 (если присутствует)
            'okpd': [],
            # Массив ОКДП (если присутствует)
            'okpd2': [],
            'orderName': item['name'],
            'organisationsSearch': self.get_organisations_search(item),
            'placingWay': 0,
            'platform': {
                'href': 'http://supply.evraz.com',
                'name': 'АО «ЕВРАЗ ЗСМК»',
            },
            # Дата публикации тендера UNIX EPOCH (UTC)
            'publicationDateTime': self.tools.get_utc_epoch(item['publication_date']),
            'region': 42,
            # Дата окончания подачи заявок UNIX EPOCH (UTC)
            'submissionCloseDateTime': self.tools.get_utc_epoch(
                item['tech_part_date']) if item['tech_part_date'] else None,
            # Дата начала подачи заявок UNIX EPOCH (UTC)
            'submissionStartDateTime': self.tools.get_utc_epoch(item['publication_date']),
            'tenderSearch': self.get_tender_search(item),
            # Дата маппинга модели в UNIX EPOCH (UTC) (milliseconds)
            'timestamp': self.tools.get_utc(),
            'status': item['status'],
            # Версия извещения
            # Если на площадке нет версии, то ставить 1
            'version': 1,
            'kind': 0,
            'type': 30,
            'ktru': [],
            'modification': {
                'modDateTime': None,
                'reason': None
            },
            'futureNumber': None,
            'scoringDateTime': None,
            'biddingDateTime': None,
            'prepayment': None,
            'preference': None,
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
        elif org_form in ['Запрос предложений']:
            return 14
        elif org_form in ['Запрос цен']:
            return 16
        elif org_form in ['Попозиционные торги']:
            return 18
        elif org_form in ['Запрос котировок']:
            return 4
        elif org_form in ['Предварительный отбор']:
            return 5
        elif org_form in ['Конкурс']:
            return 1
        elif org_form in ['Открытая тендерная закупка в электронной форме']:
            return 16
        else:
            return 0

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

            status[
            , , , , , , , ]
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
                    max_price=None,
                    guarantee_app=None,
                    guarantee_contract=None,
                    customer_guid=model['customers'][0]['guid'],
                    customer_name=model['customers'][0]['name'],
                    currency=None,
                )
            ).add_category(
                lambda c: c.set_properties(
                    name='procedureInfo',
                    displayName='Порядок размещения заказа',
                    modifications=[]
                ).add_field(
                    Field(
                        name='PublicationtDateTime',
                        displayName='Дата публикации',
                        value=model['publicationDateTime'],
                        type=FieldType.Date,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='AcceptTechPartDateTime',
                        displayName='Дата принятия Технической части',
                        value=self.tools.get_utc_epoch(item['tech_part_date']) if item.get('tech_part_date') else None,
                        type=FieldType.DateTime,
                        modifications=[]
                    )
                ).add_field(
                    Field(
                        name='ExtendTechPartDateTime',
                        displayName='Дата продления Технической части',
                        value=self.tools.get_utc_epoch(
                            item['extend_tech_part_date']) if item.get('extend_tech_part_date') else None,
                        type=FieldType.DateTime,
                        modifications=[]
                    )
                ).add_field(
                    Field(
                        name='AcceptCommercialPartDateTime',
                        displayName='Дата принятия Коммерческой части',
                        value=self.tools.get_utc_epoch(
                            item['commercial_part_date']) if item.get('commercial_part_date') else None,
                        type=FieldType.DateTime,
                        modifications=[]
                    )
                ).add_field(
                    Field(
                        name='ExtendCommercialPartDateTime',
                        displayName='Дата продления Коммерческой части',
                        value=self.tools.get_utc_epoch(
                            item['extend_commercial_part_date']) if item.get('extend_commercial_part_date') else None,
                        type=FieldType.DateTime,
                        modifications=[]
                    )
                ).add_field(
                    Field(
                        name='StartWorkDateTime',
                        displayName='Дата начала работ',
                        value=self.tools.get_utc_epoch(
                            item['tender_process_start']) if item.get('tender_process_start') else None,
                        type=FieldType.Date,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='EndWorkDateTime',
                        displayName='Дата окончания работ',
                        value=self.tools.get_utc_epoch(
                            item['tender_process_end']) if item.get('tender_process_end') else None,
                        type=FieldType.Date,
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
                    value=item['customer'],
                    type=FieldType.String,
                    modifications=[]
                    )
                ).add_field(Field(
                    name='PostAddress',
                    displayName='Почтовый адрес',
                    value='654043, Россия, Кемеровская обл., г. Новокузнецк, ш. Космическое 16',
                    type=FieldType.String,
                    modifications=[]
                    )
                ).add_array(
                    lambda c: c.set_properties(
                        name='Contacts',
                        displayName='Контакты',
                        modifications=[Modification.HiddenLabel]
                    ).add_array_items(
                        item['contacts'],
                        lambda el, i: c.add_field(Field(
                                name='FIO' + str(i),
                                displayName='ФИО',
                                value=el[0],
                                type=FieldType.String,
                                modifications=[Modification.HiddenLabel]
                                )
                            ).add_field(Field(
                                name='Phone' + str(i),
                                displayName='Телефон',
                                value=el[1],
                                type=FieldType.String,
                                modifications=[]
                                )
                            ).add_field(Field(
                                name='Email' + str(i),
                                displayName='Электронная почта',
                                value=el[2],
                                type=FieldType.String,
                                modifications=[Modification.Email]
                                )
                            )
                    )
                )
            ).add_general(
                lambda f: f.set_properties(
                    name='Info',
                    displayName='Дополнительная информация',
                    value='{} {}'.format(item['sending_order'], item['dop_info']),
                    type=FieldType.String,
                    modifications=[]
                )
            ).to_json()