import re
from decimal import Decimal
from datetime import datetime, timedelta
import time
from operator import itemgetter


class Tools:
    """
    Класс со вспомогательными функциями
    """
    def clear(self, string):
        """
        Очистка строки от мусора
        """
        if string is None or string.strip() == '':
            return None
        return re.sub(' +',' ', string.strip().replace('\n','').replace('\r','').replace('\t',''))

    def to_decimal(self, string):
        """
        Приведение сумм к double
        """

        if string is None or string.strip() == '':
            return None
        return float(string.replace(" ", "").replace(",", "."))

    @staticmethod
    def get_datatime_from_string(date_string):
        if date_string is None or date_string.strip() == '':
            return None

        parts_date = date_string.split(' ')

        if len(parts_date) > 2:
            index = (0, 1)
            datetime_string = ' '.join(itemgetter(*index)(date_string.split(' ')))
            try:
                date = datetime.strptime(datetime_string.replace('\n', '').replace('\t', '').replace('\r', ''),
                                         '%d.%m.%Y %H:%M:%S')
            except ValueError:
                date = datetime.strptime(datetime_string.replace('\n', '').replace('\t', '').replace('\r', '') + ':00',
                                         '%d.%m.%Y %H:%M:%S')
            return date
        else:
            date = datetime.strptime(date_string.replace('\n', '').replace('\t', '').replace('\r', ''),
                                     '%d.%m.%Y')
            return date

    def get_utc_epoch(self, date_string, time_delta):
        """
        Парсинг дат и перевод их к виду UNIX EPOCH
        """
        if not time_delta:
            time_delta = 3
        if date_string is None or date_string.strip() == '':
            return None
        parts_date = date_string.split(' ')
        #print('one', date_string, time_delta)
        if len(parts_date) > 2:
            index = (0, 1)
            datetime_string = ' '.join(itemgetter(*index)(date_string.split(' ')))
            try:
                date = datetime.strptime(datetime_string.replace('\n','').replace('\t','').replace('\r',''),
                                         '%d.%m.%Y %H:%M:%S') - timedelta(hours=time_delta)
            except ValueError:
                date = datetime.strptime(datetime_string.replace('\n', '').replace('\t', '').replace('\r', '') + ':00',
                                         '%d.%m.%Y %H:%M:%S') - timedelta(hours=time_delta)
        elif len(parts_date) == 2:
            date = datetime.strptime(date_string.replace('\n', '').replace('\t', '').replace('\r', ''),
                                     '%d.%m.%Y %H:%M') - timedelta(hours=time_delta)
        else:
            date = datetime.strptime(date_string.replace('\n','').replace('\t','').replace('\r',''),
                                     '%d.%m.%Y') - timedelta(hours=time_delta)

        epoch_time = (date - datetime(1970, 1, 1)).total_seconds() * 1000
        return int(epoch_time)

    def get_utc(self):
        """
        Текущая дата/время в UNIX EPOCH
        """
        return int(time.time()) * 1000


ORG_REGION_MAP = {
    "Газпром нефть" : 55,
    "Газпромнефть-ННГ" : 89,
    "Газпромнефть-Муравленко" : 89,
    "Газпромнефть-Восток" : 89,
    "Газпромнефть-Хантос" : 86,
    "Газпромнефть-ОНПЗ" : 55,
    "Газпромнефть-МНПЗ" : 77,
    "Газпромнефть-Оренбург" : 56,
    "Газпромнефть-Ангара" : 89,
    "Славнефть-Мегионнефтегаз" : 86,
    "Газпромнефть-Ямал" : 89,
    "Газпром нефть шельф" : 77,
    "Газпромнефть-Развитие" : 77,
    "Газпромнефть-Сахалин" : 65,
    "Мессояханефтегаз" : 89,
    "Газпромнефть НТЦ" : 78,
    "НГК \"Славнефть" : 77,
    "Томскнефть" : 70,
    "Газпром нефть Азия" : 55,
    "Газпромнефть-Белнефтепродукт" : 55,
    "Газпромнефть-Казахстан" : 55,
    "Газпромнефть-Корпоративные продажи" : 52,
    "Газпромнефть-Новосибирск" : 54,
    "Газпромнефть-Региональные продажи" : 47,
    "Газпромнефть-Северо-Запад" : 78,
    "Газпромнефть-Транспорт" : 76,
    "Газпромнефть-Урал" : 66,
    "Газпромнефть Марин Бункер" : 78,
    "Газпромнефть-Аэро" : 77,
    "Газпромнефть-СМ" : 77,
    "Газпромнефть-Битумные материалы" : 62,
    "Газпромнефть-Снабжение" : 55,
    "ИТСК" : 77,
    "Многофункциональный комплекс \"Лахта центр" : 78,
    "Газпромнефть-Каталитические системы" : 55,
    "Газпромнефть-Рязанский завод битумных материалов" : 62,
    "Ноябрьскнефтегазсвязь" : 89,
    "Газпромнефть Бизнес-сервис" : 89,
    "Газпромнефть-Центр" : 77,
    "Газпромнефть-Красноярск" : 24,
    "Газпромнефть-Терминал" : 54,
    "Газпромнефть МЗСМ" : 50,
    "Полиэфир" : 52,
    "Совхимтех" : 77,
    "Газпром нефть - Таджикистан" : 55,
    "Газпромнефть-Энергосервис" : 77,
    "НОВА-Брит" : 77,
    "Ноябрьскэнергонефть" : 89,
    "Газпромнефть-ННГГФ" : 89,
    "Газпромнефть-Нефтесервис" : 77,
    "Газпромнефть-Логистика" : 89,
    "Газпромнефть-Альтернативное топливо" : 77,
    "Газпромнефть-Лаборатория" : 78,
    "Ноябрьсктеплонефть" : 89,
    "Газпромнефть - Битум Казахстан" : 77,
    "Комплекс Галерная" : 78,
    "Газпромнефть - смазочные материалы" : 77,
    "Газпромнефть-ГЕО": 72,
}
