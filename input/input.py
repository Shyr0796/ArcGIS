#-*- coding:utf-8 -*-
#Chun Song
#setup2022/11/13
#实现交互式命令'Input'，增强整个程序的可移植性
import arcpy
from arcpy import env
import xlrd
import os
#CurrentPath='D:/Desktop/input'
#ShpFilePath='D:/Desktop/input/shpfile/group_3.shp'
CurrentPath=input("ShpFilePath like this : 'D:/Desktop/input' : \n")
env.workspace=CurrentPath
ShpFilePath=input("ShpName like this : 'D:/Desktop/input/shpfile/group_3.shp' : \n")

#1
def DeleteFixedColumns():
          drop_field=['InputMark','AreaNum','SurveyMark']
          arcpy.DeleteField_management(ShpFilePath , drop_field)
          print('Dropped Done!')
          
#2
def AddANewColumn(DataName, DataType):
          arcpy.AddField_management(ShpFilePath, DataName, DataType)
          print(DataName+' has been added!')

#3
def AddThreeFixedColumns():
    arcpy.AddField_management(ShpFilePath, 'InputMark', 'SHORT')
    arcpy.AddField_management(ShpFilePath, 'AreaNum', 'SHORT')
    arcpy.AddField_management(ShpFilePath, 'SurveyMark', 'SHORT')
    print(' "InputMark","urveyMark" and "AreaNum" has been added!')

#4
def SurveyMark(OF):
    #实现SurveyMark（要素图斑自动编号，从上到下，从左到右）
    #新建Ymax/Xmin两个字段，分别计算图斑最小外包矩形的左上角Y、X坐标（数学坐标）
    arcpy.AddField_management(OF,"Xmin","DOUBLE")
    arcpy.AddField_management(OF,"Ymax","DOUBLE")
    #字段计算，计算坐标，计算表达式类型为Python_9.3
    arcpy.CalculateField_management(OF,"Xmin","!shape.extent.xmin!","PYTHON_9.3")
    arcpy.CalculateField_management(OF,"Ymax","!shape.extent.ymax!","PYTHON_9.3")
    #迭代更新游标，"Ymax D;Xmin A" 意为Ymax字段将序，Xmin字段升序
    rows1=arcpy.UpdateCursor(OF,"","","","Ymax D;Xmin A")
    i=0
    for row in rows1:
        row.setValue("SurveyMark",i+1) #字段（整型）存放编号，每迭代一次+1
        rows1.updateRow(row)
        i+=1
    del row
    del rows1
    arcpy.DeleteField_management(OF,"Xmin;Ymax")
    print('SurveyMark" has been done!')

#5
def InputMark(OF):
          cursor = arcpy.UpdateCursor(OF)
          listc = range(1,10000)
          j=0
          for row in cursor:
                    value = row.getValue('InputMark')
                    row.setValue('InputMark', listc[j])
                    cursor.updateRow(row)
                    j +=1
          print('InputMark has been done!')

#6
def OutPutAttribute():
          arcpy.env.overwriteOutput = True
          arcpy.TableToExcel_conversion(ShpFilePath, CurrentPath+'/Attribute.xls')
          print('"Attribute.xlsx has been done!!!"')

#7(Fail)
def DataInput(list, type):
          arcpy.env.workspace=arcpy.GetParameterAsText(0)
          excel_path=arcpy.GetParameterAsText(1) # 站点信息表格文件
          data=xlrd.open_workbook(CurrentPath+'/Data.xls')
          sheet_data=data.sheets()[0]
#          list=["Adddata1","Adddata2","Adddata3","Adddata4"]
#          type=["SHORT", "DOUBLE", "DOUBLE", "TEXT"]
          for i in range(0,len(list)):
                    arcpy.AddField_management(ShpFilePath,list[i],type[i])
          with arcpy.da.UpdateCursor(ShpFilePath,list) as cursor:
                    n=1
          for row in cursor:
                    for j in range(0,len(list)):
                              row[j]=sheet_data.row(n)[j].value
                              cursor.updateRow(row)
                    n+=1
          print('Added elements done!!!')

#8
def DeleteFixedColumns(drop_field):
#          drop_field=['InputMark','AreaNum','SurveyMark']
          arcpy.DeleteField_management(ShpFilePath, drop_field)
          print(drop_field+' has been dropped Done!')

#9
#转换地理坐标系，投影坐标系

#10
#手动进行区域划分，并赋值AreaNum（1，2，3，4……）
#选定AreNum的各个区块，分别进行编号，组成SurveyMark
#调查统计阶段，按照不同区块进行，对应信息填入属性表格

print('============COMMAND DICTIONARY============')
print('''1: Add Three Fixed Columns ("InputMark","urveyMark" and "AreaNum")
2: Add a New custom column ()
3: DeleteThreeFixedColumns ("InputMark","urveyMark" and "AreaNum")
4: Number the SurveyMark (DataName:'A', DataType: 'SHORT')
5: Filling data sequential memory sequence 'InputMark'
6: Output shpfile attribute table
7: Input column from EXCEL
8: Delete custom column
9: Coordinate system transformation()
10: Districts are divided and numbered separately.
11: Need to be decided or settled()
12: End Command !!! ''')
print('=====================DICTIONARY END====================')
order=input('Give a order:')
while order:
          
          if order==1:
                    AddThreeFixedColumns()
                    print('=====================ORDER_1 END====================')
                    order=input('Give a order:')

          elif order == 2:
                    AddANewColumn(input('DataName : \n'),input('DataType : \n'))
                    print('=====================ORDER_2 END====================')
                    order=input('Give a order:')

          elif order == 3:
                    AddThreeFixedColumns()
                    print('=====================ORDER_3 END====================')
                    order=input('Give a order:')

          elif order == 4:
                    SurveyMark(ShpFilePath)
                    print('=====================ORDER_4 END====================')
                    order=input('Give a order:')

          elif order == 5:
                    InputMark(ShpFilePath)
                    print('=====================ORDER_5 END====================')
                    order=input('Give a order:')

          elif order == 6:
                    OutPutAttribute()
                    print('=====================ORDER_6 END====================')
                    order=input('Give a order:')

          elif order == 7:
                    list=input("Enter data names in Excel like this: ['Adddata1','Adddata2','Adddata3','Adddata4']: \n")
                    type=input("Enter datatypes in order in Excel like this: ['SHORT','DOUBLE','DOUBLE','TEXT']: \n")
                    # ['SHORT','DOUBLE','DOUBLE','TEXT']
                    DataInput(list, type)
                    print('=====================ORDER_7 END====================')
                    order=input('Give a order:')

          elif order == 8:
                    drop_field=input("Input the dropped columns like this 'A' or ['A','B',...]: \n")
                    DeleteFixedColumns(drop_field)
                    print('=====================ORDER_8 END====================')
                    order=input('Give a order:')

          elif order == 9:
                    print('order 9')
                    print('=====================ORDER_9 END====================')
                    order=input('Give a order:')

          elif order == 10:
                    print('order 10')
                    print('=====================ORDER_10 END====================')

          elif order == 11:
                    print('order 11')
                    print('=====================ORDER_11 END====================')
                    order=input('Give a order:')

          elif order == 12:
                    print('=====================ORDER_12 END====================')
                    break

