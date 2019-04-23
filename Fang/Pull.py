import json
import random
import re
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor

import requests


class Pull:
    def __init__(self, base_url="https://zu1.fang.com"):
        self.base_url = base_url
        self.mutex = threading.Lock()
        self.pool = ThreadPoolExecutor(max_workers=16)
        self.random_header()
        self.last_input_captcha_time = time.time()

    def captcha_detect(self, res):
        return False
        # self.mutex.acquire()
        # if res.url.find('captcha-verify') != -1:
        #     if time.time() - self.last_input_captcha_time < 20:
        #         self.mutex.release()
        #         return True
        #     print("Please open browser to verify.")
        #     input()
        #     self.last_input_captcha_time = time.time()
        #     self.mutex.release()
        #     return True
        # else:
        #     self.mutex.release()
        #     return False

    def pull_single_page(self, url):
        self.random_header()
        res = self.session.get(url)
        text = res.text

        if self.captcha_detect(res):
            return self.pull_single_page(url)

        search_result = re.findall(
            '<p class="title" id="(.*?)">(.*?)<a href="(.*?)"(.*?)target="_blank" title="(.*?)">(.*?)</a>(.*?)</p>',
            text, re.M | re.S)

        return_data = []

        for single_result in search_result:
            detail = self.pull_detail(single_result[2])
            return_data.append({'url': single_result[2], 'name': single_result[5], 'address': detail['address'],
                                'longitude': detail['codex'], 'latitude': detail['codey'],
                                'price': detail['price'], 'area': detail['buildingArea']})

        return return_data

    def pull_area(self, url, retry=False):
        self.random_header()
        res = self.session.get(url)
        text = res.text

        if self.captcha_detect(res):
            return self.pull_area(url)

        return_data = []
        data = re.findall('<a href="(.*?)" >(.*?)</a>',
                          re.findall('<dt>区域：</dt>(.*?)不限</a>(.*?)</dd>', text, re.M | re.S)[0][1],
                          re.M | re.S)
        if len(data) == 0 and not retry:
            return self.pull_area(url, True)

        for single_data in data:
            return_data.append({'url': single_data[0], 'name': single_data[1]})

        return return_data

    def pull_sub_area(self, url, retry=False):
        self.random_header()
        res = self.session.get(url)
        text = res.text

        if self.captcha_detect(res):
            return self.pull_sub_area(url)

        return_data = []
        data = re.findall('<a href="(.*?)" >(.*?)</a>',
                          re.findall('<div class="quYu" id="(.*?)">(.*?)不限</a>(.*?)</div>', text,
                                     re.M | re.S)[0][2],
                          re.M | re.S)

        if len(data) == 0 and not retry:
            return self.pull_sub_area(url, True)

        for single_data in data:
            return_data.append({'url': single_data[0], 'name': single_data[1]})

        return return_data

    def pull_atom_area_page(self, url):
        self.random_header()
        res = self.session.get(url)
        text = res.text

        if self.captcha_detect(res):
            return self.pull_atom_area_page(url)

        try:
            return int(re.findall('共(\d+)页',
                                  text,
                                  re.M | re.S)[0])
        except:
            return 1

    def pull_detail(self, url, retry=False):
        self.random_header()
        res = self.session.get(self.base_url + url)
        text = res.text

        if self.captcha_detect(res):
            return self.pull_detail(url)

        search_result = re.findall(
            'var houseInfo = \{(.*?)\}',
            text, re.M | re.S)

        if len(search_result) == 0 and not retry:
            return self.pull_detail(url, True)

        text = search_result[0].replace('\n', '')
        text = text.replace('\r', '')

        text = re.sub("(\w+): '(.*?)'", r'"\1": "\2"', '{' + text + '}')
        text = re.sub("(\w+): \"(.*?)\"", r'"\1": "\2"', text)
        text = re.sub(",(( )*?)}", r'}', text)
        text = re.sub("\/\/ new  add by wys", r'', text)
        return json.loads(text)

    def pull_single_and_insert(self, url, db_object, retry=False):
        data = self.pull_single_page(url)

        if len(data) == 0 and not retry:
            print('Zero Data: ' + url)
            return self.pull_single_and_insert(url, db_object, True)

        for single_data in data:
            db_object.insert(single_data['name'], single_data['address'], single_data['longitude'],
                             single_data['latitude'], single_data['price'], single_data['area'])

    def random_header(self):
        self.session = requests.Session()
        # proxies = {'http': 'http://127.0.0.1:8001', 'https': 'http://127.0.0.1:8001'}
        # self.session.proxies.update(proxies)
        head_user_agent = [
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',
            'Googlebot/2.1 (+http://www.google.com/bot.html)'
        ]
        self.session.headers.update({
            'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
        })

    def pull_atom_area_and_insert(self, atom_area, db_object):
        page_num = self.pull_atom_area_page(self.base_url + atom_area['url'])

        for i in range(1, page_num + 1):
            self.pull_single_and_insert(self.base_url + atom_area['url'] + '/i3' + str(
                i), db_object)

    def pull_and_insert(self, db_object):
        self.pull_single_and_insert("https://zu1.fang.com/house-a010-b02721//i33", db_object)

        # areas = self.pull_area(self.base_url)
        # print(areas)
        #
        # for sub_area in areas:
        #     atom_areas = self.pull_sub_area(self.base_url + sub_area['url'])
        #     print(atom_areas)
        #
        #     for atom_area in atom_areas:
        #         print('Pulling ' + atom_area['name'])
        #
        #         self.pool.submit(self.pull_atom_area_and_insert, atom_area, db_object)
        #
        # self.pool.shutdown(True)
