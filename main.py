from study import *
from asdasd import MyApp
from math2 import math2
from recall_indi import MyApp2
import xlwt,time

sub=input("subnum?")
team=input("team?")
self_team = input("self_team?")

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('result', cell_overwrite_ok=True)
sheet.write(0, 0, '效价编码')
sheet.write(0, 1, '单词编码')
sheet.write(0, 2, '出现单词')
sheet.write(0, 3, '被试答案')
sheet.write(0, 4, '信度')
sheet.write(0, 5, '双人队')
sheet.write(0, 6, '被试编号')
sheet.write(0, 7, '单人队')


sheet.write(0, 8, '预测回忆个数')

sheet.write(1, 5,team)
sheet.write(1, 6,sub)
sheet.write(1, 7,self_team)

book.save('format.xls')

study()
app = MyApp()
app.MainLoop()
#time.sleep(1000)
math2()
app2 = MyApp2()
app2.MainLoop()




