#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8:et
"""Date and Time util
"""
__author__ = ["Jianlong Chen <jianlong99@gmail.com>"]
__date__ = "2013-07-17"

 import datetime

def year():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y')

def date_time():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

def date():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

def hour():
    return datetime.datetime.strftime(datetime.datetime.now(), '%H')
