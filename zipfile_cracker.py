#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
zipfile_cracker.py
    Crack password-protected zip file based on dictonary
    If found, return password, otherwise nothing
'''

import sys
import os
import zipfile
from argparse import ArgumentParser
from threading import Thread

ls = os.linesep

class Cracker(object):
    def __init__(self, zipfile, dictonary):
        self.zipfile = zipfile
        self.dictonary = dictonary

    def extract_file(self, zipfile, password):
        try:
            zipfile.extractall(path = 'temp', pwd=bytes(password, 'utf-8'))
            print('[+] Password FOUND: {0}'.format(password))
            os.system('rm -rf temp 2>/dev/null')
        except Exception as e:
            pass

    def try_password(self):
        zfile = zipfile.ZipFile(self.zipfile)
        with open(self.dictonary, 'r') as f:
            for line in f:
                password = line.strip(ls)
                t = Thread(target = self.extract_file, args = (zfile, password))
                t.start()
    
    def run(self):
        self.try_password()

def main():
    parser = ArgumentParser(prog = sys.argv[0], description='password-protected zipfile cracker')
    parser.add_argument('-f', dest = 'zipfile', help = 'specify password-protected zip file')
    parser.add_argument('-d', dest = 'dictonary', help = 'dictonary used to crack zip file')
    args = parser.parse_args()
    if args.zipfile == None or args.dictonary == None:
        parser.print_usage()
        sys.exit(0)
    cracker = Cracker(args.zipfile, args.dictonary)
    cracker.run()

if __name__ == '__main__':
    main()