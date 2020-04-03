#coding=utf-8
#usage: python2
#env:
"""
pip install beautifulsoup4
pip install lxml
"""
import requests
from bs4 import BeautifulSoup  
import sys
import time
num = int(raw_input('How many rows:'))
print 'Your data:'
name = []
for i in range(num):
	name.append(raw_input())
url = 'http://frps.iplant.cn/frps?id={0}'
cnt = 0
for x in name:
	print ('{0}'.format(x)),
	r = requests.get(url.format(x)) 
	content = r.content
	time.sleep(1)
	soup = BeautifulSoup(content, 'lxml')
	aa = soup.find_all('a')
	ans = [x]
	if len(aa)<17:
		print x,',None',',None',',None',',None',',None'
		continue
	ans += aa[15].text.split(' ')
	ans += aa[16].text.split(' ')
	bb = soup.find_all('b')
	div = soup.find_all('div')
	ddd = soup.select('body form div div div div div div')
	for dd in ddd:
		if 'padding-bottom' in str(dd):
			dd = str(dd)
			dd = dd[dd.find('</b>')+4:]
			dd = dd[dd.find('</b>')+4:]
			zhonglatin = bb[1].text+' '+bb[2].text+' '+dd[:dd.find('<span')]
			zhonglatin = zhonglatin.replace('  ',' ')
			zhonglatin = zhonglatin.replace('<b>','')
			zhonglatin = zhonglatin.replace('</b>','')	
			ans.append(zhonglatin)
	if len(ans) == 6:
		print('%s,%s,%s,%s,%s,%s'%(ans[0].decode('utf-8'),ans[1],ans[2],ans[3],ans[4],ans[5]))
	else:
		print x,',None',',None',',None',',None',',None'
