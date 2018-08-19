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
        """на инн кпп не указано"""
        return item['customer'] if item['customer'] else ''

    @staticmethod
    def get_customer_model_list(item, org):
        return [{
            'guid': None,
            'name': item['customer'] if item['customer'] else org['name'],
            'region': int(org['region']) if org['region'] else None
        }]

    @staticmethod
    def get_global_search(item):
        return '{} {} {} {}'.format(
            item['number'],
            item['name'] if item['name'] else '',
            item['customer'] if item['customer'] else '',
            item['type'] if item['type'] else ''
        )

    @staticmethod
    def get_tender_search(item):
        return '{} {} {}'.format(
            item['number'] if item['number'] else '',
            item['name'],
            item['customer'] if item['customer'] else ''
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

    def map(self, item, multilot, org, attachments, lot, tender_lot_id):
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
            'customers': self.get_customer_model_list(item, org),
            # массив документов
            'attachments': self.get_attachments(attachments),
            'globalSearch': self.get_global_search(item),
            'guaranteeApp': None,
            'href': item['link'],
            'json': None,
            # Максимальная (начальная) цена тендера
            'maxPrice': None,
            'multilot': multilot,
            'number': item['number'],
            # Массив ОКПД (если присутствует) ex. ['11.11', '20.2']
            'okdp': [],
            # Массив ОКПД2 (если присутствует)
            'okpd': [],
            # Массив ОКДП (если присутствует)
            'okpd2': [],
            'preference': [],
            'ktru': [],
            'prepayment': None,
            'orderName': item['name'],
            'organisationsSearch': self.get_organisations_search(item),
            'placingWay': self.get_placingway(item['type']),
            'platform': {
                'href': 'http://zakupki.gazprom-neft.ru/',
                'name': 'Газпромнефть',
            },
            # Дата публикации тендера UNIX EPOCH (UTC)
            'publicationDateTime': self.tools.get_utc_epoch(lot['publication_date'][0], lot['publication_date'][1]),
            'region': org['region'],
            # Дата окончания подачи заявок UNIX EPOCH (UTC)
            'submissionCloseDateTime': self.tools.get_utc_epoch(
                lot['sub_close_date'][0], lot['sub_close_date'][1]) if lot['sub_close_date'] else None,
            # Дата начала подачи заявок UNIX EPOCH (UTC)
            'submissionStartDateTime': self.tools.get_utc_epoch(lot['publication_date'][0], lot['publication_date'][1]),
            'tenderSearch': self.get_tender_search(item),
            # Дата маппинга модели в UNIX EPOCH (UTC) (milliseconds)
            'timestamp': self.tools.get_utc(),
            'status': self.get_status(item['status']),
            # Версия извещения
            # Если на площадке нет версии, то ставить 1
            'version': 1,
            'kind': 0,
            'type': 18,
            'modification': {
                'modDateTime': self.tools.get_utc(),
                'reason': lot['info_msg'] if lot['info_msg'] else None,
            },
            'futureNumber': None,
            'scoringDateTime': None,
            'biddingDateTime': self.tools.get_utc_epoch(lot['order_view_date'][0], lot['order_view_date'][1]),
        }

        model['json'] = self.get_json(
            model,
            lot,
            org,
            item
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
        if org_form in ['Предквалификационный отбор']:
            return 5
        elif org_form in ['Отбор']:
            return 16
        elif org_form in ['Аукцион', 'Редукцион']:
            return 15
        elif org_form in ['Запрос предложений']:
            return 14
        elif org_form in ['Запрос цен']:
            return 16
        elif org_form in ['Попозиционные торги']:
            return 18
        elif org_form in ['Запрос котировок']:
            return 4
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
        [, , 'Вскрытие конвертов завершено']
        """

        if string is None or string.strip() == '':
            return 0
        elif string in ['Объявлен', 'Прием предложений']:
            return 1
        elif string in ['Вскрытие конвертов завершено', 'Рассмотрение предложений']:
            return 2
        elif string in ['Заключение договора', 'Проведение аукциона']:
            return 7
        elif string in ['Завершен']:
            return 3
        elif string == 'Отменен':
            return 4

    @staticmethod
    def get_currency_mod(lot_currency):
        if lot_currency == 'RUB':
            return Modification.CurRUB
        elif lot_currency == 'USD':
            return Modification.CurUSD
        elif lot_currency == 'EUR':
            return Modification.CurEUR

    def get_json(self, model, lot, org, item):
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
                            Head(name='Name', displayName='Наименование закупки'),
                            Head(name='DueDate', displayName='Срок выполнения'),
                            Head(name='Volume', displayName='Объем работ в рамках лота'),
                            Head(name='SubjectProcurement', displayName='Предмет закупки')
                        ])
                    ).add_rows(
                        [lot],
                        lambda el, row: row.add_cells([
                            Cell(
                                name='Name',
                                type=FieldType.String,
                                value=el.get('name'),
                                modifications=[]
                            ),
                            Cell(
                                name='DueDate',
                                type=FieldType.String,
                                value=el.get('processing_time'),
                                modifications=[]
                            ),
                            Cell(
                                name='Volume',
                                type=FieldType.String,
                                value=el.get('volume'),
                                modifications=[]
                            ),
                            Cell(
                                name='SubjectProcurement',
                                type=FieldType.String,
                                value=el.get('lot_subject'),
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
                        displayName='Дата и время начала приёма предложений',
                        value=model['submissionStartDateTime'],
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='AcceptOrderEndDateTime',
                        displayName='Дата и время окончания приёма предложений',
                        value=model['submissionCloseDateTime'],
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='BiddingEndDateTime',
                        displayName='Дата вскрытия',
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
                    )
                )
            ).add_general(
                lambda f: f.set_properties(
                    name='Placement',
                    displayName='Место оказания работ/услуг',
                    value=item['target_place'],
                    type=FieldType.String,
                    modifications=[]
                )
            ).to_json()
