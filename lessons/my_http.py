#!/usr/bin/python
# -*- coding: UTF-8 -*-

from httplib import HTTPConnection
import urllib


def status_200(resp):
    var = resp.read()
    print(var)
    return


def status_default(resp):
    print('[WARN] Status:', resp.status, ', Reason:', resp.reason)
    return


def request(host, port, url='', switch=None, params={}, method='GET', body=None, headers={}):
    if switch is None:
        switch = {200: status_200, }
    try:
        url += urllib.urlencode(params)
        http_client = HTTPConnection(host, port)
        http_client.request(method, url, body, headers)
        response = http_client.getresponse()
        switch.get(response.status, status_default)(response)

        # if response.status == 200:
        #     data = response.read()
        #     print (data)
        # else:
        #     print ("[WARN] Status:", response.status, ", Reason:", response.reason)
    except Exception, e:
        print e


def get(host, port, url='', params={}, switch=None):
    request(host, port, url, switch, params, 'GET')


def post(host, port, url='', params={}, switch=None):
    request(host, port, url, switch, params, 'POST')


if __name__ == '__main__':
    params = urllib.urlencode({'number': 12524, 'type': 'issue', 'action': 'show'})
    print params

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    request('tinyzzh.github.io', 80, '/xx.php?', {}, {'name': 'lucy'})
