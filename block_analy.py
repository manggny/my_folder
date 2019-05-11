import sys, numpy

sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
import matplotlib.pyplot as plt
from go.funcs import make_list
from go.funcs import make_gonogolick,raster

path = "C:/Users/manggny/Desktop/expdata/block"
file1 = "#3_gonogonolaser_d5_odor2_1.lvm"
nolaser_file = path + '/' + file1
file2 ="#3_gonogolaser_d5_odor2_1.lvm"
laser_file=path + '/' + file2	 

number, jieduan, day, godor, Hz, *_ = file1.split("_")
odor1, odor2, lick, pump, action, airpuff, laser = make_list(nolaser_file)
lodor1, lodor2, llick, lpump, laction, lairpuff, llaser = make_list(laser_file)
print(file1+" and "+file2)
laser_odor1_lick,laser_odor2_lick = make_gonogolick(lodor1,lodor2,llick)
nolaser_odor1_lick,nolaser_odor2_lick = make_gonogolick(odor1,odor2,lick)
tr1,ti1 = numpy.shape(laser_odor1_lick)
tr2,ti2 = numpy.shape(laser_odor2_lick)
ntr1,nti1 = numpy.shape(nolaser_odor1_lick)
ntr2,nti2 = numpy.shape(nolaser_odor2_lick)
print(sum(llaser))
print("laser licks:")
print("odor1: %f\nodor2: %f"%(numpy.sum(laser_odor1_lick[0:int(tr1/2),:]),numpy.sum(laser_odor2_lick[0:int(tr2/2),:])))
print("no-laser licks:")
print("odor1: %f\nodor2: %f"%(numpy.sum(nolaser_odor1_lick[int(ntr1/2):int(ntr1),:]),numpy.sum(nolaser_odor2_lick[int(ntr2/2):int(ntr2),:])))


laser_odor1_die = numpy.zeros(19)
laser_odor2_die = numpy.zeros(19)
nolaser_odor1_die = numpy.zeros(19)
nolaser_odor2_die = numpy.zeros(19)
laser_odor1_first = numpy.zeros(19)
laser_odor2_first = numpy.zeros(19)
nolaser_odor1_first = numpy.zeros(19)
nolaser_odor2_first = numpy.zeros(19)
laser_odor1_first_aver = 0
laser_odor2_first_aver = 0
nolaser_odor1_first_aver = 0
nolaser_odor2_first_aver = 0
for i in range(int(len(laser_odor1_lick[:,1])/2)):
	for j in range(len(laser_odor1_lick[1,:])):
		if laser_odor1_lick[i,j] == 1:
			laser_odor1_first[int(numpy.floor(j/100))] += laser_odor1_lick[i,j]
			laser_odor1_first_aver += j
			break
laser_odor1_first_aver = laser_odor1_first_aver/(len(laser_odor1_lick[:,1])/2)

for i in range(int(len(laser_odor2_lick[:,1])/2)):
	for j in range(len(laser_odor2_lick[1,:])):
		if laser_odor2_lick[i,j] == 1:
			laser_odor2_first[int(numpy.floor(j/100))] += laser_odor2_lick[i,j]
			laser_odor2_first_aver += j
			break
laser_odor2_first_aver = laser_odor2_first_aver/(len(laser_odor2_lick[:,1])/2)
for i in range(int(len(nolaser_odor1_lick[:,1])/2),len(nolaser_odor1_lick[:,1])):
	for j in range(len(nolaser_odor1_lick[1,:])):
		if nolaser_odor1_lick[i,j] == 1:
			nolaser_odor1_first[int(numpy.floor(j/100))] += nolaser_odor1_lick[i,j]
			nolaser_odor1_first_aver += j
			break
nolaser_odor1_first_aver = nolaser_odor1_first_aver/(len(nolaser_odor1_lick[:,1])/2)
for i in range(int(len(nolaser_odor2_lick[:,1])/2),len(nolaser_odor2_lick[:,1])):
	for j in range(len(nolaser_odor2_lick[1,:])):
		if nolaser_odor2_lick[i,j] == 1:
			nolaser_odor2_first[int(numpy.floor(j/100))] += nolaser_odor2_lick[i,j]
			nolaser_odor2_first_aver += j
			break
nolaser_odor2_first_aver = nolaser_odor2_first_aver/(len(nolaser_odor2_lick[:,1])/2)
print("first licks: \nlaser_odor1 : %f\nlaser_odor2 : %f\nno-laser_odor1 : %f\nno-laser_odor2 : %f"%(laser_odor1_first_aver,laser_odor2_first_aver,nolaser_odor1_first_aver,nolaser_odor2_first_aver))
xx = numpy.linspace(0,19,19)
plt.plot(xx,laser_odor1_first,'r',label='laser_odor1')
plt.plot(xx,nolaser_odor1_first,'b',label='nolaser_Odor1')
plt.title("block analysis of " +number+ "_fisrtlick_odor1")
plt.xlabel("Time(s)")
plt.ylabel("licknum(/s)")
plt.legend(loc='upper left')
plt.savefig("block_analy_of_"+number+"_fistlick_odor1.png")
plt.close()
plt.plot(xx,laser_odor2_first,'r',label='laser_odor2')
plt.plot(xx,nolaser_odor2_first,'b',label='nolaser_Odor2')
plt.title("block analysis of " +number+ "_firstlick_odor2")
plt.xlabel("Time(s)")
plt.ylabel("licknum(/s)")
plt.legend(loc='upper left')
plt.savefig("block_analy_of_"+number+"_firstlick_odor2.png")
plt.close()

xx = numpy.linspace(0,19,19)

for i in range(int(len(laser_odor1_lick[:,1])/2)):
	for j in range(len(laser_odor1_lick[1,:])):
		laser_odor1_die[int(numpy.floor(j/100))] += laser_odor1_lick[i,j]

for i in range(int(len(laser_odor2_lick[:,1])/2)):
	for j in range(len(laser_odor2_lick[1,:])):
		laser_odor2_die[int(numpy.floor(j/100))] += laser_odor2_lick[i,j]

for i in range(int(len(nolaser_odor1_lick[:,1])/2),len(nolaser_odor1_lick[:,1])):
	for j in range(len(nolaser_odor1_lick[1,:])):
		nolaser_odor1_die[int(numpy.floor(j/100))] += nolaser_odor1_lick[i,j]

for i in range(int(len(nolaser_odor2_lick[:,1])/2),len(nolaser_odor2_lick[:,1])):
	for j in range(len(nolaser_odor2_lick[1,:])):
		nolaser_odor2_die[int(numpy.floor(j/100))] += nolaser_odor2_lick[i,j]

plt.plot(xx,laser_odor1_die,'r',label='laser_odor1')
plt.plot(xx,nolaser_odor1_die,'b',label='nolaser_Odor1')
plt.title("block analysis of " +number+ " odor1")
plt.xlabel("Time(s)")
plt.ylabel("licknum(/s)")
plt.legend(loc='upper left')
plt.savefig("block_analy_of_"+number+"odor1.png")
plt.close()
plt.plot(xx,laser_odor2_die,'r',label='laser_odor2')
plt.plot(xx,nolaser_odor2_die,'b',label='nolaser_Odor2')
plt.title("block analysis of " +number+ " odor2")
plt.xlabel("Time(s)")
plt.ylabel("licknum(/s)")
plt.legend(loc='upper left')
plt.savefig("block_analy_of_"+number+"odor2.png")
plt.close()
i=0
laser_odor1_lick,laser_odor2_lick
for j in range(tr1):
	while i < ti1:
		try:
			if laser_odor1_lick[j,i] == 1:
				laser_odor1_lick[j,i + 1] = 1
				laser_odor1_lick[j, i + 2] = 1
				laser_odor1_lick[j, i + 3] = 1
				laser_odor1_lick[j, i + 4] = 1
				laser_odor1_lick[j, i + 5] = 1
				laser_odor1_lick[j, i + 6] = 1
				laser_odor1_lick[j, i + 7] = 1
				i += 8
			# print(go_lick[j][i + 7])
			else:
				i += 1
		except:
			i += 1
	# print(go_lick[j][i + 7])
	i = 0
i = 0
for j in range(ntr1):
	while i < nti1:
		try:
			if nolaser_odor1_lick[j,i] == 1:
				nolaser_odor1_lick[j,i + 1] = 1
				nolaser_odor1_lick[j, i + 2] = 1
				nolaser_odor1_lick[j, i + 3] = 1
				nolaser_odor1_lick[j, i + 4] = 1
				nolaser_odor1_lick[j, i + 5] = 1
				nolaser_odor1_lick[j, i + 6] = 1
				nolaser_odor1_lick[j, i + 7] = 1
				i += 8
			else:
				i += 1
		except:
			i += 1
	i = 0
i=0
for j in range(tr2):
	while i < ti2:
		try:
			if laser_odor2_lick[j,i + 1]== 1:
				laser_odor2_lick[j,i + 2] = 1
				laser_odor2_lick[j, i + 3] = 1
				laser_odor2_lick[j, i + 4] = 1
				laser_odor2_lick[j, i + 5] = 1
				laser_odor2_lick[j, i + 6] = 1
				laser_odor2_lick[j, i + 7] = 1
				laser_odor2_lick[j, i + 8] = 1
				i += 8
			# print(go_lick[j][i + 7])
			else:
				i += 1
		except:
			i += 1
	# print(go_lick[j][i + 7])
	i = 0
i = 0
i = 0
for j in range(ntr2):
	while i < nti2:
		try:
			if nolaser_odor2_lick[j,i] == 1:
				nolaser_odor2_lick[j,i + 1] = 1
				nolaser_odor2_lick[j, i + 2] = 1
				nolaser_odor2_lick[j, i + 3] = 1
				nolaser_odor2_lick[j, i + 4] = 1
				nolaser_odor2_lick[j, i + 5] = 1
				nolaser_odor2_lick[j, i + 6] = 1
				nolaser_odor2_lick[j, i + 7] = 1
				i += 8
			else:
				i += 1
		except:
			i += 1
	i = 0



if tr1>tr2:
	raster(laser_odor1_lick[0:int(tr1/2),:],nolaser_odor1_lick[int(ntr1/2):int(ntr1),:],number+'_block_laser')
	print()
else:
	raster(laser_odor2_lick[0:int(tr2/2),:],nolaser_odor2_lick[int(ntr2/2):int(ntr2),:],number+'_block_laser')
