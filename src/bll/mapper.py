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
    def get_organisations_search(customer):
        """на roseltorg.ru кпп не указано"""
        return customer

    @staticmethod
    def get_customer_model_list(customer):
        return [{
            'guid': None,
            'name': customer,
            'region': 16
        }]

    @staticmethod
    def get_global_search(item):
        return '{} {} {}'.format(
            item['number'],
            item['name'] if item['name'] else '',
            item['type'] if item['type'] else ''
        )

    @staticmethod
    def get_tender_search(item):
        return '{} {}'.format(
            item['number'] if item['number'] else '',
            item['name'] if item.get('name') else item['name'],
        )

    def get_attachments(self, files):
        attachments = []
        for file in files:
            attachments.append({
                'displayName': file['display_name'],
                'href': file['url'],
                'publicationDateTime': self.tools.get_utc_epoch(
                    file['publication_date'][0], file['publication_date'][1]),
                'realName': file['real_name'],
                'size': file['size']
            })
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
            'attachments': self.get_attachments(item['attachments']),
            'globalSearch': self.get_global_search(item),
            'guaranteeApp': None,
            'href': item['link'],
            'json': None,
            # Максимальная (начальная) цена тендера
            'maxPrice': item['price'],
            'multilot': None,
            'number': item['number'],
            # Массив ОКПД (если присутствует) ex. ['11.11', '20.2']
            'okdp': [],
            # Массив ОКПД2 (если присутствует)
            'okpd': [],
            # Массив ОКДП (если присутствует)
            'okpd2': [],
            'orderName': item['name'],
            'organisationsSearch': self.get_organisations_search(item['customer']),
            'placingWay': self.get_placingway(item['type']),
            'platform': {
                'href': 'https://etp.tatneft.ru',
                'name': 'ЭТП Татнефть',
            },
            # Дата публикации тендера UNIX EPOCH (UTC)
            'publicationDateTime': self.tools.get_utc_epoch(*item['publication_date']),
            'region': 16,
            # Дата окончания подачи заявок UNIX EPOCH (UTC)
            'submissionCloseDateTime': self.tools.get_utc_epoch(
                *item['sub_close_date']) if item.get('sub_close_date') else None,
            # Дата начала подачи заявок UNIX EPOCH (UTC)
            'submissionStartDateTime': self.tools.get_utc_epoch(
                *item['sub_start_date']) if item.get('sub_start_date') else None,
            'tenderSearch': self.get_tender_search(item),
            # Дата маппинга модели в UNIX EPOCH (UTC) (milliseconds)
            'timestamp': self.tools.get_utc(),
            'status': self.get_status(item['status']),
            # Версия извещения
            # Если на площадке нет версии, то ставить 1
            'version': 1,
            'kind': 0,
            'type': 30,
            'ktru': [],
            "modification": {
                'modDateTime': '',
                'reason': ''
            },
            'futureNumber': None,
            'scoringDateTime': self.tools.get_utc_epoch(*item['scoring_date']) if item.get('scoring_date') else None,
            'biddingDateTime': None,
            'preference': [],
            'group': None,
        }

        model['json'] = self.get_json(model)
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
        ['Тендер', 'Запрос предложений', 'Редукцион']

        """

        if org_form in ['Аукцион на повышение', 'Аукцион на понижение']:
            return 15
        elif org_form in ['Запрос предложений']:
            return 14
        elif org_form in ['Запрос цен']:
            return 16
        elif org_form in ['Тендер', 'Редукцион']:
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

        ['Опубликован, прием предложений', 'Прием предложений завершен', 'Поставщик выбран', 'Раунд завершен', 'Торги не состоялись', 'Торги приостановлены']
        """

        if string is None or string.strip() == '':
            return 0
        elif string in ['Опубликован, прием предложений']:
            return 1
        elif string in ['Прием предложений завершен', 'Раунд завершен']:
            return 2
        elif string in ['Заключение договора', 'Проведение аукциона']:
            return 7
        elif string in ['Поставщик выбран']:
            return 3
        elif string == ['Торги не состоялись', 'Торги приостановлены']:
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
                    max_price=model['maxPrice'],
                    guarantee_app=model['guaranteeApp'],
                    guarantee_contract=None,
                    customer_guid=model['customers'][0]['guid'],
                    customer_name=model['customers'][0]['name']
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
                            Head(name='Name', displayName='Наименования товара, работы, услуги'),
                            Head(name='Count', displayName='Количество'),
                            Head(name='Measure', displayName='Единицы измерения'),
                            Head(name='Notice', displayName='Замечание')
                        ])
                    ).add_rows(
                        item['positions'],
                        lambda el, row: row.add_cells([
                            Cell(
                                name='Name',
                                type=FieldType.String,
                                value=el.get('name'),
                                modifications=[]
                            ),
                            Cell(
                                name='Count',
                                type=FieldType.String,
                                value=el.get('quantity'),
                                modifications=[]
                            ),
                            Cell(
                                name='Measure',
                                type=FieldType.String,
                                value=el.get('measure'),
                                modifications=[]
                            ),
                            Cell(
                                name='Notice',
                                type=FieldType.String,
                                value=el.get('notice'),
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
                        name='PublicationDateTime',
                        displayName='Дата публикации',
                        value=model['publicationDateTime'],
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='AcceptOrderEndDateTime',
                        displayName='Дата окончания приема предложений',
                        value=model['submissionCloseDateTime'],
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='ScoringStartDateTime',
                        displayName='Дата начала приема предложений',
                        value=model['submissionStartDateTime'],
                        type=FieldType.DateTime,
                        modifications=[]
                    )
                ).add_field(        #
                    Field(
                        name='ScoringEndDateTime',
                        displayName='Дата подведения итогов',
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
                        value=None,
                        type=FieldType.String,
                        modifications=[]
                        )
                    ).add_field(Field(
                        name='Email',
                        displayName='Электронная почта',
                        value=None,
                        type=FieldType.String,
                        modifications=[Modification.Email]
                        )
                    )
                )
            ).add_general(
                lambda f: f.set_properties(
                    name='Quantity',
                    displayName='Начальная цена заказа',
                    value=model['maxPrice'] if model.get('MaxPrice') else '',
                    type=FieldType.String,
                    modifications=[]
                )
            ).add_general(
                lambda f: f.set_properties(
                    name='deliveryPlace',
                    displayName='Место поставки',
                    value=item['delivery_place'] if item.get('delivery_place') else '',
                    type=FieldType.String,
                    modifications=[]
                )
            ).add_general(
                lambda f: f.set_properties(
                    name='PaymentTerms',
                    displayName='Условия и сроки поставки',
                    value=item['delivery_terms'] if item.get('payment_terms') else '',
                    type=FieldType.String,
                    modifications=[]
                )
            ).to_json()
