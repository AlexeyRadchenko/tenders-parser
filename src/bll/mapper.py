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
    def get_customer_model_list(item):
        return [{
            'guid': None,
            'name': 'ООО «Иркутская нефтяная компания»',
            'region': None
        }]

    @staticmethod
    def get_global_search(item):
        return '{} {} {}'.format(
            item['number'],
            item['name'] if item['name'] else '',
            'ООО «Иркутская нефтяная компания»',
        )

    @staticmethod
    def get_tender_search(item):
        return '{} {} {}'.format(
            item['number'] if item['number'] else '',
            item['name'] if item['name'] else '',
            'ООО «Иркутская нефтяная компания»'
        )

    def get_attachments(self, files):
        if not files:
            return None
        attachments = []
        for file in files:
            attachments.append({
                'displayName': file['display_name'],
                'href': file['url'],
                'publicationDateTime': self.tools.get_utc_epoch(
                    file['publication_date'][0], file['publication_date'][1]),
                'realName': file['real_name'],
                'size': None
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
            'customers': self.get_customer_model_list(item),
            # массив документов
            'attachments': self.get_attachments(item.get('attachments')),
            'globalSearch': self.get_global_search(item),
            'guaranteeApp': None,
            'href': item.get('link'),
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
            'organisationsSearch': 'ООО «Иркутская нефтяная компания»',
            'placingWay': 0,
            'platform': {
                'href': 'https://tenders.irkutskoil.ru/',
                'name': 'ЭТП Иркутская нефтяная компания',
            },
            # Дата публикации тендера UNIX EPOCH (UTC)
            'publicationDateTime': self.tools.get_utc_epoch(
                item['publication_date'][0], item['publication_date'][1]) if item.get('publication_date') else None,
            'region': 38,
            # Дата окончания подачи заявок UNIX EPOCH (UTC)
            'submissionCloseDateTime': self.tools.get_utc_epoch(
                item['sub_close_date'][0], item['sub_close_date'][1]) if item.get('sub_close_date') else None,
            # Дата начала подачи заявок UNIX EPOCH (UTC)
            'submissionStartDateTime': self.tools.get_utc_epoch(
                item['sub_start_date'][0], item['sub_start_date'][1]) if item.get('sub_close_date') else None,
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
            "modification": {
                'modDateTime': None,
                'reason': None
            },
            'futureNumber': None,
            'scoringDateTime': None,
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

    def get_json(self, model):
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
                    name='procedureInfo',
                    displayName='Порядок размещения заказа',
                    modifications=[]
                ).add_field(
                    Field(
                        name='PublicationtDateTime',
                        displayName='Дата публикации',
                        value=model.get('publicationDateTime'),
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='AcceptOrderStartDateTime',
                        displayName='Начало сбора заявок',
                        value=model.get('submissionStartDateTime'),
                        type=FieldType.DateTime,
                        modifications=[Modification.Calendar]
                    )
                ).add_field(
                    Field(
                        name='AcceptOrderEndtDateTime',
                        displayName='Окончание сбора заявок',
                        value=model.get('submissionCloseDateTime'),
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
                    value='ООО «Иркутская нефтяная компания»',
                    type=FieldType.String,
                    modifications=[]
                    )
                ).add_field(Field(
                    name='PostAddress',
                    displayName='Почтовый адрес',
                    value='Россия, 664007, г. Иркутск, пр-кт Большой Литейный, д. 4',
                    type=FieldType.String,
                    modifications=[]
                    )
                ).add_array(
                    lambda ar: ar.set_properties(
                        name='Contacts',
                        displayName='Контакты',
                        modifications=[Modification.HiddenLabel]
                    ).add_field(Field(
                        name='EmailSupport',
                        displayName='Электронная почта',
                        value='support.etp@irkutskoil.ru',
                        type=FieldType.String,
                        modifications=[Modification.Email]
                        )
                    ).add_field(Field(
                        name='EmailPko',
                        displayName='Электронная почта',
                        value='pko@irkutskoil.ru',
                        type=FieldType.String,
                        modifications=[Modification.Email]
                        )
                    )
                )
            ).to_json()
