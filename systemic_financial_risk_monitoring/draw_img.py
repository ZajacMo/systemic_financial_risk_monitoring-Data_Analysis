import matplotlib.pyplot as plt
import functools
from nltk.tokenize.texttiling import smooth
from scipy.stats import norm
from pylab import mpl
from numpy import ones_like

def draw(img_category = "svg"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            #设置中文字体
            mpl.rcParams['font.sans-serif'] = ['SimHei']
            mpl.rcParams['axes.unicode_minus'] = False
            # 设置画幅
            plt.figure(figsize=(16,8))
            #设置字体大小
            font_size = 20
            # 调用函数
            func(*args,**kwargs)
            # 设置x轴字体大小
            plt.xticks(fontsize=font_size)
            # 设置y轴字体大小
            plt.yticks(fontsize=font_size)
            # 设置标题
            plt.title(args[0],fontsize=font_size)
            # 获取边框并去掉左右上
            ax = plt.gca()
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            # 设置网格线
            plt.grid(axis='y')
            # 左边距
            plt.subplots_adjust(left=0.1)
            # 保存图片
            plt.savefig("..\\output\\img\\" + args[0] + "."+img_category,  format=img_category, bbox_inches='tight')
            # 显示图片
            # plt.show()
        return wrapper
    return decorator

'''
topic: 图片标题
label: y轴标签
index: 数据索引
data: 切片的数据
'''
@draw(img_category="svg")
def single_line(topic, label, index, data):
    # 绘制压力指数原始图像
    plt.plot(index.values,data,label=label,linewidth=1,alpha=0.5)
    # 绘制压力指数HP滤波后的图像
    plt.plot(index.values,smooth(data,90),label=label+"-HP",linewidth=3)
    # 设置y轴标签
    plt.ylabel("压力指数",fontsize=17,rotation=0,y=1.03,labelpad=-20)
    # 设置图例位置
    plt.legend(loc=1)


@draw(img_category="svg")
def double_line(topic, labels, index, data):
    plt.plot(index, data[labels[0]], label=labels[0] + "概率", linewidth=1, alpha=0.5, color='dodgerblue')
    plt.plot(index, smooth(data[labels[0]], 90), label=labels[0] + "概率" + "-HP", linewidth=3, color='dodgerblue')
    plt.plot(index, data[labels[1]], label=labels[1] + "概率", linewidth=1, alpha=0.5, color='darkorange')
    plt.plot(index, smooth(data[labels[1]], 90), label=labels[1] + "概率" + "-HP", linewidth=3, color='darkorange')
    plt.ylabel("区制概率密度",fontsize=17,rotation=0,y=1.02,labelpad=-20)
    plt.legend(loc=1)


@draw(img_category="svg")
def draw_hist(topic, label, data, params = None):
    print(ones_like(data)/float(len(data)))
    n, bins, patches =plt.hist(data, bins=50, edgecolor='white', density=True, color='skyblue',alpha=0.8)
    # 直方图函数，x为x轴的值，normed=1表示为概率密度，即和为一，绿色方块，色深参数0.5.返回n个概率，直方块左边线的x值，及各个方块对象
    y1 = norm.pdf(bins, params['line1']['mean'], params['line1']['std'])  # 拟合一条最佳正态分布曲线y
    y2 = norm.pdf(bins, params['line2']['mean'], params['line2']['std'])
    plt.plot(bins, y1, 'g--')  # 绘制y的曲线
    plt.plot(bins, y2*.65, 'r--')
    plt.xlabel(label,fontsize=17, x=1.02,labelpad=-20)
    plt.ylabel("概率密度",fontsize=17,rotation=0,y=1.02,labelpad=-20)

