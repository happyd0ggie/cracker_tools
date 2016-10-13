#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import nmap
import socket

ls = os.linesep

class Scanner:
    def __init__(self, host, ports):
        self.host = host
        self.ports = ports

    def scan(self, host, port):
        scanner = nmap.PortScanner()
        try:
            scanner.scan(host, port)
            state = scanner[host]['tcp'][int(port)]['state']
            print('[*] {0} tcp/{1} {2}'.format(host, port, state))
        except Exception as e:
            print('Opps, an error occured: {0}'.format(e))
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(prog = sys.argv[0], description = 'Port scanner')
    parser.add_argument('-H', dest = 'host', help = 'specify target host')
    parser.add_argument('-p', dest = 'ports', help = 'specify target port')
    args = parser.parse_args()

    host = args.host
    ports = str(args.ports).split(',')

    if not host or not ports:
        parser.print_usage()
        sys.exit(1)
    
    scanner = Scanner(host, ports)

    try:
        host = socket.gethostbyname(host)
    except:
        pass

    for port in ports:
        scanner.scan(host, port)

if __name__ == '__main__':
    main()