#coding=utf-8
import urllib, urllib2, sys
import ssl
import json
import base64
import requests
import cv2
import os
import numpy as np
# client_id 为官网获取的AK， client_secret 为官网获取的SK
def get_token():
	host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
	AK = "oYYb7zDqH2xoRMbFu85WSIuy"
	CK = "CfuG0wmlvoKoPwQXOU3je2yQ7qbCB36V"
	host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+AK+'&client_secret='+CK
	request = urllib2.Request(host)
	request.add_header('Content-Type', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	content = response.read()
	to_json = json.loads(content)
	token = to_json['access_token']
	return token

token = get_token()
# print token
# 当前路径下的JPG
path = os.getcwd()
pathlist = os.listdir(path)
for p in pathlist:
	if "JPG" in p or "jpg" in p:		
		filename = p
		img = cv2.imread(filename, -1)  
		height, width = img.shape[:2]  
		if height<width:
			img =np.rot90(img,-1)
		cropped = img[512:1560, 512:1560]  # 裁剪坐标为[y0:y1, x0:x1]
		cv2.imwrite("test_out.jpg", cropped)
		with open("test_out.jpg",'rb') as f:
			img = base64.b64encode(f.read())
			host = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
			headers={
			   'Content-Type':'application/x-www-form-urlencoded'
			}
			access_token = token
			host=host+'?access_token='+access_token
			data={}
			data['access_token']=access_token
			data['image'] =img
			res = requests.post(url=host,headers=headers,data=data)
			req=res.json()
			ok = 0
			for mydict in req['words_result']:
				for (k,v) in mydict.items():
					if "CollectSN" in v:
						index = v.find(":")
						index += 2
						ok = 1
						with open("done.txt","a") as fff:
							print >>fff,filename,v[index:]
			if ok ==0 :
				with open("error.log","a") as ff:
					print >>ff,filename
