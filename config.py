# -*- coding: utf-8 -*-
import os

import constants

debug = False

# flask http端口
http_port = 6303

# 取得页面信息的方法
engine = constants.browser

# 缓存配置
cache_dir = 'cache'
cache_session_name = 'requests_wechatsogou_session'

# mysql数据库配置
host = 'localhost'
user = 'root'
passwd = ''
db = 'wechatmp'  # 默认数据库
charset = 'utf8'
prefix = 'sogou'  # 默认数据表前缀

# 打码平台配置ruokuai
dama_type = ''
dama_name = ''
dama_pswd = ''
dama_soft_id = ''
dama_soft_key = ''

agent = (
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
)

# 当前目录
current_path = os.path.dirname(__file__) + os.sep

# 数据保存目录
local_storage_path = os.path.join(current_path, "data", "html") + os.sep

# 数据库目录
db_path = os.path.join(current_path, "data") + os.sep
db_file = 'meta.db'

# web资源目录
web_source_path = os.path.join(current_path, "webapp") + os.sep

# web部署目录
web_path = os.path.join(current_path, "static", "dist") + os.sep

# node modules
node_modules_path = os.path.join(current_path, "node_modules") + os.sep

# 日志根目录
log_path = os.path.join(current_path, "data", "log") + os.sep

# 0755 permission needed
phantomjs_path = os.path.join(current_path, "bin", "PhantomJS") + os.sep + "phantomjs"
chrome_path = os.path.join(current_path, "bin", "chrome") + os.sep + "chromedriver"

browser_platform = constants.chrome if debug else constants.phantomjs
