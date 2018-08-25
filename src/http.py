from src.bll.retrier import retry
from requests import post
from bs4 import BeautifulSoup


class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    source_url = 'https://zakupki.tmk-group.com/index.php'

    init_tenders_list_request_params = {
        'module': 'default',
        'rpctype': 'direct'
    }

    init_tenders_list_request_json = {
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

    init_tender_data_reauest_params = {
        'module': 'tmk',
        'rpctype': 'direct'
    }

    init_tender_data_request_json = {
        'action': 'Procedure',
        'data': [{
            'is_peretorg_view': False,
            'is_view': 1,
            'procedure_id': None,
        }],
        'jsversion': 387,
        'method': 'load',
        'tid': 1,
        'token': 'ZqbdFGbG5dA+K+zoIfxn7w',
        'type':	'rpc'
    }

    def get_tender_list(self):
        """генератор списка тендеров в формате JSON"""
        while True:
            r = post(
                self.source_url,
                params=self.init_tenders_list_request_params,
                json=self.init_tenders_list_request_json,
                proxies=self.proxy
            )
            res = retry(r, 5, 100)
            if res is not None and res.status_code == 200:
                result = res.json()
                total = result['result']['totalCount']
                print(total, total - self.init_tenders_list_request_json['data'][0]['start'])
                yield result['result']['procedures']
                if total - self.init_tenders_list_request_json['data'][0]['start'] > 25:
                    self.init_tenders_list_request_json['data'][0]['start'] += 25
                else:
                    self.init_tenders_list_request_json['data'][0]['start'] = 0
                    break

    def get_tender_data(self, tender_id):
        """данные отдельного тендера"""
        self.init_tender_data_request_json['data'][0]['procedure_id'] = tender_id
        r = post(
            self.source_url,
            params=self.init_tender_data_reauest_params,
            json=self.init_tender_data_request_json,
            proxies=self.proxy
        )
        res = retry(r, 5, 100)
        if res is not None and res.status_code == 200:
            result = res.json()
            return result['result']['procedure']

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
