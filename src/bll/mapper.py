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
    def get_organisations_search(customers_req):
        return ' '.join(
            ['{} {} {} {}'.format(inn, kpp, name, region) for inn, kpp, name, region in customers_req]
        )

    @staticmethod
    def get_global_search(item, lot):
        return '{} {} {} {}'.format(
            item['number'],
            item['name'] if item['name'] else '',
            ' '.join([customer['name'] for customer in lot['customers']]),
            lot['type'] if lot['type'] else ''
        )

    @staticmethod
    def get_tender_search(item, lot):
        return '{} {} {}'.format(
            item['number'] if item['number'] else '',
            item['name'] if item['name'] else lot['name'],
            ' '.join([customer[2] for customer in lot['customers_inn_kpp_name_region']])
        )

    def map(self, item, multilot, lot, tender_lot_id):
        """
        Функция маппинга итоговой модели
        """

        model = {
            # Идентификатор тендера (Тендер+Лот)
            # Для каждого лота в тендере создается отдельная модель
            'id': tender_lot_id,
            # Массив заказчиков
            # [{
            #   guid = идентификатор организации (str/None),
            #   name = название организации (str),
            #   region = регион организации (int/None),
            # }]
            'customers': lot['customers'],
            # массив документов
            'attachments': lot['attachments'],
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
            'orderName': item['name'],
            'organisationsSearch': self.get_organisations_search(lot['customers_inn_kpp_name_region']),
            'placingWay': self.get_placingway(lot['type']),
            'platform': {
                'href': 'https://zakupki.tmk-group.com/#com/procedure/index',
                'name': 'Трубная металлургическая компания',
            },
            # Дата публикации тендера UNIX EPOCH (UTC)
            'publicationDateTime': self.tools.get_utc_epoch(item['publication_date']),
            'region': lot['org_region'],
            # Дата окончания подачи заявок UNIX EPOCH (UTC)
            'submissionCloseDateTime': self.tools.get_utc_epoch(
                lot['sub_close_date']) if lot['sub_close_date'] else None,
            # Дата начала подачи заявок UNIX EPOCH (UTC)
            'submissionStartDateTime': self.tools.get_utc_epoch(item['publication_date']),
            'tenderSearch': self.get_tender_search(item, lot),
            # Дата маппинга модели в UNIX EPOCH (UTC) (milliseconds)
            'timestamp': self.tools.get_utc(),
            'status': self.get_status(lot['status']),
            # Версия извещения
            # Если на площадке нет версии, то ставить 1
            'version': 1,
            'kind': 0,
            'type': 30,
            'ktru': [],
            'group': None,
            'preference': [],
            'prepayment': None,
            'modification': {
                'modDateTime': self.tools.get_utc_epoch(lot['last_edit_date']),
                "reason": None
            },
            'futureNumber': None,
            'guid': None,
            'scoringDateTime': self.tools.get_utc_epoch(lot['scoring_date']),
            'biddingDateTime': None,
        }

        model['json'] = self.get_json(
            model,
            lot
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

        if org_form in ['Аукцион на понижение (редукцион)']:
            return 15
        elif org_form in ['Запрос предложений', 'Попозиционный запрос предложений']:
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
        elif string == 'registration':
            return 1
        elif string == 'second_parts':
            return 2
        elif string == 'completed':
            return 3
        elif string in ['cancelled', 'failed']:
            return 4
        elif string == 'trade':
            return 7

    @staticmethod
    def get_currency_mod(lot_currency):
        if lot_currency == 'RUB':
            return Modification.CurRUB
        elif lot_currency == 'USD':
            return Modification.CurUSD
        elif lot_currency == 'EUR':
            return Modification.CurEUR

    def get_json(self, model, lot):
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
                    guarantee_app=None,
                    guarantee_contract=None,
                    customer_guid=' '.join([customer['guid'] for customer in model['customers']]),
                    customer_name=' '.join([customer['name'] for customer in model['customers']]),
                    currency=lot['currency']
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
                            Head(name='Name', displayName='Наименование'),
                            Head(name='Quantity', displayName='Количество'),
                            Head(name='TradeMark', displayName='Предпочтительная торговая марка'),
                            Head(name='Options', displayName='Характеристики'),
                            Head(name='Measure', displayName='Единица измерения')
                        ])
                    ).add_rows(
                        [position for position in lot['positions']],
                        lambda position, row: row.add_cells([
                            Cell(
                                name='Name',
                                type=FieldType.String,
                                value=position.get('name'),
                                modifications=[]
                            ),
                            Cell(
                                name='Quantity',
                                type=FieldType.String,
                                value=str(position.get('quantity')),
                                modifications=[]
                            ),
                            Cell(
                                name='TradeMark',
                                type=FieldType.String,
                                value=position.get('trademark'),
                                modifications=[]
                            ),
                            Cell(
                                name='Options',
                                type=FieldType.String,
                                value=' '.join([
                                    '{} ({}): {}'.format(
                                        pos['requirement'],
                                        pos['type_vocab'],
                                        pos['value'].replace('::', ' ')
                                    ) for pos in position.get('requirements')]
                                ),
                                modifications=[]
                            ),
                            Cell(
                                name='Measure',
                                type=FieldType.String,
                                value=position.get('okei_symbol'),
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
                        displayName='Дата и время окончания срока подачи заявок',
                        value=model['submissionCloseDateTime'],
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='ScoringStartEndTime',
                        displayName='Дата окончания срока подведения итогов',
                        value=model['scoringDateTime'],
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
                    value=lot['org'],
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
                        value=lot['org_fio'],
                        type=FieldType.String,
                        modifications=[Modification.HiddenLabel]
                        )
                    ).add_field(Field(
                        name='Phone',
                        displayName='Телефон',
                        value=lot['org_phone'],
                        type=FieldType.String,
                        modifications=[]
                        )
                    ).add_field(Field(
                        name='Email',
                        displayName='Электронная почта',
                        value=lot['org_email'],
                        type=FieldType.String,
                        modifications=[Modification.Email]
                        )
                    ).add_field(Field(
                        name='CustomerPlace',
                        displayName='Адрес местонахождения',
                        value=lot['org_address'],
                        type=FieldType.String,
                        modifications=[]
                        )
                    )
                )
            ).add_general(
                lambda f: f.set_properties(
                    name='DeliveryAmount',
                    displayName='Объем поставки',
                    value=lot['delivery_volume'],
                    type=FieldType.String,
                    modifications=[]
                )
            ).add_general(
                lambda f: f.set_properties(
                    name='DeliveryPlace',
                    displayName='DeliveryPlace',
                    value=lot['delivery_place'] if lot['delivery_place'] else '',
                    type=FieldType.String,
                    modifications=[]
                )
            ).add_general(
                lambda f: f.set_properties(
                    name='PaymentTerms',
                    displayName='Условия, сроки поставки и оплаты',
                    value=lot['delivery_term'],
                    type=FieldType.String,
                    modifications=[]
                )
            ).add_general(
                lambda f: f.set_properties(
                    name='Notice',
                    displayName='Комментарий',
                    value=lot['delivery_comment'],
                    type=FieldType.String,
                    modifications=[]
                )
            ).add_general(
                lambda f: f.set_properties(
                    name='DeliveryType',
                    displayName='Базис доставки',
                    value=lot['delivery_basis'],
                    type=FieldType.String,
                    modifications=[]
                )
            ).to_json()
