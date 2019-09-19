import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors



# for i in range(1, 10000):
# 加载数据
data = loaddata(1)
fig = plt.figure()
# 加载图片设置
my_cmap = colormap()

# 第一个子图,按照默认配置
ax = fig.add_subplot(221)
ax.imshow(data)

# 第二个子图,使用api自带的colormap
ax = fig.add_subplot(222)
cmap = mpl.cm.bwr  # 蓝，白，红
ax.imshow(data, cmap=cmap)

# 第三个子图增加一个colorbar
ax = fig.add_subplot(223)
cmap = mpl.cm.winter # 冬季风格
im = ax.imshow(data, cmap=my_cmap)
plt.colorbar(im)  # 增加colorbar

# 第四个子图可以调整colorbar
ax = fig.add_subplot(224)
cmap = mpl.cm.rainbow
# 这里设置colormap的固定值
norm = mpl.colors.Normalize(vmin=-1, vmax=1)
im=ax.imshow(data,cmap=cmap)
plt.colorbar(im,cmap=cmap, norm=norm,ticks=[-1,0,1])


# 显示
plt.show()
