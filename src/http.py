from src.bll.retrier import retry
from requests import get
from bs4 import BeautifulSoup
import re

class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    source_url_list = [
        'https://tenders.irkutskoil.ru/tender_result.php',
        'https://tenders.irkutskoil.ru/tenders.php',
        'http://irkutskoil.ru/tenders/type/?archive=Y',
        'http://irkutskoil.ru/tenders/type/?archive=N'
    ]

    def get_max_pages_after(self, html):
        pagination = html.find('div', {'class': 'multip'}).find_all('a')
        print(pagination)
        if pagination:
            max_pages = re.search(r'\d+', pagination[8].attrs['href'])
            return int(max_pages.group(0))

    def get_max_pages_before(self, html):
        pagination = html.find('div', {'class': 'modern-page-navigation'}).find_all('a')
        #print(pagination)
        if pagination:
            return int(pagination[5].text)

    def get_tender_list(self):
        """генератор списков тендеров"""
        for i, url in enumerate(self.source_url_list):
            params = None
            max_pages = None
            # собираем сведения об АРХИВНЫХ тендерах в верстке ПОСЛЕ 17.07.2017, инициализация параметров влож. цикла
            if i == 0:
                params_key = 'cpage'
                params = {params_key: 1}
                search_args = 'table', {'class': 'lot_list'}
                get_max_pages_func = self.get_max_pages_after
                search_type = 'arc_after'
            # собираем сведения об АКТИВНЫХ тендерах в верстке ПОСЛЕ 17.07.2017, т.к. одна странница делаем запрос
            elif i == 1:
                r = get(url, proxies=self.proxy)
                res = retry(r, 5, 100)
                if res is not None and res.status_code == 200:
                    html = BeautifulSoup(res.content, 'lxml')
                    items_table = html.find('table', {'class': 'lot_list'})
                    yield {
                        'type': 'active_after',
                        'items': [{
                            'data_type': 'link',
                            'link': item.attrs['href']} for item in items_table.find_all('a')]
                    }
                elif res.status_code == 500:
                    break
            # собираем сведения об АРХИВНЫХ тендерах в верстке ДО 17.07.2017, инициализация параметров влож. цикла
            elif i == 2:
                params_key = 'PAGEN_1'
                params = {params_key: 1}
                search_args = 'div', {'class': 'tenders'}
                get_max_pages_func = self.get_max_pages_before
                search_type = 'arc_before'
            # собираем сведения об АКТИВНЫХ тендерах в верстке ДО 17.07.2017
            elif False and i == 3:
                r = get(url, proxies=self.proxy)
                res = retry(r, 5, 100)
                if res is not None and res.status_code == 200:
                    html = BeautifulSoup(res.content, 'lxml')
                    items_table = html.find('div', {'class': 'tenders'})
                    yield {
                        'type': 'active_before',
                        'items': items_table
                    }
                elif res.status_code == 500:
                    break
            # цикл перебора многостраничных данных
            if i == 0 or i == 2:
                while True:
                    #print(params, max_pages)
                    r = get(url, params=params, proxies=self.proxy)
                    res = retry(r, 5, 100)
                    if res is not None and res.status_code == 200:
                        html = BeautifulSoup(res.content, 'lxml')
                        if not max_pages:
                            max_pages = get_max_pages_func(html)
                        items_table = html.find(*search_args)
                        yield {
                            'type': search_type,
                            'items': items_table
                        }
                        if params[params_key] < max_pages:
                            params[params_key] += 1
                        else:
                            break
                    elif res.status_code == 500:
                        break

    def get_tender_data(self, url):
        """данные отдельного тендера"""
        r = get(url, proxies=self.proxy)
        res = retry(r, 5, 100)
        if res is not None and res.status_code == 200:
            html = BeautifulSoup(res.content, 'lxml')
            return html
        return None

    def get_organization(self, customers):
        result = []
        for customer in customers:
            # заглушка
            if customer['name'] is None:
                return [None]
            result.append(
                {
                    'guid': None,
                    'name': customer['name'],
                    'region': None
                }
            )
        return result
            # url = 'http://organizationHost/organization?inn={}&kpp={}&name={}'.format(
            #   customer['inn'], customer['kpp'], customer['name'])
            # r = requests.get(url)
            # return r.json()
