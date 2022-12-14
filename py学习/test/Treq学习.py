# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-09 15:44:14
#FilePath     : /py学习/Treq学习.py
#LastEditTime : 2020-06-09 15:47:09
#Github       : https://github.com/sandorn/home
#==============================================================
使用Python的Treq on Twisted来进行HTTP压力测试_python_脚本之家
https://www.jb51.net/article/64235.htm
'''

from twisted.internet import epollreactor
epollreactor.install()

from twisted.internet import reactor, task
from twisted.web.client import HTTPConnectionPool
import treq
import random
from datetime import datetime

req_generated = 0
req_made = 0
req_done = 0

cooperator = task.Cooperator()

pool = HTTPConnectionPool(reactor)


def counter():
    '''This function gets called once a second and prints the progress at one
    second intervals.
    '''
    print(f"Requests: {req_generated} generated; {req_made} made; {req_done} done")
    # reset the counters and reschedule ourselves
    req_generated = req_made = req_done = 0
    reactor.callLater(1, counter)


def body_received(body):
    global req_done
    req_done += 1


def request_done(response):
    global req_made
    deferred = treq.json_content(response)
    req_made += 1
    deferred.addCallback(body_received)
    deferred.addErrback(lambda x: None)  # ignore errors
    return deferred


def request():
    deferred = treq.post('http://api.host/v2/loadtest/messages',
                         auth=('api', 'api-key'),
                         data={'from': 'Loadtest <test@example.com>',
                               'to': 'to@example.org',
                               'subject': "test"},
                         pool=pool)
    deferred.addCallback(request_done)
    return deferred


def requests_generator():
    global req_generated
    while True:
        deferred = request()
        req_generated += 1
        # do not yield deferred here so cooperator won't pause until
        # response is received
        yield None


if __name__ == '__main__':
    # make cooperator work on spawning requests
    cooperator.cooperate(requests_generator())

    # run the counter that will be reporting sending speed once a second
    reactor.callLater(1, counter)

    # run the reactor
    reactor.run()
