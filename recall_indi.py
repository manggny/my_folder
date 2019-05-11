#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import wx,threading,win32api,win32con
import time
import xlrd
import xlwt
from xlutils.copy import copy

class MyApp2(wx.App):

	def OnInit(self):
		frame = MyFrame(parent=None, id=-1, title='ExampleBoxSizer')
		frame.ShowFullScreen(True)
		return True


class MyFrame(wx.Frame):

	def __init__(self, parent, id, title):
		resolx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
		#resoly = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
		self.pos = resolx-50

		wx.Frame.__init__(self, parent, id, title, size=(778, 494),
						  style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)

        # 下面为 基本设置
		self.panel = wx.Panel(self, -1)
		self.panel.SetBackgroundColour((0,0,0))
		font = wx.Font(20, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)

		# 初始画面： 指导语 案件反应
		self.guide1 = wx.StaticText(self.panel,label='接下来请你再次回忆一遍之前学习的词语\n\n你认为你能回忆出多少个词？\n\n（输入个数后按回车键）', style=wx.ALIGN_CENTER)
		self.textCtrl1 = wx.TextCtrl(self.panel, -1, value=' ', style=wx.TE_PROCESS_ENTER)
		self.guide1.SetFont(font)
		self.guide1.SetForegroundColour((255,255,255))
		self.h_sizer1=wx.BoxSizer(wx.HORIZONTAL)

		self.h_sizer1.Add(self.guide1, proportion=1, flag=wx.ALIGN_BOTTOM|wx.ALL, border=20)
		self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
		self.h_sizer2.Add(self.textCtrl1, proportion=1, flag=wx.ALIGN_TOP|wx.ALL, border=20)
		self.V_sizer1 = wx.BoxSizer(wx.VERTICAL)

		self.V_sizer1.Add(self.h_sizer1, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=20)
		self.V_sizer1.Add(self.h_sizer2, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=20)
		#text.SetForegroundColour((255,0,0)) #
		self.panel.SetSizer(self.V_sizer1)

		## binding 시간 순서로 됨!! 근데 정확한 시간은 여기서 안됨..
		self.Bind(wx.EVT_TEXT_ENTER, self.onkeydown,self.textCtrl1)


	def onkeydown(self,event):
		self.conf = self.textCtrl1.GetValue()
		self.panel.DestroyChildren()
		self.guide()

	def guide(self):

		self.panel.DestroyChildren()

		font = wx.Font(30, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
		self.zhushi = wx.StaticText(self.panel, label='指导语,下面进行个人回忆，按空格键开始', style=wx.ALIGN_CENTER)
		self.zhushi.SetFont(font)
		self.zhushi.SetForegroundColour((255, 255, 255))

		h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		h_sizer.Add(self.zhushi, proportion=2, flag=wx.ALIGN_CENTER | wx.ALL, border=30)
		V_sizer = wx.BoxSizer(wx.VERTICAL)
		V_sizer.Add(h_sizer, proportion=2, flag=wx.ALIGN_CENTER | wx.ALL, border=30)
		self.panel.SetSizer(V_sizer)
		self.panel.Layout()
		# text.SetForegroundColour((255,0,0)) #
		#	self.sizer.Add(self.panel, 1, wx.EXPAND)
		self.panel.Bind(wx.EVT_KEY_DOWN, self.keydown2)


	def keydown2(self,event):
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_SPACE:
			self.panel.Hide()
			#wx.FutureCall(4000,self.dest_guide)
			self.panel.DestroyChildren()
		#	self.panel.Unbind(wx.EVT_KEY_DOWN, self.keydown2)
			self.recall_inde()


	def recall_inde(self):
		#self.panel.SetBackgroundColour((128, 128, 128))
		self.ans_txt_list = []
		self.info_list = []
		self.ans_conf_list = []
		for i in range(32):
			self.ans_txt_list.append(wx.TextCtrl(self.panel, -1, value='词语'))
			self.info_list.append(wx.TextCtrl(self.panel, -1, style=wx.TE_READONLY | wx.TE_CENTER|wx.BORDER_NONE,
											  value='完全不确定 1--2--3--4--5--6--7 完全确定'))
			#
			self.info_list[i].SetBackgroundColour((0,0,0))
			self.info_list[i].SetForegroundColour((255,255,255))

			# self.info_list.append(wx.StaticText(self.panel, -1,label='完全不确定 1--2--3--4--5--6--7 完全确定',style=wx.ALIGN_CENTER))
			# self.file_path.write('123123132')
			self.ans_conf_list.append(wx.TextCtrl(self.panel, -1, value='确定度'))

		self.title = wx.StaticText(self.panel, label='Recall Test', style=wx.ALIGN_CENTER)
		self.timer = wx.StaticText(self.panel, label='300', style=wx.ALIGN_CENTER, pos=(self.pos - 10, 10))

		font = wx.Font(20, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
		self.title.SetForegroundColour((255, 255, 255))
		self.title.SetFont(font)
		self.timer.SetForegroundColour((255, 255, 255))
		self.timer.SetFont(font)
		self.bt_confirm = wx.Button(self.panel,label='√')
		self.bt_confirm.Bind(wx.EVT_BUTTON,self.click_bt)

#		self.timer = wx.StaticText(self.panel, label='300', style=wx.ALIGN_CENTER)  # wx.TE_READONLY|wx.TE_CENTER)
#		self.timer.SetFont(font)

		all_hsizer = [wx.BoxSizer(wx.HORIZONTAL)]
		all_hsizer[0].Add(self.title, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

#		all_hsizer[1].Add(self.timer, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

		h_box_sizer = []
		j=0
		for i in range(16):
			# print(i)
			all_hsizer.append(wx.BoxSizer(wx.HORIZONTAL))
			all_hsizer[i + 1].Add(self.ans_txt_list[j], proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
			all_hsizer[i + 1].Add(self.info_list[j], proportion=2, flag=wx.ALL, border=6)
			all_hsizer[i + 1].Add(self.ans_conf_list[j], proportion=0, flag=wx.ALL, border=6)

			all_hsizer[i + 1].Add(self.ans_txt_list[j + 1], proportion=0, flag=wx.EXPAND | wx.ALL, border=6)
			all_hsizer[i + 1].Add(self.info_list[j + 1], proportion=2, flag=wx.ALL, border=6)
			all_hsizer[i + 1].Add(self.ans_conf_list[j + 1], proportion=0, flag=wx.ALL, border=6)

			j += 2

		all_hsizer.append(wx.BoxSizer(wx.HORIZONTAL))
		all_hsizer[17].Add(self.bt_confirm, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

		v_box_sizer = wx.BoxSizer(wx.VERTICAL)
		for i in range(17):
			v_box_sizer.Add(all_hsizer[i], proportion=1, flag=wx.EXPAND)

		v_box_sizer.Add(all_hsizer[17], proportion=1, flag=wx.ALIGN_CENTER)
		self.panel.SetSizer(v_box_sizer)

		self.panel.Layout()
		self.panel.Show()
		start = time.time()
		#t = timer(start)
		#t.run()

		#self.timer.SetLabel(str(t.interval))
		wx.CallLater(100000,self.end)

		self.t = threading.Thread(target=self.worker)
		self.t.daemon = True
		self.start = time.time()
		self.t.start()

	def worker(self):
		self.now = time.time() - self.start
		integ = round(self.now)
		while self.timer != None:
			self.now = time.time() - self.start
			if round(self.now) > integ:
				integ = round(self.now)
				self.timer.SetLabel(str(360 - integ))
			if integ > 8:  # 一定要比end函数出现之前先结束！！
				return

	def click_bt(self,event):
		self.ans_list = []
		self.conf_list = []
		for i in self.ans_txt_list:
			self.ans_list.append(i.GetValue())
		for i in self.ans_conf_list:
			self.conf_list.append(i.GetValue())

	def end(self):


		ExcelFile = xlrd.open_workbook(r'C:/Users/manggny/Desktop/Learning/Learning/memorytask.xlsx')
		format_exl =xlrd.open_workbook(r'format.xls')
		copy_exl = copy(format_exl)
		new_sheet = copy_exl.get_sheet(0)

		sheet1 = ExcelFile.sheet_by_index(0)  # 第一个sheet
		words_list = sheet1.col_values(2)
		cinum_list = sheet1.col_values(1)
		xiao_list = sheet1.col_values(0)
		for i in range(len(words_list)):
			new_sheet.write(i+1,0,xiao_list[i])
			new_sheet.write(i+1,1, cinum_list[i])
			new_sheet.write(i+1,2,words_list[i])
			new_sheet.write(i+1, 4, self.conf_list[i])

		for i in range(len(self.ans_list)):
			new_sheet.write(i + 1, 4,self.conf_list[i])
			new_sheet.write(i + 1, 3, self.ans_list[i])
		new_sheet.write(1, 8, self.conf)

		self.panel.DestroyChildren()

		font = wx.Font(30, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
		self.guide_end = wx.StaticText(self.panel, label='第一轮学习结束了，现在休息一分钟，\n\n休息过程中请尽量放松大脑。\n\n请不要相互交流，也不要看手机！\n\n休息结束后将进行新一轮的学习。', style=wx.ALIGN_CENTER)
		self.guide_end.SetFont(font)
		self.guide_end.SetForegroundColour((255, 255, 255))

		h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		h_sizer.Add(self.guide_end, proportion=2, flag=wx.ALIGN_CENTER | wx.ALL, border=30)
		V_sizer = wx.BoxSizer(wx.VERTICAL)
		V_sizer.Add(h_sizer, proportion=2, flag=wx.ALIGN_CENTER | wx.ALL, border=30)
		self.panel.SetSizer(V_sizer)
		self.panel.Layout()

		# # 对错结果初始化
		# correct = []
		#
		# for i in range(30):
		# 	correct.append(0)
		#
		# # 删除相同答案
		# for i in range(len(ans_list)):
		# 	for j in range(i,len(ans_list)):
		# 		if ans_list[i] == 0:
		# 			break
		# 		elif ans_list[i] == ans_list[j]:
		# 			ans_list[j] = 0
		#
		# #判答案
		# for i in range(len(ans_list)):
		# 	for j in range(len(words_list)):
		# 		if ans_list[i] == 0:
		# 			break
		# 		elif ans_list[i] == words_list[j]:
		# 			correct[j] = 1
		#

		copy_exl.save('inde_recall_result.xls')
		self.panel.Bind(wx.EVT_KEY_DOWN, self.end_all)

	def end_all(self, event):
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_SPACE:
			self.panel.DestroyChildren()
			wx.Exit()





class timer(threading.Thread):  # The timer class is derived from the class threading.Thread
	def __init__(self,start):
		threading.Thread.__init__(self)
		self.time_start = start
		self.interval = 0
		self.thread_stop = False

	def run(self):  # Overwrite run() method, put what you want the thread do here
		while not self.thread_stop:
			self.interval = round(time.time()-self.time_start)
			#print('Thread Object(%d), Time:%s\n' % (self.thread_num, time.ctime()))
			#time.sleep(self.interval)

	def stop(self):
		self.thread_stop = True






def main():
#	start = time.time()
	app = MyApp2()
	app.MainLoop()


if __name__ == '__main__':
	main()