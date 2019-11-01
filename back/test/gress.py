#coding=utf-8

import sys,os
from sys import path
import numpy as np
import scipy.linalg as la
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path.append(BASE_DIR) #这里preprocess是split_by_date.py所在文件夹
from Plsregress import plsregress
from ReadExcel import excel2m
from mean import mean
from responsibility import get_responsibility,draw;
from corrcoef import get_over_corrcoef

if __name__=="__main__":
    # upcc_path=os.path.join(BASE_DIR,'excel/2-2-1更新UPCC.xls')
    # ipcc_path=os.path.join(BASE_DIR,'excel/2-2-1更新IPCC.xls')
    # upcc,ipcc=excel2m(upcc_path),excel2m(ipcc_path)
    upcc_path=os.path.join(BASE_DIR,'excel/2-1-1更新UPCC.xls')
    ipcc_path=os.path.join(BASE_DIR,'excel/2-1-1更新IPCC.xls')
    upcc,ipcc=excel2m(upcc_path,True),excel2m(ipcc_path,True);
    # p=get_over_corrcoef(ipcc,upcc);
    # print(p)
    # print(type(ipcc))
    p=plsregress(ipcc,upcc)
    # print(p)
    zs=p.get('zs');
    print(zs)
    # res=get_responsibility(ipcc,upcc,zs);
    # dc=res.get('dc');
    # ds=res.get('ds');
    # # print(dc)
    # draw(list(range(len(dc))),dc,list(range(len(ds))),ds)





