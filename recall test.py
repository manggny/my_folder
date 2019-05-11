import threading
import thread
import time

import wx,sys
import time


class MyApp(wx.App):

	def OnInit(self):
		frame = MyFrame(parent=None, id=-1, title='ExampleBoxSizer')
		frame.ShowFullScreen(True)
		return True


class MyFrame(wx.Frame):

	def __init__(self, parent, id, title):

		wx.Frame.__init__(self, parent, id, title, size=(778, 494),
						  style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)

		# 下面为 基本设置
		self.panel = wx.Panel(self, -1)
		self.panel.SetBackgroundColour((0,0,0))
		font = wx.Font(20, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)

		# 初始画面： 指导语 案件反应
		self.guide1 = wx.StaticText(self.panel,label='接下来请你们回忆刚才学习的词语\n\n你认为你和本回合搭档能回忆出多少个词？\n\n（输入个数后按回车键）', style=wx.ALIGN_CENTER)
		self.textCtrl1 = wx.TextCtrl(self.panel, -1, value='信心', style=wx.TE_PROCESS_ENTER)
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
		t = threading.Thread(target=self.worker)
		self.start = time.time()
		t.start()
		t.

		self.textCtrl1.SetLabel('aaaa')

	def worker(self):
		self.timer = time.time() - self.start
		integ = round(self.timer)
		while True:
			self.timer = time.time()-self.start
			if round(self.timer) > integ:
				integ = round(self.timer)
				self.guide1.SetLabel(str(300-integ))

			if integ>10:

				sys.exit()



		return




def main():
#	start = time.time()
	app = MyApp()
	app.MainLoop()


if __name__ == '__main__':
	main()
