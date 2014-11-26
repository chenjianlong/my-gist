#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8:et
"""Read the subprocess stdout
"""
__author__ = ["Jianlong Chen <jianlong99@gmail.com>"]
__date__ = "2013-07-02"

 import subprocess

def subprocess_stdout(cmd):
    """subprocess stdout generator"""
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in proc.stdout:
        yield line
