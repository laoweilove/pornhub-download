import re
from urllib.parse import quote

import httpx
import requests.utils as rus
import yaml
from curl_cffi import requests


lag = 'www'
h = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
}
config = yaml.load(open('config.yaml'), yaml.Loader)
proxy = config['proxy']
res = requests.Session(proxies=proxy, timeout=5, headers=h)



def login():
    url = 'https://cn.pornhub.com/'
    s = res.get(url).text
    token = re.findall('token\s*?= "([^"]+)"', s)[0]
    redirect = re.findall('login\?redirect=([^"]+)"', s)[0]
    url2 = 'https://cn.pornhub.com/front/authenticate'
    d = f'redirect={redirect}&user_id=&intended_action=&token={token}&from=pc_login_modal_%3Aindex&taste_profile=&username={config["login"]["username"]}&password={quote(config["login"]["password"])}&remember_me=on'
    res.post(url2,data=d)
    cookie = res.cookies.jar
    cookie_dic = rus.dict_from_cookiejar(cookie)
    config.update({'cookie': cookie_dic})
    w = open('config.yaml', 'w+')
    yaml.dump(config, w)


login()
