#!/usr/bin/env python3

from __future__ import print_function
from multiprocessing.util import LOGGER_NAME
from os import fdopen
import netmiko
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import SSHException
import sys
import time 
import select
import paramiko
import re
import pwinput
import socket
import datetime
import logging

time_now = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
username = input('Username: ')
password = pwinput.pwinput(prompt='Password: ', mask='*')
platform = 'cisco_ios'
ip_host_file = open(r'filename.txt', 'r')
f = open('csv_file.csv', 'w+')
f.write('row1, row2, row3, row4, row5')
f.write('\n')
f.close()

for host in ip_host_file:
	host = host.rstrip()

	fd = open(f'{host}-{time_not}.log', 'w')
	sys.stdout = fd

	try: 

		device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
		output = device.send_command('command')
		fd.close()

	except NetmikoTimeoutAuthentication:
		with open('login_issues.csv', 'a') as f:
			f.write(f'{host},Device Unreachable/SSH not enabled\n')
			sys.stderr.write(f'{host}-Connection Timeout...\n')
		continue
	except NetmikoAuthenticationException:
	    with open('login_issues.csv', 'a') as f:
	    	f.write(f'{host},Device Unreachable/Failure\n')
			sys.stderr.write(f'{host}-Authentication failed, Exiting...\n')
			sys.exit()
	except SSHException:
		with open('login_issue.csv', 'a') as f:
			f.write(f'{host},SSH not enabled\n')
			sys.stderr.write(f'{host}-SSH not enabled...\n')
		continue

		

