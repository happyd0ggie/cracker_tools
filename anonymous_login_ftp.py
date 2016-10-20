#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ftptool
import sys
import os
import argparse

ls = os.linesep

class Scanner:
    def __init__(self, host):
        self.host = host

    def login(self):
        try:
            print('Testing {0}...'.format(self.host), end = ' ')
            ftp = ftptool.FTPHost.connect(self.host, user = 'anonymous', password = 'me@your.com')
            ftp.quit()
            return True
        except Exception as e:
            return False

def main():
    desc = 'Host scanner on which anonymous user can login'
    parser = argparse.ArgumentParser(prog = sys.argv[0], description = desc)
    parser.add_argument('-H', dest = 'hosts', help = 'specify hosts')
    parser.add_argument('-f', dest = 'filename', help = 'specify hosts file')
    args = parser.parse_args()
    if args.hosts == None and args.filename == None:
        parser.print_usage()
        sys.exit(1)
    if args.hosts:
        for host in args.hosts.split(','):
            scanner = Scanner(host)
            if scanner.login():
                print(host, 'FTP Anonymous Login successed.')
            else:
                print('\n')
    elif args.filename:
        with open(args.filename, 'r') as f:
            for host in f:
                host = host.strip(ls)
                scanner = Scanner(host)
                if scanner.login():
                    print(host, 'FTP Anonymous Login successed.')
                else:
                    print('\n')
    else:
        parser.print_usage()
        sys.exit(1)

if __name__ == '__main__':
    main()