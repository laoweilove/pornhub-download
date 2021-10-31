import requests
import re,time
from lxml import etree
import execjs
import pyaria2
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry

res = requests.Session()
res.mount('https://', HTTPAdapter(max_retries=Retry(total=5, method_whitelist=frozenset(['GET', 'POST']))))
rpc=pyaria2.Aria2RPC()#aria2rpc设置，默认6800端口，没密钥

dic={}
proxy={
    #'http':'http://127.0.0.1:7890',
    'https':'https://127.0.0.1:7890'
} #我这里clashx端口7890，v2ray 端口8001

cookie=open('cookie.txt','r').read()#自行粘贴cookie到同目录下cookie.txt
h={

    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67',
    'cookie': cookie,
}

def download(chanels,s,name):
    opin={'http-proxy':'http://127.0.0.1:7890','https-proxy':'https://127.0.0.1:7890','out':chanels+'/'+name}#aria2 设置梯子
    rpc.addUri([s], opin)

def getchannelslist(chanels,page):
    url='https://cn.pornhub.com/channels/'+chanels+'/videos?o=ra&page='+str(page)
    s=res.get(url,headers=h,proxies=proxy).text
    html = etree.HTML(s)
    vkeys = html.xpath('//ul[@class="videos row-5-thumbs videosGridWrapper"]/li/@data-video-vkey')
    names=html.xpath('//ul[@class="videos row-5-thumbs videosGridWrapper"]/li/div/div[3]/span/a/@title')
    for i,j in enumerate(vkeys):
        getvideo(chanels,j,names[i])
        print(j,'ok')
    return len(vkeys)

def starlist(star,page):
    url='https://cn.pornhub.com/pornstar/'+star+'/videos/upload?page='+str(page)
    s = res.get(url, headers=h, proxies=proxy).text
    html = etree.HTML(s)
    vkeys = html.xpath('//ul[@class="videos row-5-thumbs"]/li/@data-video-vkey')
    names = html.xpath('//ul[@class="videos row-5-thumbs"]/li/div/div[3]/span/a/@title')
    for i, j in enumerate(vkeys):
        getvideo(star, j, names[i])
        print(j, 'ok')
    return len(vkeys)

def modellist(model,page):
    url='https://cn.pornhub.com/model/'+model+'/videos?page='+str(page)
    s = res.get(url, headers=h, proxies=proxy).text
    html = etree.HTML(s)
    vkeys = html.xpath('//ul[@id="mostRecentVideosSection"]/li/@data-video-vkey')
    names = html.xpath('//ul[@id="mostRecentVideosSection"]/li/div/div[3]/span/a/@title')
    for i, j in enumerate(vkeys):
        getvideo(model, j, names[i])
        print(j, 'ok')
    return len(vkeys)

def getvideo(chanels,viewkey,name):
    url='https://'+lag+'.pornhub.com/view_video.php?viewkey='+viewkey
    try:


        s=res.get(url,headers=h,timeout=5,proxies=proxy,).text
        x=re.findall('= media_\d;(var .*?media_\d.*?;)',s)
        urls=[]
        for i,j in enumerate(x):
            js='function test(a){ '+j+'return media_'+str(i+1)+';}'
            ss=execjs.compile(js)

            xnul=ss.call('test','1')
            urls.append(xnul)
        nul=urls[-1]
        xx=''
        lex=0
        while xx=='':
            xx=res.get(nul,headers=h,proxies=proxy).json()[lex-1]['videoUrl']
            lex=lex-1
            if lex <-3:
                break


        download(chanels,xx,name+'.mp4')
        time.sleep(2)
    except:
        pass

def chanel(chanes):
    lex=36
    page=1
    while lex==36:
        lex=getchannelslist(chanes,page)
        page+=1

def star(chanes):
    lex = 40
    page = 1
    while lex == 40:
        lex = starlist(chanes, page)
        page += 1

def model(chanes):
    lex = 40
    page = 1
    while lex == 40:
        lex = modellist(chanes, page)
        page += 1

if __name__ == '__main__':
    x=input('地址').split('/')
    if x[3]=='model':
        model(x[4])
    elif x[3]=='pornstar':
        star(x[4])
    elif x[3]=='channels':
        chanel(x[4])
