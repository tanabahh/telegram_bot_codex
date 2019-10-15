import time
import requests
from yaml import safe_load
from lxml import html
from datetime import datetime
#from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.triggers.combining import AndTrigger
#from apscheduler.triggers.interval import IntervalTrigger
#from apscheduler.triggers.cron import CronTrigger


#httpsProxy = "https://118.97.151.130:9090"
#httpProxy = "http://210.212.73.61:80"

#prox = {
#    "http": httpProxy,
#    "https": httpsProxy
#}

#разбор конфига
with open("config", 'r') as config_file:
    config_dict = safe_load(config_file)

tasks = config_dict["tasks"]
tasks = tasks[0]
url = tasks["url"]
xpath = tasks["xpath"]
max_secs = tasks["max-secs-without-changes"]
message_first = tasks["messages"]['first']
message_second = tasks["messages"]['second']
message_finish = tasks["messages"]['finish']
schedule = tasks['schedule']


#поиск нужного элемента для считывания времени последнего поста
def find(url, xpath, proxies= None):
    response = requests.get(url, proxies=proxies).text
    tree = html.fromstring(response)
    elem = tree.xpath(xpath)
    element = html.tostring(elem[0])
    return element

#проверка был ли пост
def check_post():
    elem = find(url, xpath)
    post_date = hash(elem)  # сохранять хэш проверять время сравнивать не по времени!
    f = open('hash.txt', 'r')
    hashfile = []
    for line in f:
        hashfile.append(line)
    if post_date == hashfile[0]:
        hashfile[1] = datetime.strptime(hashfile[1], "%Y-%m-%d+%H:%M:%S")
        return hashfile[1] - datetime.now() >= max_secs
    else:
        updatefile(post_date)
        return False

def updatefile(post_date):
    f = open('hash.txt', 'w')
    f.write(str(post_date)+'\n'+str(datetime.now()))


#бот
def manager():
    if check_post():
        webhook = 'https://notify.bot.codex.so/u/H97FIRDA'
        requests.post(webhook, data={"message": message_first[0].encode('cp1251')})

#scheduler = BackgroundScheduler()
#trigger = AndTrigger([IntervalTrigger(hours=1), CronTrigger(day_of_week='sat,sun')])
#scheduler.add_job(manager(), trigger)

manager()

