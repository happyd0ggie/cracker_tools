#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
unix_password_cracker.py
    crack unix password using dictonary
'''

import sys
import os
import crypt

ls = os.linesep

class Cracker(object):
    def __init__(self, password_file, dictonary_file):
        self.password_file = password_file
        self.dictonary_file = dictonary_file
        
    def crack_password(self, hashed_password):
        '''
        for each hashed password in password.txt, trying password in dictonary
        file until nothing found.
        '''

        try:
            salt = hashed_password.split('$')
            insalt = '${0}${1}$'.format(salt[1], salt[2])
            with open(self.dictonary_file, 'r') as f:
                for line in f:
                    password = line.strip(ls)
                    if crypt.crypt(password, insalt) == hashed_password:
                        print(' [+] Password FOUND: {0}'.format(password))
                        return
                print(' [-] Password NOT found.')
        except Exception as e:
            print('ERROR: {0}'.format(e))
            sys.exit(1)
    
    def try_password(self):
        '''
        crack hashed password for each user in password
        '''

        try:
            with open(self.password_file, 'r') as f:
                for line in f:
                    username = line.strip(ls).split(':')[0]
                    hashed_password = line.strip(ls).split(':')[1]
                    if hashed_password != '*' and hashed_password != '!':
                        print('[*] Cracking password for {0}...'.format(username))
                        self.crack_password(hashed_password)
        except Exception as e:
            print('ERROR: {0}.'.format(e))
            sys.exit(1)

    def run(self):
        '''
        start cracking program
        '''

        self.try_password()

def usage():
    print('Usage\n  {0} passwords.txt dictonary.txt'.format(sys.argv[0]))
    sys.exit(1)

def main():
    if len(sys.argv) < 3:
        usage()
    cracker = Cracker(sys.argv[1], sys.argv[2])
    cracker.run()

if __name__ == '__main__':
    main()