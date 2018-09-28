from src.bll.retrier import retry
from requests import get, post, Session
from bs4 import BeautifulSoup
import re


class Http:
    def __init__(self, proxy=None):
        if proxy and proxy.get('enabled'):
            self.proxy = proxy
        else:
            self.proxy = None

    session_and_params_init_url = 'https://etp.tatneft.ru/pls/tzp/f?p=220:562:::::' \
                                  'P562_OPEN_MODE,GLB_NAV_ROOT_ID,GLB_NAV_ID:,12920020,12920020'

    switch_url = 'https://etp.tatneft.ru/pls/tzp/wwv_flow.accept'

    get_data_url = 'https://etp.tatneft.ru/pls/tzp/wwv_flow.show'

    switch = {
        'p_flow_id': '220',
        'p_flow_step_id': '562',
        'p_instance': None,  # палучаем параметр после создание сессии, обязателен !
        'p_page_submission_id': None,  # палучаем параметр после создание сессии, обязателен !
        'p_request': 'P562_STATE',
        'p_arg_names': ['10532953143930147', '10534736305934762', '10535342538936485', '10535948079938095',
                        '24971825244917975', '26372130093113705', '1437807258407274', '77340431388563902',
                        '45808826609401811', '45809533882403910', '12683322157747701', '16945835513307812',
                        '23308440874903678', '18242524906460956', '16946623093332668', '20314841512322654',
                        '27125454544558788', '77524428635937367', '77552410877042629', '77524700153948142',
                        '77543707705237610', '80658314736165424'
                        ],
        'p_t08': '-100',
        'p_t18': '174738740000',
        'p_t19': '0',
        'p_t20': 'ALL', # основновй параметр для вывода текущи/всех/закрытых тендеров, обязателен !
        'p_arg_checksums': None,  # палучаем параметр после создание сессии, обязателен !
        'p_page_checksum': None,  # палучаем параметр после создание сессии, обязателен !
    }

    init_request_form_params = {
        'p_flow_id': '220',
        'p_flow_step_id': '562',
        'p_instance': None,  # палучаем параметр после создание сессии, обязателен !
        'p_request': None,  # палучаем параметр после создание сессии, обязателен !
        'p_widget_action': 'PAGE',
        'p_widget_action_mod': None,  # переметр с номером страницы, и количестовом элементов на ней , обязателен !
        'p_widget_mod': 'ACTION',
        'p_widget_name': 'worksheet',
        'p_widget_num_return': None,  # параметр с количестовм элементов , обязателен !
        'x01': '25399118176800742',
        'x02': '25400525673806806',
    }
    """пример параметров для запроса 100 строк для первой и второй страницы
    'p_widget_action_mod': 'pgR_min_row=1max_rows=25rows_fetched=25',
    'p_widget_num_return': '25', запрос первой страницы по 25 строк
    
    'p_widget_action_mod': 'pgR_min_row=26max_rows=25rows_fetched=25',
    'p_widget_num_return': '25', запрос второй страницы по 25 строк
    """
    def next_page_exist(self, html):
        next_page_selector = html.find('ul', {'class': 'a-IRR-pagination'}).find_all('li')[-1]
        if next_page_selector.attrs.get('aria-hidden'):
            return False
        else:
            return True

    def get_pulgin_identifier(self, js_string):
        ident = re.findall(r'"\w{64}"', js_string)
        if ident:
            return ident[-1].strip('"')

    def get_session_params(self, response):
        html = BeautifulSoup(response, 'lxml')
        sub_ident = html.find('input', {'name': 'p_page_submission_id'}).attrs['value']
        page_check_sum = html.find('input', {'name': 'p_page_checksum'}).attrs['value']
        page_arg_checsums = html.find('input', {'name': 'p_arg_checksums'}).attrs['value']
        url = html.find('ul', {'class': 'dhtmlMenuLG2'}).find_all('li')[1].find('a').attrs['href']
        ajax_identifier = self.get_pulgin_identifier(html.find_all('script')[-1].text)
        return url.split(':')[2], sub_ident, page_check_sum, page_arg_checsums, ajax_identifier

    def get_tender_list(self, quantity_items=15):
        """генератор списков тендеров"""
        with Session() as session:
            """сервер etp.tatneft.ru создает сессию и инциализирует идентификаторы для запросов, если их не установить, то будем
            получать ошибку. Если запросов не поступает определенное время, сервер сессию закрывает. Для каждой новой
            сессии - параметры будут сгенерированы сервером заново и будут отличатся.
            """
            params_response = session.get(self.session_and_params_init_url, proxies=self.proxy)
            instance_id, submission_id, p_check_sum, p_arg_checksum, ajax_identifier = self.get_session_params(
                params_response.content
            )
            # устанавливаем параметры для переключения на запросы из полного списка тендеров
            self.switch['p_instance'] = instance_id
            self.switch['p_page_submission_id'] = submission_id
            self.switch['p_page_checksum'] = p_check_sum
            self.switch['p_arg_checksums'] = p_arg_checksum

            session.post(self.switch_url, data=self.switch, proxies=self.proxy)

            self.init_request_form_params['p_instance'] = instance_id
            self.init_request_form_params['p_request'] = 'PLUGIN={}'.format(ajax_identifier)
            self.init_request_form_params['p_widget_num_return'] = str(quantity_items)
            last_show_item_num = 1
            while True:
                print(last_show_item_num)
                p_widget_action_mod = 'pgR_min_row={0}max_rows={1}rows_fetched={1}'.format(
                    last_show_item_num, quantity_items
                )
                self.init_request_form_params['p_widget_action_mod'] = p_widget_action_mod
                r = session.post(self.get_data_url, data=self.init_request_form_params, proxies=self.proxy)
                res = retry(r, 5, 100)
                if res is not None and res.status_code == 200:
                    html = BeautifulSoup(res.content, 'lxml')
                    items_div = html.find('table', {'class': 'a-IRR-table'})
                    if items_div:
                        items_data_list = items_div.find_all('tr')[1:]
                        yield items_data_list
                        if not self.next_page_exist(html):
                            break
                        last_show_item_num += quantity_items
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
