#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pexpect
import sys

PROMPT = ['# ', '>>> ', '> ', '\$ ']

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)

def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    conn_str = 'ssh ' + user + '@' + host
    #print(conn_str)
    #sys.stdin.read()
    child = pexpect.spawn(conn_str)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print('[-] Error connecting')
        return
    elif ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword'])
    elif ret == 2:
        child.sendline(password)
        child.expect(PROMPT)
        return child
    else:
        print('[-] Error connecting')
        return
    

def main():
    host = '127.0.0.1'
    user = 'sindyoung'
    password = 'shengdexiang2016'
    child = connect(user, host, password)
    send_command(child, 'cat /etc/passwd | grep -i root')

if __name__ == '__main__':
    main()