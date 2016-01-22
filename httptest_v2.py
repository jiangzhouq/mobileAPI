#!/usr/bin/python
# -*- coding: utf-8 -*-
# Description: 多线程有用方法模块
# Create: 2008-8-30
# Author: MK2[fengmk2@gmail.com]

import httplib  
import time
import os

while 1:
	try:
		conn = httplib.HTTPConnection("127.0.0.1:12342")  
		conn.request("GET", "")  
		r1 = conn.getresponse()  
		print r1.status, r1.reason  
		if r1.status == 200:
			print 'ok'
		else:
			print 'not ok'
			os.system("kill $(ps aux | grep '[t]hreadutil.py' | awk '{print $2}')")
			time.sleep(5)
			os.system('nohup python threadutil.py &')
                	time.sleep(5)
		time.sleep(60)
	except:
		os.system("kill $(ps aux | grep '[t]hreadutil.py' | awk '{print $2}')")
                time.sleep(5)
                os.system('nohup python threadutil.py &')
                time.sleep(5)
		print 'not ok'
