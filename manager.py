# -*- coding: utf-8 -*-
import requests
from yaml import safe_load
from lxml import html
from datetime import datetime
httpsProxy = "https://118.97.151.130:9090"
httpProxy = "http://210.212.73.61:80"

prox = {
    "http": httpProxy,
    "https": httpsProxy
}

with open("config", 'r') as config_file:
    config_dict = safe_load(config_file)

tasks = config_dict["tasks"]
tasks = tasks[0]
url = tasks["url"]
xpath = tasks["xpath"]
max_secs = tasks["max-secs-without-changes"]
message = tasks["messages"]
def find(url, xpath, proxies= None):
    response = requests.get(url, proxies=proxies).text
    tree = html.fromstring(response)
    elem = tree.xpath(xpath)
    return elem

elem = find(url, xpath,proxies=prox)
post_date = elem[0].attrib['datetime']
def check_post(post_date):
    date_pattern = "%Y-%m-%dT%H:%M:%S"
    post_date = datetime.strptime(post_date.split("+")[0], date_pattern)
    delta = datetime.now() - post_date
    return delta.total_seconds() >= max_secs
check_post(post_date)
webhook = 'https://notify.bot.codex.so/u/H97FIRDA'
requests.post(webhook, data={"message":message.encode('cp1251')})