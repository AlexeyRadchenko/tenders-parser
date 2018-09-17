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
        'http://irkutskoil.ru/tenders/type/?archive=N',
        'http://irkutskoil.ru/tenders/type/?archive=Y'
    ]

    def get_max_pages(self, html):
        pagination = html.find('div', {'class': 'multip'}).find_all('a')
        print(pagination)
        if pagination:
            max_pages = re.search(r'\d+', pagination[8].attrs['href'])
            return int(max_pages.group(0))

    def get_tender_list(self):
        """генератор списков тендеров"""
        for i, url in enumerate(self.source_url_list):
            # собираем сведения об архивных тендерах в верстке после 17.07.2017
            if i == 0:
                params = {'cpage': 1}
                max_pages = None
                while True:
                    print(params, max_pages)
                    r = get(url, params=params, proxies=self.proxy)
                    res = retry(r, 5, 100)
                    if res is not None and res.status_code == 200:
                        html = BeautifulSoup(res.content, 'lxml')
                        if not max_pages:
                            max_pages = self.get_max_pages(html)
                        items_table = html.find('table', {'class': 'lot_list'})
                        yield {
                            'type': 'arc_after',
                            'items': items_table
                        }
                        if params['cpage'] < max_pages:
                            params['cpage'] += 1
                        else:
                            break
                    elif res.status_code == 500:
                        break
            # собираем сведения об активных тендерах в верстке после 17.07.2017
            elif i == 1:
                pass

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
