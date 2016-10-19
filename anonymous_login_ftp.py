#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ftptool
import sys
import argparse

class Scanner:
    def __init__(self, host):
        self.host = host

    def login(self):
        try:
            ftp = ftptool.FTPHost.connect(self.host, user = 'anonymous', password = 'me@your.com')
            ftp.quit()
            return True
        except Exception as e:
            return False

def main():
    desc = 'Host scanner on which anonymous user can login'
    parser = argparse.ArgumentParser(prog = sys.argv[0], description = desc)
    parser.add_argument('-H', dest = 'hosts', help = 'specify hosts')
    args = parser.parse_args()
    if args.hosts == None:
        parser.print_usage()
        sys.exit(1)
    for host in args.hosts:
        scanner = Scanner(host)
        if scanner.login():
            print(host, 'FTP Anonymous Login successed.')

if __name__ == '__main__':
    main()