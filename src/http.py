from src.bll.retrier import retry
from requests import post
from bs4 import BeautifulSoup
import json


class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    source_url = 'https://zakupki.tmk-group.com/index.php'

    init_request_params = {
        'module': 'default',
        'rpctype': 'direct'
    }
    init_request_json = {
        'action': 'Procedure',
        'data': [{
            'dir': 'DESC',
            'limit': 25,
            'sort': 'id',
            'start': 0
        }],
        'jsversion': 387,
        'method': 'list',
        'tid': 7,
        'token': 'ZqbdFGbG5dA + K + zoIfxn7w',
        'type': 'rpc'
    }

    def get_tender_list(self):
        """генератор списка тендеров в формате JSON"""
        while True:
            r = post(self.source_url, params=self.init_request_params, json=self.init_request_json, proxies=self.proxy)
            res = retry(r, 5, 100)
            if res is not None and res.status_code == 200:
                result = r.json()
                total = result['result']['totalCount']
                print(total, total - self.init_request_json['data'][0]['start'])
                yield result['result']['procedures']
                if total - self.init_request_json['data'][0]['start'] > 25:
                    self.init_request_json['data'][0]['start'] += 25
                else:
                    self.init_request_json['data'][0]['start'] = 0
                    break
        """
        while True:
            #print(page)
            #page_url = self.source_url.format(page)
            r = get(self.source_url, params=self.init_request_params, json=self.init_request_json,  proxies=self.proxy)
            res = retry(r, 5, 100)
            if res is not None and res.status_code == 200:
                html = BeautifulSoup(res.content, 'lxml')
                items_div = html.find('div', {'data-view': 'full'})
                if items_div:
                    items_data_list = items_div.find_all('a')
                    yield items_data_list
                    page += 1
                else:
                    break
            elif res.status_code == 500:
                break"""

    def get_tender_data(self, url):
        """данные отдельного тендера"""
        r = post(url, proxies=self.proxy)
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
