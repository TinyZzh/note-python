#!/usr/bin/python
# -*- coding: UTF-8 -*-

import httplib
import urllib

params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})

print params

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
try:
    httpClient = httplib.HTTPConnection('www.baidu.com', 80)

    httpClient.request('GET', '')
    response = httpClient.getresponse()
    if response.status == 200:
        data = response.read()
        print data
    else:
        print response.reason
except Exception, e:
    print e
