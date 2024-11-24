# pornhub-download

-  使用aria2-rpc下载
-  使用clash代理，代理端口可自定
-  python3
-  需要安装execjs pyaria2

# 用法 
- 1、 去pornhub 抓取自己的cookie，粘贴到cookie.txt
- 2、 找到一个心仪的演员，复制其主页地址
- 3、 终端python3 pornhub.py
- 4、aria2 rpc模式打开，默认端口6800，无密钥，如过有修改，在代码内自行修改
- 5、 将主页地址，粘进去回车开始下载

  - 输入用户页面，既可下载该用户上传的全部免费视频
  - 包括三种：channels、model、star
  - 暂时没注意到其他用户类型，如有可以留言回复


# 2021.10.27更新
适应新的js规则

# 2021.11.1更新
增加延迟，减少被ban几率

# 2022.7.28 更新
- 优化代码，变量名称，增加可读性
- 增加requirements.txt
- 增加uag.txt


# 2022.7.29 更新
- 增加更多user-agent 随机选择
- 增加LOGO

# 2022.8.31 更新
- 用httpx替换requests，从而支持http2

# 2022.11.3 更新
- 使用yaml保存信息
- 增加login.py，通过在cookei.yaml中设置usernam 和password 即可登录
- 登录过程中可能会遇到机器验证，需在p站登录通过验证后即可
- 之后即可利用保存在yaml里的信息，直接使用downloader

# 2022.11.3 更新
- 使用curl_cffi替换httpx
- 更新videourl获取方式