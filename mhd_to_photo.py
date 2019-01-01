#coding=utf-8
import cv2
import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
DEBUG_MODE = 1

filename = 'annotations.csv'
annotations_list = []
with open(filename) as f:
	reader = csv.reader(f)
	annotations_list = list(reader)

path = os.getcwd()
pathlist = os.listdir(path)
cnt = 201900000
def draw(data,x,y,radius,pad):
	data[max(0, y - radius):min(data.shape[0], y + radius),max(0, x - radius - pad):max(0, x - radius)] = 3000  # 竖线
	data[max(0, y - radius):min(data.shape[0], y + radius),min(data.shape[1], x + radius):min(data.shape[1], x + radius + pad)] = 3000  # 竖线
	data[max(0, y - radius - pad):max(0, y - radius),max(0, x - radius):min(data.shape[1], x + radius)] = 3000  # 横线
	data[min(data.shape[0], y + radius):min(data.shape[0], y + radius + pad),max(0, x - radius):min(data.shape[1], x + radius)] = 3000  # 横线
	return data


def show_nodules(ct_scan, nodules,Origin,Spacing,p,radius=20, pad=2, max_show_num=4):  # radius是正方形边长一半，pad是边的宽度,max_show_num最大展示数
    show_index = []
    global cnt
    # print nodules.shape[0]
    for idx in range(nodules.shape[0]):  # lable是一个nx4维的数组，n是肺结节数目，4代表x,y,z,以及直径
        if idx < max_show_num:
            if abs(nodules[idx, 0]) + abs(nodules[idx, 1]) + abs(nodules[idx, 2]) + abs(nodules[idx, 3]) == 0: continue
            x, y, z = int((nodules[idx, 0]-Origin[0])/SP[0]), int((nodules[idx, 1]-Origin[1])/SP[1]), int((nodules[idx, 2]-Origin[2])/SP[2])
            # print(x, y, z)
            data = ct_scan[z]
            radius=int(nodules[idx, 3]/SP[0]/2)
            maxx = 0
            maxy = 0
            minx = 10000
            miny = 10000
            x_list = []
            y_list = []
            #pad = 2*radius
            # 注意 y代表纵轴，x代表横轴
            if DEBUG_MODE == 1:
            	data = draw(data,x,y,radius,pad)
            # data[max(0, y - radius):min(data.shape[0], y + radius),
            # max(0, x - radius - pad):max(0, x - radius)] = 3000  # 竖线
            x_list.append(max(0, x - radius - pad))
            x_list.append(max(0, x - radius))
            y_list.append(max(0, y - radius))
            y_list.append(min(data.shape[0], y + radius))
            # data[max(0, y - radius):min(data.shape[0], y + radius),
            # min(data.shape[1], x + radius):min(data.shape[1], x + radius + pad)] = 3000  # 竖线
            x_list.append(min(data.shape[1], x + radius))
            x_list.append(min(data.shape[1], x + radius + pad))
            y_list.append(min(data.shape[0], y + radius))
            y_list.append(max(0, y - radius))
            # print "line2",max(0, y - radius),min(data.shape[0], y + radius),min(data.shape[1], x + radius),min(data.shape[1], x + radius + pad)
            # data[max(0, y - radius - pad):max(0, y - radius),
            # max(0, x - radius):min(data.shape[1], x + radius)] = 3000  # 横线
            x_list.append(max(0, x - radius))
            x_list.append(min(data.shape[1], x + radius))
            y_list.append(max(0, y - radius - pad))
            y_list.append(max(0, y - radius))            
            # print "line3",max(0, y - radius - pad),max(0, y - radius),max(0, x - radius),min(data.shape[1], x + radius)
            # data[min(data.shape[0], y + radius):min(data.shape[0], y + radius + pad),
            # max(0, x - radius):min(data.shape[1], x + radius)] = 3000  # 横线
            x_list.append(max(0, x - radius))
            x_list.append(min(data.shape[1], x + radius))
            y_list.append(min(data.shape[0], y + radius))
            y_list.append(min(data.shape[0], y + radius + pad))
            # print "line4",min(data.shape[0], y + radius),min(data.shape[0], y + radius + pad),max(0, x - radius),min(data.shape[1], x + radius)
            if z in show_index:  # 检查是否有结节在同一张切片，如果有，只显示一张
            	continue
            x_list.sort()
            y_list.sort()
            maxx = x_list[len(x_list)-1]
            minx = x_list[0]
            maxy = y_list[len(y_list)-1]
            miny = y_list[0]
            
            show_index.append(z) 
            cnt += 1
            file = p+"_"+str(cnt)+".jpg"
            with open("all.txt","a") as f:
            	print >> f,file,"nodules",minx,miny,maxx,maxy 
            plt.figure(idx)
            directory = p+"_out" 
            if os.path.exists(directory) == 0:
            	os.mkdir(directory)
            plt.imsave(directory+"\\"+file,data,cmap='gray')
            # plt.imshow(data, cmap='gray')
    # plt.show()
path = os.getcwd()
pathlist = os.listdir(path)
for p in pathlist:
	if "." not in p:
		sublist = os.listdir(path+"\\"+p)
		for sub in sublist:
			if ".mhd" in sub:
				filename = path + "\\" + p + "\\" + sub
				itkimage = sitk.ReadImage(filename)#读取.mhd文件
				OR=itkimage.GetOrigin()
				print(OR)
				SP=itkimage.GetSpacing()
				print(SP)
				numpyImage = sitk.GetArrayFromImage(itkimage)#获取数据，自动从同名的.raw文件读取
				mylist = []
				count = 0
				for eachline in annotations_list:
					if eachline[0] in sub:
						neweachline = eachline[1:]
						get_float = [float(f) for f in neweachline]
						mylist.append(get_float)
				b = np.array(mylist)
				show_nodules(numpyImage,b,OR,SP,p)
