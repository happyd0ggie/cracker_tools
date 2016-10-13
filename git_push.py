#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pexpect
import os
import sys

def usage():
	'''
	1. export github_password='your_github_password'
	2. ./git_push.py
	'''
	print('''
	Usage:
	  ./git_push.py
	Note:
	  you should set your github password in current shell
	  e.g. export github_password='your_github_password'
	''')

def push():
	password = os.getenv('github_password')
	if password == None:
		print('your github password parameter is not set yet')
		usage()
		sys.exit(1)
	cmd = 'git push'
	git = pexpect.spawn(cmd)
	while True:
		index = git.expect(['Username', pexpect.TIMEOUT])
		if index == 0:
			break
		elif index == 1:
			pass
		else:
			pass
	git.sendline('shengdexiang')
	git.expect('Password.*')
	git.sendline(password)
	git.interact()

def main():
	push()

if __name__ == '__main__':
	main()