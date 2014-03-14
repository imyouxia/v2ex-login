#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import urllib
import urllib2
import cookielib
import re
from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

username = '' #用户名
password = '' #密码

#登录地址
url_login = 'http://www.v2ex.com/signin'

#每日登录奖励领取地址
url_get = 'http://www.v2ex.com/mission/daily'

'''
创建的cookie对象必需为全局变量，后面的页面都需要cookie才可以正确获得
因为如果cookie值不为空，将获得新的once值
'''

#获取一个cookie对象
cookie = cookielib.CookieJar()
#构建cookie处理器
cookie_p = urllib2.HTTPCookieProcessor(cookie)
#装载cookie
opener = urllib2.build_opener(cookie_p)

def get_info(url,tag,name):
	'''
	根据对应的属性值获取页面上的值
	'''
	response = opener.open(url)
	content = response.read()
	soup = BeautifulSoup(content)
	value = soup.find(attrs={tag:name})
	return value

def login():
	'''
	once值每次登录都不一样，在页面上可以看到
	也必需有http header
	'''
	req = urllib2.Request(url_login)
	once = get_info(req,'name','once')['value']
	postdata = {
			'u':username,
			'p':password,
			'once':once,	
			#'next':"/"
			}
	
	header = {'Host':'www.v2ex.com','Origin':'http://www.v2ex.com','Referer':'http://www.v2ex.com/signin','User-Agent':"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/32.0.1700.107 Chrome/32.0.1700.107 Safari/537.36"}
	
	data = urllib.urlencode(postdata)
	
	req = urllib2.Request(url_login,data,header)
	response = opener.open(req)

	#print response.getcode()
	#登录成功，会有对应的auth值
	if not 'auth' in [c.name for c in cookie]:
		raise ValueError,"登录失败！"
		
def if_get():
	if_page = urllib2.Request(url_get)
	if_get = opener.open(if_page).read()
	
	if("每日登录奖励已领取" in if_get):
		print "每日登录奖励已领取"
		exit(0)

def daily_mission():
	'''
	获得每日任务的领取地址
	'''
	daily_url = urllib2.Request(url_get)
	data = get_info(daily_url,'class','super normal button')['onclick']
	first_href = data[data.find("'")+1:len(data)-2]
	full_req = urllib2.Request('http://www.v2ex.com' + first_href)
	page = opener.open(full_req).read()	
	
	if("已成功领取每日登录奖励" in page):
		print "已成功领取每日登录奖励"
		exit(0)

if __name__ == '__main__':
	'''
	登录、判断是否已领取、领取
	'''
	login()
	if_get()
	daily_mission()

