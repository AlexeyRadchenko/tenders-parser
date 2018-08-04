from src.bll.retrier import retry
from requests import get
from bs4 import BeautifulSoup


class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    source_url = 'http://www.zakupki.bgkrb.ru/purchase/'

    init_params = {
        'catalog_filter': 151,
        'PAGEN_1': 1, #1207
    }

    def get_tender_list(self):
        """генератор списков тендеров"""
        while True:
            r = get(self.source_url, params=self.init_params, proxies=self.proxy)
            res = retry(r, 5, 100)
            if res is not None and res.status_code == 200:
                html = BeautifulSoup(res.content, 'lxml')
                next_page_exist = html.find('a', class_='paginator_list_right')
                print(next_page_exist, self.init_params['PAGEN_1'])
                if next_page_exist:
                    yield html.find('div', class_='news-list').find_all('tr')
                    self.init_params['PAGEN_1'] += 1
                else:
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
