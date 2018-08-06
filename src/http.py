from src.bll.retrier import retry
from requests import get
from bs4 import BeautifulSoup


class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    source_url = 'https://etpgpb.ru/procedures/page/{}/?procedure[category]=actual&procedure[section][0]' \
                 '=common&procedure[section][1]=gazprom'

    def get_tender_list(self):
        """генератор списков тендеров"""
        page = 36
        while True:
            #print(page)
            page_url = self.source_url.format(page)
            r = get(page_url, proxies=self.proxy)
            res = retry(r, 5, 100)
            if res is not None and res.status_code == 200:
                html = BeautifulSoup(res.content, 'lxml')
                #items_div = html.find('div', class_='block__related block__related_big hidden')
                items_div = html.find('div', {'data-view': 'full'})
                if items_div:
                    items_data_list = items_div.find_all('a')
                    yield items_data_list
                    page += 1
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
