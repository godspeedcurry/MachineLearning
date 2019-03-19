#for python 3
#coding=utf-8
import urllib, sys
import ssl
import json
import base64
import requests
import cv2
import os
import numpy as np
import datetime
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
# client_id 为官网获取的AK， client_secret 为官网获取的SK
def get_token():
	# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
	AK = "oYYb7zDqH2xoRMbFu85WSIuy"
	CK = "CfuG0wmlvoKoPwQXOU3je2yQ7qbCB36V"
	host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+AK+'&client_secret='+CK
	request = urllib.request.Request(host)
	request.add_header('Content-Type', 'application/json; charset=UTF-8')
	response = urllib.request.urlopen(request)
	content = response.read()
	to_json = json.loads(content)
	token = to_json['access_token']
	return token

token = get_token()

# 当前路径下的JPG
path = os.getcwd()
pathlist = os.listdir(path)
try:
	os.system("mkdir out") #创造一个目录
except:
	print ("directory named as \"out\" exists")

for p in pathlist:
	if ("JPG" in p and "test" not in p ) or "jpg" in p:		
		filename = p
		img = cv2.imread(filename, -1)  
		height, width = img.shape[:2]  
		if height<width:
			img =np.rot90(img,-1)
		cropped = img[512:1360, 512:1360]  # 裁剪坐标为[y0:y1, x0:x1]
		newfilename = "test_out"+filename+".jpg" 
		cv2.imwrite(newfilename, cropped)
		with open(newfilename,'rb') as f:
			print("start to detect %s" % filename)
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
			with open("get.txt","a") as gg:
				print (filename,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),file=gg)
			for mydict in req['words_result']:
				for (k,v) in mydict.items():	
					with open("get.txt","a") as gg:
						print (k,v,file=gg)
					# to modify
					v = v.upper()
					if "ZSTU" in v:  #主要改的就是这个
					# if "CollectSN" in v or "CollectS" in v or "Collects" in v:
						index = v.find("ZSTU")
						# index = v.find(":")
						# while v[index].isdigit()==0 and v[index].isalpha()==0: #既不是数字也不是字母
						# 	index += 1
						ok = 1
						with open("done.txt","a") as fff:
							print (filename,v[index:],file=fff)
			if ok ==0 :
				with open("error.log","a") as ff:
					os.system("mv %s out"%filename) #linux		
					print (filename,file=ff)
		# os.system("DEL %s"%newfilename) #windows
		os.system("rm %s"%newfilename) #linux
