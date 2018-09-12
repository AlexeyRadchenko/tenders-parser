from src.bll.retrier import retry
from requests import get
from bs4 import BeautifulSoup


class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    source_url = 'http://supply.evraz.com'
    tender_modal_window = {
        'modalWindow': 'Y'
    }

    def get_tender_list(self):
        r = get(self.source_url, proxies=self.proxy)
        res = retry(r, 5, 100)
        if res is not None and res.status_code == 200:
            html = BeautifulSoup(res.content, 'lxml')
            items_div_list = html.find_all('div', {'class': 'panel-body'})
            result_url_list = []
            for div in items_div_list:
                links = div.find_all('a')
                result_url_list.extend([self.source_url+url.attrs['url'] for url in links])
            return result_url_list

    def get_tender_data(self, url):
        """данные отдельного тендера"""
        r = get(url, params=self.tender_modal_window, proxies=self.proxy)
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