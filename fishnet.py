#2022/11/15 by Chun Song      
#-*- coding:utf-8 -*-
#<渔网工具（fishenet）自动化实现>（ArcGIS10.2/Python 2.7.3）
import os
import arcpy
import xlwt
import xlrd
from arcpy import env
files_path="D:\Desktop\fishnet\Fishnet_Python"#files_path为文件夹Fishenet_Python存储路径，修改后即可运行
env.workspace = files_path      #确定工作空间

#确定渔网工具参数，创建渔网工具
input_extent_shapefile = files_path+"/"+"独克宗古城建筑新.shp"	# 需要制作渔网单元格的边界范围矢量文件
output_fishnet_shapefile = files_path+"/"+'Fishnet'	# 渔网单元格输出绝对路径
grid_unit = 10	                                                      # 渔网单元格边长，单位：米
four_point_list=arcpy.Describe(input_extent_shapefile)
arcpy.CreateFishnet_management(output_fishnet_shapefile,
                               str(four_point_list.extent.XMin) +" "+ str(four_point_list.extent.YMin),
                               str(four_point_list.extent.XMin) + " "+ str(four_point_list.extent.YMin+10),
                               str(grid_unit), str(grid_unit),  "0", "0",
                               str(four_point_list.extent.XMax) + " "+ str(four_point_list.extent.YMax),
                               'LABELS', "#", 'POLYGON')#渔网函数
print("Fishnet has been done!!!")

import arcpy
#将生成渔网图层与原图层放入一个新建的gdb文件（fishnet_internect.gdb）中，用于相交函数使用
arcpy.env.overwriteOutput = True
input_data1=files_path+"/"+"Fishnet_label.shp"#创建临时图层
input_data2=files_path+"/"+"Fishnet.shp"
input_data3=files_path+"/"+"独克宗古城建筑新.shp"
arcpy.AddMessage("starting progress")
arcpy.CreateFileGDB_management(files_path, "fishnet_internect1.gdb")#创建gdb函数
arcpy.MakeFeatureLayer_management(input_data1, "input_data1")#临时图层复制函数
arcpy.MakeFeatureLayer_management(input_data2, "input_data2")
arcpy.MakeFeatureLayer_management(input_data3, "input_data3")
arcpy.FeatureClassToGeodatabase_conversion(["input_data1","input_data2","input_data3"],
                                           files_path+"/"+"fishnet_internect1.gdb")#将数据复制到到gdb中
print("GDBfile1 is done!")

#令渔网中心点与建筑图层相交，得到相交后的渔网网格中心点
from arcpy import env
env.workspace = files_path+'/'+'fishnet_internect.gdb'  #环境设置
inFeatures = ['input_data1','input_data3']
fishenet_intersect = files_path+'/'+'fishnet_intersect'
clusterTolerance = 1.5
arcpy.Intersect_analysis(inFeatures, fishenet_intersect, '',
                         clusterTolerance, 'point')#相交函数
print('fishenet_intersect is Done!')

#需要提取fishenet_intersect.shp文件中的点数据()
infc=r'D:\Desktop\渔网（给王祺220722）\Fishnet_Python\fishnet_intersect.shp'
#循环读取每个点的坐标
for row in arcpy.da.SearchCursor(infc, ['SHAPE@XY']):
              X,Y=row[0]
              print('{}.{}'.format(X,Y))

# 新建一个字典
points = {'key': ['value1', 'value2']}
# 往字典中添加数据
infc=r'D:\Desktop\fishnet\Fishnet_Python\fishnet_intersect.shp'
#循环读取每个点的坐标
for row in arcpy.da.SearchCursor(infc, ['OID@', 'SHAPE@X', 'SHAPE@X']):
              ID=row[0]
              X=row[1]
              Y=row[2]
              points[ID] =['{}'.format(X),'{}'.format(Y)]
#print(points)
# 先创建并打开一个文本文件
file = open('points.txt', 'w') 
# 遍历字典的元素，将每项元素的key和value分拆组成字符串，注意添加分隔符和换行符
for k,v in points.items():
	file.write(str(k)+' '+str(v)+'\n')	
# 注意关闭文件
file.close()
print('Done!')
