import json

with open('config.json', 'r', encoding='utf8') as cfg:
    config = json.load(cfg)

mongodb = config['mongodb']
rabbitmq = config['rabbitmq']
proxy = config['proxy']
sleep_time = config['sleep_time']
