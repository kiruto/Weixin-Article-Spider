# Source
https://github.com/kiruto/wxbot

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
4. Find the file named 'config.constant.ts', edit the value of 'HOST' to your host.
5. Create virtual environment named 'ENV', then activate.
6. Run pip install requirements and npm install dependencies.
7. Run python service.py.
