#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
zipfile_cracker.py
    Crack password-protected zip file based on dictonary
'''

import sys
import os
import zipfile

ls = os.linesep

def usage():
    print('Usage\n  {0} zipfile dictonary'.format(sys.argv[0]))
    sys.exit(1)

class Cracker(object):
    def __init__(self, zipfile, dictonary):
        self.zipfile = zipfile
        self.dictonary = dictonary

    def try_password(self):
        zfile = zipfile.ZipFile(self.zipfile)
        with open(self.dictonary, 'r') as f:
            for line in f:
                password = line.strip(ls)
                try:
                    zfile.extractall(pwd = password)
                    print('[+] Password FOUND: {0}'.format(password))
                    sys.exit(0)
                except Exception as e:
                    pass
            print('[-] Password NOT found.')
    
    def run(self):
        self.try_password()

def main():
    if len(sys.argv) < 3:
        usage()
    cracker = Cracker(sys.argv[1], sys.argv[2])
    cracker.run()

if __name__ == '__main__':
    main()