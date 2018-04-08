#!/usr/bin/python
# -*- coding: UTF-8 -*-
#author: elina.ma@blackboard.com

import os
import sys
import requests
import logging



FILE_PATH = os.path.split(os.path.realpath(__file__))[0]
sys.path.append('../../')


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('one_time_login.log', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger


def send_request(session, url, payload):
	try:
		r = session.get(url, params=payload)
		logger.info('Response status code is %s' % str(r.status_code))
	except Exception as ex:
		logger.error('Call api failed and error message is : %s' % str(ex))
	return r

def one_time_login(hostname, ticket, code):

	session = requests.Session()	
	
	#https://qa-trylearn-std-rc.int.bbpd.io/webapps/login/?action=one_time_login&ticket=6ed6b906-b15b-4bd6-a07c-2ff79e6cbc32
	#send first request for one-time-login page
	login_url = 'https://' + hostname + '/webapps/login/'
	payload = {'action': 'one_time_login', 'ticket': ticket} 
	res = send_request(session, login_url, payload)
	#first_cookies = res.cookies
	#dict_cookie = requests.utils.dict_from_cookiejar(res.cookies)
	#logger.info('dict_cookie type is %s %s' % (type(dict_cookie), dict_cookie))
	
	#send second request for inputting entrycode
	#code = '2f290339-c55a-426d-bc5f-1363d5044ba3'
	login_url = 'https://' + hostname
	payload = {'action': 'one_time_login', 
				'ticket': ticket, 'entryCode': code, 'bottom_Login': 'Login'}
	try:
		res = session.post(login_url, params=payload)
		logger.info('Access url is %s, response is %s' % (login_url, res.content.decode("utf-8")))
	except Exception as ex:
		logger.error('Call api is fail')
	if str(res.status_code) == '200':
		login_status = (res.content.decode('utf-8').find('ultraVersion') > -1 
		or res.content.decode('utf-8').find('Welcome, BBSupport') > -1)
		if not login_status:
			logger.info('Login is failed for %s as content is not expectant' % login_url)
		else:
			logger.info('Login is successful for %s' % login_url)
	else:
		logger.error('Login is failed for %s as code is not 200' %login_url)

	return 1

if __name__ == '__main__':
	logger = setup_custom_logger('one-time-login')

	if len(sys.argv) >= 4:
		hostname = sys.argv[1]
		ticket = sys.argv[2]
		entrycode = sys.argv[3]
	else:
		logger.error('parameters are missing')
		sys.exit()
	one_time_login(hostname, ticket, entrycode)
