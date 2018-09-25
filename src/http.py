from src.bll.retrier import retry
from requests import get
from bs4 import BeautifulSoup


class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    source_url_list = [
        'http://www.uralchem.ru/purchase/tenders/',
        'http://www.uralchem.ru/purchase/tenders_Ariba/'
    ]
    param_for_tenders = {
        'PAGEN_1': 1,  # открытые
        'PAGEN_2': 1,  # завершенне
    }
    param_for_tenders_Ariba = {
        'PAGEN_2': 1,  # открытые
        'PAGEN_3': 1,  # завершенне
    }

    def next_page_exist(self, html, data_id):
        return html.find(
            'div', {'data-id': data_id}
        ).find('ul', {'class': 'pagination-list'}).find('li', {'class': 'next'})

    def get_tender_list(self):
        """генератор списков тендеров"""
        for i, url in enumerate(self.source_url_list):
            for tenders_type in ['open', 'close']:
                params = None
                if tenders_type == 'open' and i == 0:
                    params = {'PAGEN_1': 1,}
                    params_key = 'PAGEN_1'
                    data_id = 'tab-1'
                elif tenders_type == 'close' and i == 0:
                    params = {'PAGEN_2': 1,}
                    params_key = 'PAGEN_2'
                    data_id = 'tab-2'
                elif tenders_type == 'open' and i == 1:
                    params = {'PAGEN_2': 1, }
                    params_key = 'PAGEN_2'
                    data_id = 'tab-1'
                elif tenders_type == 'close' and i == 1:
                    params = {'PAGEN_3': 1, }
                    params_key = 'PAGEN_3'
                    data_id = 'tab-2'
                while True:
                    r = get(url, params=params, proxies=self.proxy)
                    res = retry(r, 5, 100)
                    if res is not None and res.status_code == 200:
                        html = BeautifulSoup(res.content, 'lxml')
                        print(self.next_page_exist(html, data_id))
                        items_div = html.find('div', {'data-id': data_id})
                        if items_div:
                            items_data_list = items_div.find_all('div', {'class': 'tenders-item'})
                            yield items_data_list, i, url, params_key, params[params_key]
                            if not self.next_page_exist(html, data_id):
                                break
                            else:
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
