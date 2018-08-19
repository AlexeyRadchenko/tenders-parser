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
        'http://zakupki.gazprom-neft.ru/tenderix/index.php',
        'http://zakupki.gazprom-neft.ru/tenderix/prequalification.php'
    ]

    init_params = {
        'PAGE': 1,
        #'FILTER[STATE]': 'ALL'
    }

    def get_tender_list(self):
        """генератор списков тендеров"""
        for url in self.source_url_list:
            while True:
                print(self.init_params)
                r = get(url, proxies=self.proxy, params=self.init_params)
                res = retry(r, 5, 100)
                if res is not None and res.status_code == 200:
                    html = BeautifulSoup(res.content, 'lxml')
                    items_div_exist = html.find('ul', {'class': 'pagination'})
                    if items_div_exist:
                        items_data_list = html.find('div', {'id': 'listOutBuyTender'}).find_all('article')
                        yield items_data_list
                        self.init_params['PAGE'] += 1
                    else:
                        self.init_params['PAGE'] = 1
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