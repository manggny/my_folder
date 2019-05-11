import win32api,win32con
import pygame
import time
import random
import xlrd
## read xls


def study():
	ExcelFile=xlrd.open_workbook(r'C:/Users/manggny/Desktop/Learning/Learning/memorytask.xlsx')
	sheet1=ExcelFile.sheet_by_index(0) # 第一个sheet
	words_list = sheet1.col_values(2)

	pygame.init()

	resolx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
	resoly = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
#print(resolx,resoly)
	screen = pygame.display.set_mode((resolx,resoly),pygame.FULLSCREEN)#, flags=pygame.FULLSCREEN, depth=0)
	cur_font = pygame.font.SysFont("SimHei", 40) #宋体的英文名是simsun 我没有。。。
	bg = (0,0,0)
	pygame.mouse.set_visible(0)

	while True:

		screen.fill(bg)
	## 指导语
		text_fmt = cur_font.render(u'指导语，也可以放图片', 1, (255, 255, 255))
		textpos = text_fmt.get_rect()
		textpos.center = (resolx / 2, resoly / 2)
		screen.blit(text_fmt, textpos)
	#	screen.blit(obj)
		pygame.display.flip()
		try:
			while 1:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							raise 1
		except :
			pass
		screen.fill(bg)
		for i in words_list:
			text_fmt = cur_font.render(i, 1, (255,255,255))
			textpos = text_fmt.get_rect()
			textpos.center = (resolx / 2, resoly / 2)
			screen.blit(text_fmt,textpos)
	#	screen.blit(obj)
			pygame.display.flip()
			pygame.time.delay(2000)
			screen.fill(bg)
			text_fmt = cur_font.render(u'+', 1, (255, 255, 255))
			textpos = text_fmt.get_rect()
			textpos.center = (resolx/2, resoly / 2)
			screen.blit(text_fmt, textpos)
		#	screen.blit(obj)
			pygame.display.flip()
			pygame.time.delay(1000)
			screen.fill(bg)


	## 指导语
		text_fmt = cur_font.render(u'结束语', 1, (255, 255, 255))
		textpos = text_fmt.get_rect()
		textpos.center = (resolx / 2, resoly / 2)
		screen.blit(text_fmt, textpos)
	#	screen.blit(obj)
		pygame.display.flip()
		try:
			while 1:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							raise 1
		except :
			pass
		screen.fill(bg)
		ExcelFile2 = xlrd.open_workbook(r'C:/Users/manggny/Desktop/Learning/Learning/math.xlsx')
		math_sheet1 = ExcelFile2.sheet_by_index(0)  # 第一个sheet
		math_list = math_sheet1.col_values(0)
		random.shuffle(math_list)

		for j in math_list:
			text_fmt = cur_font.render(j, 1, (255,255,255))
			textpos = text_fmt.get_rect()
			textpos.center = (resolx / 2, resoly / 2)
			screen.blit(text_fmt,textpos)
	#	screen.blit(obj)
			pygame.display.flip()
			pygame.time.delay(2500)
			screen.fill(bg)
			text_fmt = cur_font.render(u'+', 1, (255, 255, 255))
			textpos = text_fmt.get_rect()
			textpos.center = (resolx/2, resoly / 2)
			screen.blit(text_fmt, textpos)
		#	screen.blit(obj)
			pygame.display.flip()
			pygame.time.delay(1500)
			screen.fill(bg)
		text_fmt = cur_font.render(u'下面要切换屏幕 按任意键继续。。', 1, (255, 255, 255))
		textpos = text_fmt.get_rect()
		textpos.center = (resolx / 2, resoly / 2)
		screen.blit(text_fmt, textpos)
		#	screen.blit(obj)
		pygame.display.flip()
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						pygame.mouse.set_visible(1)
						pygame.quit()
						return


if __name__ == '__main__':
	study()