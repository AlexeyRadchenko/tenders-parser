from src.bll.retrier import retry
from requests import get
from bs4 import BeautifulSoup


class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    source_url = 'https://www.uralmash.ru/tenders/'
    init_request_params = {
        'PAGEN_1': 1
    }

    def get_max_pages(self, data_html):
        return int(data_html.find('ul', {'class': 'pagination'}).find_all('a')[-2:][0].text)

    def get_tender_list(self):
        """генератор списков тендеров"""
        max_pages = None
        while True:
            r = get(self.source_url, params=self.init_request_params, proxies=self.proxy)
            res = retry(r, 5, 100)
            if res is not None and res.status_code == 200:
                html = BeautifulSoup(res.content, 'lxml')
                items_div = html.find('div', {'class': 'newsWrapper'})
                if not max_pages:
                    max_pages = self.get_max_pages(html)
                print(self.init_request_params['PAGEN_1'], max_pages)
                if items_div and self.init_request_params['PAGEN_1'] <= max_pages:
                    items_data_list = items_div.find('div', {'class': 'row'}).find_all('div', {'class': 'newsItem'})
                    yield items_data_list
                    self.init_request_params['PAGEN_1'] += 1
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
