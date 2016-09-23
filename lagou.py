# -*- coding: utf-8 -*-
import requests
import sys
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding('utf8')

# 设置mongo数据库连接
client = MongoClient(host='localhost', port=27017)
db = client.mongo

def get_json(url, page, lang_name):
    data = {
    	'first':'True',
    	'pn':page,
    	'kd':lang_name
    	}
    json = requests.post(url, data).json()
    return json

url = 'http://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false'

def job_info(job_title):
    page = 1
    while True:
    	try:
        	json = get_json(url, page, job_title)
        	list_con = json['content']['positionResult']['result']
    	except:
    		continue
        # 如果list_con 为空列表就跳出循环
        if list_con:
            for i in list_con:
                db.test.insert({
                    "companySName": i['companyShortName'],
                    "companyFName": i['companyFullName'],
                    'salary': i['salary'],
                    'city': i['city'],
                    'education': i['education'],
                    'postionName': i['positionName']
                })
                print i['companyShortName'], i['companyFullName'], i['salary'], i['city'], i['education'], i['positionName']
            page += 1
        else:
            break

if __name__ == '__main__':
    url = 'http://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false'
    job_info('运维')