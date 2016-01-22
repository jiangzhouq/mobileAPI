#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import MySQLdb
import hashlib;
import random
import string
import phpserialize
import time
from DBUtils.PooledDB import PooledDB

POOLIYUN720 = None
POOLMOBILEDB = None
def process(action, uid):
	global POOLIYUN720 
	global POOLMOBILEDB
	if POOLIYUN720 == None :
		POOLIYUN720 = PooledDB(MySQLdb,10,host='localhost',user='root',passwd='Adminiyun720',db='www.iyun720.com',port=3306,charset="utf8") #5为连接池里的最少连接数
	if POOLMOBILEDB == None: 
		POOLMOBILEDB = PooledDB(MySQLdb,10,host='localhost',user='root',passwd='Adminiyun720',db='mobileapi',port=3306,charset="utf8") #5为连接池里的最少连接数

	if int(action) == 5:
		conn = POOLIYUN720.connection()
		cur = conn.cursor()
		n = cur.execute("SELECT uid,username,user_pic,sex,province,city FROM iyun_witkey_space WHERE uid=%d" % uid)
		query_result_user= []
		query_result_user = list(cur.fetchall())
		for i in range(len(query_result_user)):
			query_result_user[i] = list(query_result_user[i])
		for i in range(len(query_result_user)):
			print 'now',i
			n = cur.execute("SELECT shop_slogans FROM iyun_witkey_shop WHERE uid=%d" % (query_result_user[i][0]))
			slogans = cur.fetchone()
			if not slogans == None:
				txt1 = list(slogans)[0]
				if not txt1 == None:
					query_result_user[i].append(txt1.encode("utf-8"))
				else:
					query_result_user[i].append('')
			else:
				query_result_user[i].append('')
			n = cur.execute("SELECT fuid FROM iyun_witkey_free_follow WHERE uid=%d" % (query_result_user[i][0]))
			follow = cur.fetchall()
			print 'follow:',len(follow)
			if len(follow) > 0:
				query_result_user[i].append(len(follow))
			else:
				query_result_user[i].append(0)
			n = cur.execute("SELECT uid FROM iyun_witkey_free_follow WHERE fuid=%d" % (query_result_user[i][0]))
			followed = cur.fetchall()
			if len(followed) > 0:
				query_result_user[i].append(len(followed))
			else:
				query_result_user[i].append(0)
			n = cur.execute("SELECT service_id FROM iyun_witkey_service WHERE uid=%d AND service_status=2" % (query_result_user[i][0]))
			work = cur.fetchall()
			if len(work) > 0:
				query_result_user[i].append(len(work))
			else:
				query_result_user[i].append(0)
		jso = return_users(query_result_user)
		cur.close()
		conn.close()
		return jso
	elif int(action) == 7:
		conn = POOLIYUN720.connection()
		cur = conn.cursor()
		n = cur.execute("SELECT service_id,title,content,leave_num,uid,username,on_time,file_path,province,city,views FROM iyun_witkey_service WHERE service_status=2 AND uid=%d" % uid)
		query_result_service= []
		query_result_service = list(cur.fetchall())
		for i in range(len(query_result_service)):
			query_result_service[i] = list(query_result_service[i])
		for i in range(len(query_result_service)):
			n = cur.execute("SELECT extdata FROM iyun_witkey_custom_fields_ext WHERE objid=%d AND c_id=5" % (query_result_service[i][0]))
			txt1 = list(cur.fetchone())[0]
			query_result_service[i].append(phpserialize.loads(txt1.encode("utf-8")).get("goods_tag","").get("content",""))
			n = cur.execute("SELECT extdata FROM iyun_witkey_custom_fields_ext WHERE objid=%d AND c_id=7" % (query_result_service[i][0]))
			txt1 = list(cur.fetchone())[0]
			query_result_service[i].append(phpserialize.loads(txt1.encode("utf-8")).get("make_device","").get("content",""))
			n = cur.execute("SELECT extdata FROM iyun_witkey_custom_fields_ext WHERE objid=%d AND c_id=8" % (query_result_service[i][0]))
			txt1 = list(cur.fetchone())[0]
			query_result_service[i].append(phpserialize.loads(txt1.encode("utf-8")).get("make_software","").get("content",""))
		jso = return_medias(query_result_service)
		cur.close()
		conn.close()
		return jso
	elif int(action) == 19:
		conn = POOLIYUN720.connection()
		cur = conn.cursor()
		n = cur.execute("SELECT service_id,title,content,leave_num,uid,username,on_time,file_path,province,city,views FROM iyun_witkey_service WHERE service_status=2")
		query_result_service= []
		query_result_service = list(cur.fetchall())
		for i in range(len(query_result_service)):
			query_result_service[i] = list(query_result_service[i])
		for i in range(len(query_result_service)):
			n = cur.execute("SELECT extdata FROM iyun_witkey_custom_fields_ext WHERE objid=%d AND c_id=5" % (query_result_service[i][0]))
			txt1 = list(cur.fetchone())[0]
			query_result_service[i].append(phpserialize.loads(txt1.encode("utf-8")).get("goods_tag","").get("content",""))
			n = cur.execute("SELECT extdata FROM iyun_witkey_custom_fields_ext WHERE objid=%d AND c_id=7" % (query_result_service[i][0]))
			txt1 = list(cur.fetchone())[0]
			query_result_service[i].append(phpserialize.loads(txt1.encode("utf-8")).get("make_device","").get("content",""))
			n = cur.execute("SELECT extdata FROM iyun_witkey_custom_fields_ext WHERE objid=%d AND c_id=8" % (query_result_service[i][0]))
			txt1 = list(cur.fetchone())[0]
			query_result_service[i].append(phpserialize.loads(txt1.encode("utf-8")).get("make_software","").get("content",""))
		jso = return_medias(query_result_service)
		cur.close()
		conn.close()
		return jso
	elif int(action) == 20:
		conn = POOLIYUN720.connection()
		cur = conn.cursor()
		n = cur.execute("SELECT uid,username,user_pic,sex,province,city FROM iyun_witkey_space")
		query_result_user= []
		query_result_user = list(cur.fetchall())
		for i in range(len(query_result_user)):
			query_result_user[i] = list(query_result_user[i])
		for i in range(len(query_result_user)):
			print 'now',i
			n = cur.execute("SELECT shop_slogans FROM iyun_witkey_shop WHERE uid=%d" % (query_result_user[i][0]))
			slogans = cur.fetchone()
			if not slogans == None:
				txt1 = list(slogans)[0]
				if not txt1 == None:
					query_result_user[i].append(txt1.encode("utf-8"))
				else:
					query_result_user[i].append('')
			else:
				query_result_user[i].append('')
			n = cur.execute("SELECT fuid FROM iyun_witkey_free_follow WHERE uid=%d" % (query_result_user[i][0]))
			follow = cur.fetchall()
			print 'follow:',len(follow)
			if len(follow) > 0:
				query_result_user[i].append(len(follow))
			else:
				query_result_user[i].append(0)
			n = cur.execute("SELECT uid FROM iyun_witkey_free_follow WHERE fuid=%d" % (query_result_user[i][0]))
			followed = cur.fetchall()
			if len(followed) > 0:
				query_result_user[i].append(len(followed))
			else:
				query_result_user[i].append(0)
			n = cur.execute("SELECT service_id FROM iyun_witkey_service WHERE uid=%d AND service_status=2" % (query_result_user[i][0]))
			work = cur.fetchall()
			if len(work) > 0:
				query_result_user[i].append(len(work))
			else:
				query_result_user[i].append(0)
		jso = return_users(query_result_user)
		cur.close()
		conn.close()
		return jso
	elif int(action) == 100:
			arr =[]
			n = cur.execute("select service_id from iyun_witkey_service")
			arr = list(cur.fetchall())
			dict1 = {"user":arr}
			return Response(json.dumps(dict1,sort_keys=True))

# uid(int),user_profile(String),user_name(String),sex(String),province(String), city(String), hot(int)
# 
def return_users(strlist):
	userlist = strlist
	for i in range(len(userlist)):
		dict1 = {}
		if userlist[i][0]:
			dict1['uid'] = userlist[i][0]
		if userlist[i][1]:
			dict1['username'] = userlist[i][1]
		if userlist[i][2]:
			dict1['user_profile'] = userlist[i][2]
		if userlist[i][3]:
			dict1['sex'] = userlist[i][3]
		if userlist[i][4]:
			dict1['province'] = userlist[i][4]
		if userlist[i][5]:
			dict1['city'] = userlist[i][5]
		if userlist[i][6]:
			dict1['summary'] = userlist[i][6]
		if userlist[i][7]:
			dict1['follow'] = userlist[i][7]
		if userlist[i][8]:
			dict1['followed'] = userlist[i][8]
		if userlist[i][9]:
			dict1['works'] = userlist[i][9]
		dict1['popular'] = 0
		userlist[i] = dict1
	dict2 = {"data":userlist}
	return json.dumps(dict2,sort_keys=False, indent=4);

def return_medias(strlist):
	medialist = strlist
	for i in range(len(medialist)):
		dict1 = {}
		if medialist[i][0]:
			dict1['mid'] = medialist[i][0]
		if medialist[i][1]:
			dict1['title'] = medialist[i][1].encode("utf-8")
		if medialist[i][2]:
			dict1['summary'] = medialist[i][2].encode("utf-8")
		if medialist[i][3]:
			dict1['comment'] = medialist[i][3]
		dict1['favorite'] = 0
		dict1['is_my_favorite'] = 0
		if medialist[i][4]:
			dict1['uid'] = medialist[i][4]
		if medialist[i][5]:
			dict1['username'] = medialist[i][5].encode("utf-8")
		dict1['user_profile'] = ''
		if medialist[i][6]:
			dict1['create_time'] = medialist[i][6]
		if medialist[i][7]:
			strurl = 'http://view.iyun720.com/pic/'+ str(medialist[i][0]) + '/short_' + medialist[i][7].encode("utf-8").split("/")[-1]
			filename='thumbnail_' + medialist[i][7].encode("utf-8").split("/")[-1].split(".")[0]
			print filename
			extension=medialist[i][7].encode("utf-8").split("/")[-1].split(".")[1]
			if extension == 'mp4':
				extension = 'jpg'
			mm = hashlib.md5()
			mm.update(filename)
			filename=mm.hexdigest()
			dict1['thumbnail'] = 'http://view.iyun720.com/pic/'+ str(medialist[i][0]) + '/' + filename + '.' + extension
			dict1['low_resolution'] = strurl
			dict1['standard_resolution'] = strurl
		dict1['type'] = 1
		if medialist[i][11]:
			dict1['tag'] = medialist[i][11]
		if medialist[i][8]:
			dict1['province'] = medialist[i][8]
		if medialist[i][9]:
			dict1['city'] = medialist[i][9]
		if medialist[i][10]:
			dict1['popular'] = medialist[i][10]
		medialist[i] = dict1
	dict2 = {"data":medialist}
	return json.dumps(dict2,sort_keys=False, indent=4);


def return_comments():
	return 'hello'



