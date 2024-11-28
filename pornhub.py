import json
import httpx
import re
import time
from lxml import etree
import pyaria2
import random
import yaml
from curl_cffi import requests

c = yaml.load(open('config.yaml'), yaml.Loader)
rpc = pyaria2.Aria2RPC(url=c['rpc']['url'],token=c['rpc']['token'])
lag = 'www'
dic = {}
cookie = ''
for i in c['cookie']:
    cookie += f'{i}={c["cookie"][i]};'

user_agents = open('uag.txt', 'r').read().split('\n')
user_agent = random.choice(user_agents)

h = {
    'user-agent': user_agent,
    'cookie': cookie,
}

proxy = c['proxy']  # 我这里clash端口7890，v2ray 端口8001

res = requests.Session(proxies=proxy, timeout=5, headers=h)

LOGO = '''

   ___                                    _     
  / _ \ ___   _ __  _ __    /\  /\ _   _ | |__  
 / /_)// _ \ | '__|| '_ \  / /_/ /| | | || '_ \ 
/ ___/| (_) || |   | | | |/ __  / | |_| || |_) |
\/     \___/ |_|   |_| |_|\/ /_/   \__,_||_.__/ 

                                        by laowei
'''


def download(channels, video_url, name):
    options = {
        'http-proxy': proxy['http'],
        'https-proxy': proxy['https'],
        'out': channels + '/' + name
    }  # aria2 设置梯子
    rpc.addUri([video_url], options)


def channels_list(channels, page):
    url = f'https://{lag}.pornhub.com/channels/{channels}/videos?o=ra&page={page}'
    s = res.get(url).text
    html = etree.HTML(s)
    view_keys = html.xpath('//ul[@class="videos row-5-thumbs videosGridWrapper"]/li/@data-video-vkey')
    names = html.xpath('//ul[@class="videos row-5-thumbs videosGridWrapper"]/li/div/div[3]/span/a/@title')
    for i, j in enumerate(view_keys):
        get_video(channels, j, names[i])
        print(j, 'ok')
    return len(view_keys)


def star_list(pornstar, page):
    url = f'https://{lag}.pornhub.com/pornstar/{pornstar}/videos/upload?page={page}'
    s = res.get(url).text
    html = etree.HTML(s)
    view_keys = html.xpath('//ul[@class="videos row-5-thumbs"]/li/@data-video-vkey')
    names = html.xpath('//ul[@class="videos row-5-thumbs"]/li/div/div[3]/span/a/@title')
    for i, j in enumerate(view_keys):
        get_video(pornstar, j, names[i])
        print(j, 'ok')
    return len(view_keys)


def model_list(models, page):
    url = f'https://{lag}.pornhub.com/model/{models}/videos?page={page}'
    s = res.get(url).text
    html = etree.HTML(s)
    view_keys = html.xpath('//ul[@id="mostRecentVideosSection"]/li/@data-video-vkey')
    names = html.xpath('//ul[@id="mostRecentVideosSection"]/li/div/div[3]/span/a/@title')
    for i, j in enumerate(view_keys):
        get_video(models, j, names[i])
        print(j, 'ok')
    return len(view_keys)


def get_video(channels, view_key, name):
    url = f'https://{lag}.pornhub.com/view_video.php?viewkey={view_key}'
    try:
        s = res.get(url).text
        json_data = re.findall('var flashvars_\d+ = (\{.*?});', s)[0]
        urls = json.loads(json_data)['mediaDefinitions']
        nul = urls[-1]['videoUrl']
        video_url = ''
        count = 0
        while video_url == '':
            video_url = res.get(nul).json()[count - 1]['videoUrl']
            count = count - 1
            if count < -3:
                break

        download(channels, video_url, name + '.mp4')
        time.sleep(2)
    except Exception as err:
        print(err)
        time.sleep(2)
        pass


def chanel(channels):
    count = 36
    page = 1
    while count == 36:
        count = channels_list(channels, page)
        page += 1


def star(pornstar):
    count = 40
    page = 1
    while count == 40:
        count = star_list(pornstar, page)
        page += 1


def model(models):
    count = 40
    page = 1
    while count == 40:
        count = model_list(models, page)
        page += 1


if __name__ == '__main__':
    print(LOGO)
    input_address = input('地址').split('/')
    if input_address[3] == 'model':
        model(input_address[4])
    elif input_address[3] == 'pornstar':
        star(input_address[4])
    elif input_address[3] == 'channels':
        chanel(input_address[4])
