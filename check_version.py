#!/usr/bin/python
# -*- coding: UTF-8 -*-
#author:elina.ma@blackboard.com

import sys
import json
import requests


def get_ultra_ui_version(base_url):
	version_url = base_url + '/ultra/api/v1/buildinfo'
	
	try:
		res = requests.get(version_url)
		#print('respons status is %d' % res.status_code)
		ultraVersion = json.loads(res.text)['ultraVersion']
		#print(type(ultraVersion))
	except Exception as ex:
		print('call api is failed and error message is :%s' % str(ex))
	print(ultraVersion)	
	return ultraVersion 

if len(sys.argv) >=2:
	base_url = sys.argv[1]
else:
	print('parameters are missing')
	sys.exit()

get_ultra_ui_version(base_url)

#get_ultra_ui_version('https://qa-ultra-adv-dev-rds-96x.bbpd.io')
