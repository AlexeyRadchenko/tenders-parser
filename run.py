from time import sleep
from src.collector import Collector
from settings import sleep_time


if __name__ == "__main__":
    collector = Collector(quantity=None, publish_date=None, base_url='https://www.uralmash.ru')
    while True:
        collector.collect()
        break
        #sleep(sleep_time)
