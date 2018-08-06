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

    def get_utc_epoch(self, date_string):
        """
        Парсинг дат и перевод их к виду UNIX EPOCH
        """

        if date_string is None or date_string.strip() == '':
            return None
        parts_date = date_string.split(' ')
        if len(parts_date) > 2:
            index = (0, 1)
            datetime_string = ' '.join(itemgetter(*index)(date_string.split(' ')))
            try:
                date = datetime.strptime(datetime_string.replace('\n','').replace('\t','').replace('\r',''),
                                         '%d.%m.%Y %H:%M:%S') - timedelta(hours=5)
            except ValueError:
                date = datetime.strptime(datetime_string.replace('\n', '').replace('\t', '').replace('\r', '') + ':00',
                                         '%d.%m.%Y %H:%M:%S') - timedelta(hours=5)
        elif len(parts_date) == 2:
            date = datetime.strptime(date_string.replace('\n', '').replace('\t', '').replace('\r', ''),
                                     '%d.%m.%Y %H:%M:%S') - timedelta(hours=5)
        else:
            date = datetime.strptime(date_string.replace('\n','').replace('\t','').replace('\r',''),
                                     '%d.%m.%Y') - timedelta(hours=5)

        epoch_time = (date - datetime(1970, 1, 1)).total_seconds() * 1000
        return int(epoch_time)

    def get_utc(self):
        """
        Текущая дата/время в UNIX EPOCH
        """
        return int(time.time()) * 1000


REGION_MAP = {
    "москва": 77,
    "московская область": 50,
    "ярославская область": 76,
    "ивановская область": 37,
    "костромская область": 44,
    "вологодская область": 35,
    "архангельская область": 29,
    "ненецкий автономный округ": 89,
    "коми республика": 11,
    "тверская область": 69,
    "новгородская область": 53,
    "псковская область": 60,"мурманская область": 51,
    "карелия республика": 10,
    "ленинградская область": 47,
    "санкт-петербург": 78,
    "смоленская область": 67,
    "калининградская область": 39,
    "брянская область": 32,
    "калужская область": 40,
    "крым республика": 91,
    "севастополь": 92,
    "тульская область": 71,
    "орловская область": 57,
    "курская область": 46,
    "белгородская область": 31,
    "ростовская область": 61,
    "краснодарский край": 23,
    "ставропольский край": 26,
    "калмыкия республика": 8,
    "кабардино-балкарская республика": 7,
    "северная осетия-алания республика": 15,
    "чеченская республика": 95,
    "дагестан республика": 5,
    "карачаево-черкесская республика": 9,
    "адыгея республика": 1,
    "ингушетия республика": 6,
    "рязанская область": 62,
    "тамбовская область": 68,
    "воронежская область": 36,
    "липецкая область": 48,
    "волгоградская область": 34,
    "саратовская область": 64,
    "астраханская область": 30,
    "татарстан республика": 16,
    "марий эл республика": 12,
    "удмуртская республика": 18,
    "чувашская республика": 21,
    "мордовия республика": 13,
    "ульяновская область": 73,
    "пензенская область": 58,
    "самарская область": 63,
    "башкортостан республика": 2,
    "челябинская область": 74,
    "оренбургская область": 56,
    "казахстан": 99,
    "германия": 0,
    "южная осетия республика": 0,
    "владимирская область": 33,
    "нижегородская область": 52,"кировская область": 43,
    "пермский край": 59,
    "свердловская область": 66,
    "тюменская область": 72,
    "ханты-мансийский-югра автономный округ": 86,
    "ямало-ненецкий автономный округ": 89,
    "новосибирская область": 54,
    "томская область": 70,
    "курганская область": 45,
    "омская область": 55,
    "красноярский край": 24,
    "алтай республика": 4,
    "кемеровская область": 42,
    "хакасия республика": 19,
    "алтайский край": 22,
    "иркутская область": 38,
    "тыва республика": 17,
    "бурятия республика": 3,
    "забайкальский край": 75,
    "амурская область": 28,
    "саха (якутия) республика": 14,
    "еврейская автономная область": 79,
    "хабаровский край": 27,
    "камчатский край": 41,
    "магаданская область": 49,
    "чукотский автономный округ": 87,
    "приморский край": 25,
    "сахалинская область": 65
}
