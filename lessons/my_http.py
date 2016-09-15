#!/usr/bin/python
# -*- coding: UTF-8 -*-

import httplib
import urllib

params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})

print params

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}


def status_200(resp):
    var = resp.read()
    print(var)
    return


def status_default(resp):
    print('[WARN] Status:', resp.status, ', Reason:', resp.reason)
    return

try:
    httpClient = httplib.HTTPConnection('tinyzzh.github.io', 80)

    httpClient.request('GET', '/xxx/11')
    response = httpClient.getresponse()

    switch = {
        200: status_200,
    }
    switch.get(response.status, status_default)(response)

    # if response.status == 200:
    #     data = response.read()
    #     print (data)
    # else:
    #     print ("[WARN] Status:", response.status, ", Reason:", response.reason)
except Exception, e:
    print e

