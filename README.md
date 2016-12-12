# Introduction
微信公众号文章爬虫。本项目提供一个利用chrome抓取公众号文章的思路，若部署在你自己的服务器上，不需要输入验证码。
项目业务由flask + Angular实现，http服务使用tornado。
本项目还提供了一种使用场景，使用Chrome插件可以一键转载到UEditor。示例在chrome_extension目录中。

# Demo
http://weixin-article-spider-demo.exyui.com/

# Sources
https://github.com/kiruto/wxbot

https://github.com/Chyroc/WechatSogou

# PhantomJS
http://phantomjs.org/download.html

# ChromeDrive
https://sites.google.com/a/chromium.org/chromedriver/

# npm & node.js
https://nodejs.org/en/download/

# Environment
- OS tested on CentOS7 and OS X
- Python 2.7+
- node.js 6+

# Deploy
1. Make sure python have permission of this path to create files and directories.
2. Create a directory named 'bin/PhantomJS', then download PhantomJS's bin file in it.
3. Create a directory named 'bin/chrome', then download ChromeDrive's bin file in it.
4. Create a directory named 'cache'.
5. Create virtual environment named 'ENV', then activate.
6. Run pip install requirements and npm install dependencies.
7. Run python service.py.

# Licence
```
Weixin-Article-Spider
Copyright (C) 2016  Yuriel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
