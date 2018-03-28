# -*- coding: UTF-8 -*-
import requests
import re
import random
import time
from collections import deque
from urllib.parse import *


# judge the eligible url
def judge_url(url, url_set, queue):
    in_queue = False
    for i in queue:
        if url.address == i.address:
            in_queue = True
            break
    if url.address in url_set or in_queue == True:
        return False
    elif ('g20chn.org' in url.address or 'g20chn.com' in url.address) and 'English' not in url.address:
        return True
    else:
        return False


class Url(object):
    def __init__(self, address, page=False):
        self.address = address
        self.page = page

    def get_address(self):
        if self.page:
            if 'index_' not in self.address:
                return re.sub(r'index.html','index_1.html',self.address)
            else:
                temp = re.findall(r'/index_(.).html',self.address)
                temp = str(int(temp[0]) + 1)
                return re.sub(r'index_(.).html','index_' + temp + '.html',self.address)
        else:
            return self.address


# visit urls by BFS
url_queue = deque()
visited = set()
count = 0
url = Url('http://g20chn.org/')
url_queue.append(url)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}
session = requests.Session()
session.get(url.address, headers=headers, timeout=5)

while url_queue and count <= 10000:
    url = url_queue.popleft()
    print('已经爬取: ' + str(count) + '   正在爬取 <---  ' + url.address)
    visited |= {url.address}
    try:
        r = session.get(url.address, headers=headers, timeout=5)
    except:
        continue

    # judge whether url points to a web page.
    if 'Content-Type' in r.headers and 'html' in r.headers['Content-Type']:
        data = r.text
        if '<div id="pages">' in data:
            url.page = True
        pre_url = Url(url.get_address())
        if judge_url(pre_url, visited, url_queue):
            url_queue.append(pre_url)
            print('add into urls to be visited ->' + pre_url.address)
        count += 1
        with open(r'D:\spider\data\text{}.txt'.format(count), 'w', encoding='utf-8') as f:
            f.write(data)
    else:
        continue

    for pre_url in re.findall('href="(.+?)"',data):
        pre_url = Url(urljoin(r.url, pre_url))
        if judge_url(pre_url, visited, url_queue):
            url_queue.append(pre_url)
            print('add into urls to be visited ->' + pre_url.address)
