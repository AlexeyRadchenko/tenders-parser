from src.bll.retrier import retry
from requests import post
from bs4 import BeautifulSoup


class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    source_url = 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Length': '348',
        'Cookie': 'GLOBAL_OBERON=ORA_WWV-GpESRgE_2FIHkeTuN--xgIeZ; _ym_uid=1537952218596738451; _ym_d=1537952218; _ym_visorc_48062852=w; _ga=GA1.2.1475219486.1537952219; _gid=GA1.2.280130067.1537952219; _ym_isad=2',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'X-Requested-With': 'XMLHttpRequest'
    }

    init_request_form_params = {
        'p_flow_id': '220',
        'p_flow_step_id': '562',
        'p_instance': '770888636588',
        'p_request': 'PLUGIN=2076931AFCD50898683D5E431CA90D7BE4DD2032F49C436C328615CB66D07DA0',
        'p_widget_action': 'PAGE',
        'p_widget_action_mod': None,
        'p_widget_mod': 'ACTION',
        'p_widget_name': 'worksheet',
        'p_widget_num_return': '15',
        'x01': '25399118176800742',
        'x02': '25400525673806806',
    }

    def next_page_exist(self, html):
        next_page_selector = html.find('ul', {'class': 'a-IRR-pagination'}).find_all('li')[-1]
        if next_page_selector.attrs.get('aria-hidden'):
            return False
        else:
            return True

    def get_tender_list(self):
        """генератор списков тендеров"""
        page = 1
        while True:
            print(page)
            page_param = 'pgR_min_row={}max_rows=15rows_fetched=15'.format(page)
            self.init_request_form_params['p_widget_action_mod'] = page_param
            r = post(self.source_url, data=self.init_request_form_params, proxies=self.proxy)
            res = retry(r, 5, 100)
            if res is not None and res.status_code == 200:
                html = BeautifulSoup(res.content, 'lxml')
                items_div = html.find('table', {'class': 'a-IRR-table'})
                if items_div:
                    items_data_list = items_div.find_all('tr')[1:]
                    yield items_data_list
                    if not self.next_page_exist(html):
                        break
                    page += 15
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
