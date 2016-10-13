#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import socket
import threading

ls = os.linesep
screen_lock = threading.Semaphore(value = 1)

class Scanner:
    def __init__(self, host, ports):
        self.host = host
        self.ports = ports

    def conn_scan(self, host, port):
        '''
        tcp full connection scann
        '''

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(3.0)
            s.connect((host, port))
            s.send(b'hello\r\n')
            response = s.recv(100)
            screen_lock.acquire()
            print('  [+] {0}/tcp open'.format(port))
            print('    [+] {0}'.format(str(response)))
        except:
            screen_lock.acquire()
            print('  [-] {0}/tcp close'.format(port))
        finally:
            screen_lock.release()
            s.close()

    def port_scan(self, host, ports):
        try:
            ip = socket.gethostbyname(host)  # hostname -> ip
        except:
            print('[-] Cannot resolve {0}: Unknown host'.format(host))
            return None

        try:
            name = socket.gethostbyaddr(ip)  # ip -> hostname
            print('\n[+] Scan results for: {0}'.format(name[0]))
        except:
            print('\n[+] Scan results for: {0}'.format(ip))

        for port in ports:
            t = threading.Thread(target = self.conn_scan, args = (host, int(port)))
            t.start()

    def run(self):
        self.port_scan(self.host, self.ports)

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
    scanner.run()

if __name__ == '__main__':
    main()