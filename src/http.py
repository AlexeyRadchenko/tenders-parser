from src.bll.retrier import retry
from requests import post


class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    tenders_source_url_list = [
        'https://www.nornickel.ru/ajax/tenders-centralized.php',
        'https://www.nornickel.ru/ajax/tenders-local.php'
    ]

    init_request_form_data = {
        'draw': '1',
        'length': '100',
        'search[regex]': 'false',
        'search[value]': '',
        'start': '0'
    }

    def reset_param(self):
        self.init_request_form_data['draw'] = '1'
        self.init_request_form_data['start'] = '0'
        return 0

    def get_tender_list(self):
        """генератор списков тендеров"""
        records = 0
        for i, url in enumerate(self.tenders_source_url_list):
            while True:
                r = post(url, data=self.init_request_form_data, proxies=self.proxy)
                res = retry(r, 5, 100)
                if res is not None and res.status_code == 200:
                    data = res.json()
                    records += len(data['data'])
                    #print(records, data['recordsTotal'])
                    #print(data)
                    yield data['data']
                    if records < int(data['recordsTotal']):
                        self.init_request_form_data['draw'] = str(int(self.init_request_form_data['draw']) + 1)
                        self.init_request_form_data['start'] = str(int(self.init_request_form_data['start']) + 100)
                    elif records >= int(data['recordsTotal']) and self.init_request_form_data.get('archive') is None:
                        self.init_request_form_data['archive'] = 'true'
                        records = self.reset_param()
                    else:
                        del self.init_request_form_data['archive']
                        records = self.reset_param()
                        break

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

