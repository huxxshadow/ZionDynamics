import time
time_dict = {}

def timer(func):
    def func_wrapper(*args, **kwargs):
        time_start = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        time_spend = time_end - time_start
        if func.__name__ not in time_dict:
            time_dict[func.__name__] = []
        time_dict[func.__name__].append(time_spend)

        print('%s cost time: %.3f s ********************' % (func.__name__, time_spend))
        return result
    return func_wrapper

# import matplotlib.pyplot as plt
# import numpy as np
# import time
# from math import *
# import seaborn as sns

# sns.set_style('darkgrid')
#
#
# plt.ion() #开启interactive mode 成功的关键函数
# plt.figure(1)
# t = [0]
# t_now = 0
# m = [sin(t_now)]
#
#
#
# for i in range(2000):
#     plt.clf()
#     t_now = i*0.1
#     t.append(t_now)#模拟数据增量流入，保存历史数据
#     m.append(sin(t_now))#模拟数据增量流入，保存历史数据
#     plt.subplot(211)
#     plt.plot(t,m,'-o',color='black')
#     plt.subplot(212)
#     plt.plot(t, m, '-o', color='black')
#     plt.pause(0.01)
#     plt.show()




# @timer
# def test(n):
#     sum = 0
#     for i in range(n + 1):
#         sum += n
#     return sum
