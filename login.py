import httpx
import re
import yaml
import requests.utils as res_ut
from urllib.parse import quote
from curl_cffi import requests

proxy = {
    # 'http':'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}
lag = 'www'
h = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
}
res = requests.Session(proxies=proxy, headers=h)
config = yaml.load(open('cookie.yaml'), yaml.Loader)['login']


def login():
    url = 'https://cn.pornhub.com/'
    s = res.get(url).text
    token = re.findall('token\s*?= "([^"]+)"', s)[0]
    redirect = re.findall('login\?redirect=([^"]+)"', s)[0]
    url2 = 'https://cn.pornhub.com/front/authenticate'
    d = f'redirect={redirect}&user_id=&intended_action=&token={token}&from=pc_login_modal_%3Aindex&taste_profile=&username={config["username"]}&password={quote(config["password"])}&remember_me=on'
    res.post(url2, data=d)
    cookie = res.cookies.jar
    cookie_dic = res_ut.dict_from_cookiejar(cookie)
    w = open('cookie.yaml', 'w+')
    yaml.dump({'cookie': cookie_dic, 'login': config}, w)


login()
