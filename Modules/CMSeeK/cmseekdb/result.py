#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

import cmseekdb.basic as cmseek

def target(target):
    ## initiate the result
    target = target.replace('https://','').replace('http://', '').split('/')
    target = target[0]
    print('[CMSEEK][CMS SCANNER]Target:' + cmseek.bold + cmseek.red + target + cmseek.cln)

def end(requests, time, log_file):
    ## end the result
    print('[CMSEEK][CMS SCANNER]Result: ' + cmseek.bold + cmseek.fgreen + log_file + cmseek.cln)

def cms(cms,version,url):
    ## CMS section
    print('[CMSEEK][CMS SCANNER]CMS: ' + cmseek.bold + cmseek.fgreen + cms + cmseek.cln)
    if version != '0' and version != None:
        print('[CMSEEK][CMS SCANNER]Version: '+ cmseek.bold + cmseek.fgreen + version + cmseek.cln)
    print('[CMSEEK][CMS SCANNER]CMS URL: ' + cmseek.fgreen + url + cmseek.cln)

def menu(content):
    # Use it as a header to start off any new list of item
    print('[CMSEEK][CMS SCANNER]' ,content)

def init_item(content):
    # The first item of the menu
    print('[CMSEEK][CMS SCANNER]' ,content)

def item(content):
    # a normal item just not the first or the last one
    print('[CMSEEK][CMS SCANNER]' ,content)

def empty_item():
    pass

def end_item(content):
    # The ending item
    print('[CMSEEK][CMS SCANNER]' ,content)

def init_sub(content, slave=True):
    # initiating a list of menu under a item
    print('[CMSEEK][CMS SCANNER]' ,content)

def sub_item(content, slave=True):
    # a sub item
    print('[CMSEEK][CMS SCANNER]' ,content)

def end_sub(content, slave=True):
    # ending a sub item
    print('[CMSEEK][CMS SCANNER]' ,ontent)

def empty_sub(slave=True):
	pass


def init_subsub(content, slave2=True, slave1=True):
    # Sub item of a sub item.. this is getting too much at this point
    part1 = ' ┃    │    ' if slave2 else ' ┃         '
    part2 = '│   │' if slave1 else '    │'
    part3 = '\n ┃    │    ' if slave2 else '\n ┃         '
    part4 = '│   ├── ' if slave1 else '    ├── '
    content =  part4 + content
    print('[CMSEEK][CMS SCANNER]' ,content)

def subsub(content, slave2=True, slave1=True):
    part1 = ' ┃    │    ' if slave2 else ' ┃         '
    part2 = '│   ├── ' if slave1 else '    ├── '
    content =  part2 + content
    print('[CMSEEK][CMS SCANNER]' ,content)

def end_subsub(content, slave2=True, slave1=True):
    part1 = ' ┃    │    ' if slave2 else ' ┃         '
    part2 = '│   ╰── ' if slave1 else '    ╰── '
    content = part2 + content
    print('[CMSEEK][CMS SCANNER]' ,content)
