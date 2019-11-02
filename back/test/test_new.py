import sys,os
from sys import path
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
path.append(BASE_DIR)
import numpy as np
import scipy.linalg as la
 
from excel import Excel;
from corrcoef import *;
from plsregress import *;
from optics import *;
from util import *;

# 测试用户侧还是系统侧
# 用户侧
util=Util();
# p=util.IsClinet(0.27897971688429907-0.3439974186200785j,
# 3.3869187269102277+0.48124030963454467j,30);
# # 系统侧
# p=util.IsClinet(0.27897971688429907-0.3439974186200785j,
# 3.3869187269102277+0.48124030963454467j,10);
# print(p)

# 复数的情况 
upcc_path=os.path.join(BASE_DIR,'excel/2-1-2更新UPCC.xls')
ipcc_path=os.path.join(BASE_DIR,'excel/2-1-2更新IPCC.xls');
excel=Excel(ipcc_path,upcc_path).read();
# # 非复数的情况 A
# upcc_path=os.path.join(BASE_DIR,'excel/2-2-2更新UPCC.xls')
# ipcc_path=os.path.join(BASE_DIR,'excel/2-2-2更新IPCC.xls')
# excel=Excel(ipcc_path,upcc_path).read();

# # 偏最小二乘法
ipcc,upcc=excel.get('ipcc'),excel.get('upcc');
pls=Plsregress(ipcc,upcc);
zs=pls.get_plsregress().get('zs');
print(util.get_responsibility_mean(ipcc,upcc,zs))
# print(pls.get_plsregress());
# print(pls.get_c_s_dev_mean());
# # 责任图
# pls.draw_responsibility();
# print(pls.get_responsibility());
# window,step,e 相关系数超e
# corrcoef=Corrcoef(ipcc,upcc);
# p=corrcoef.get_optics_data(is_complex=True);
# print(p)
# # # optics
# ipccn,upccn=p.get('ipccn'),p.get('upccn');
# op=Optics(ipccn,upccn);
# # 有序队列图
# op.draw_ordered_graph();
# # 参数e:聚类图
# op.draw_three_section();
# # 三个部分的zs,us
# print(op.get_three_section_plsregress());
# # 输出用户侧和系统侧发射水平
# print(op.get_three_section_c_s_dev_mean());
# # 三个部分的责任，不需要画图
# print(op.get_three_section_responsibility_mean());
# # p=op.get_three_section();
# # print(p)


# # # print(p.get('ipccn'))

