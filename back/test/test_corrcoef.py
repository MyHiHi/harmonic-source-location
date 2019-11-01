#coding=utf-8

import sys,os
from sys import path
import numpy as np
import scipy.linalg as la
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path.append(BASE_DIR) 
from Plsregress import plsregress
from ReadExcel import excel2m
from mean import mean
from responsibility import get_responsibility,draw,draw_scatter
from corrcoef import get_over_corrcoef,get_optics_data
from optics import *
from responsibility import *

if __name__=="__main__":
    window=50
    # upcc_path=os.path.join(BASE_DIR,'excel/2-2-1更新UPCC.xls')
    # ipcc_path=os.path.join(BASE_DIR,'excel/2-2-1更新IPCC.xls')
    # upcc,ipcc=excel2m(upcc_path),excel2m(ipcc_path)

    # upcc_path=os.path.join(BASE_DIR,'excel/2-1-1更新UPCC.xls')
    # ipcc_path=os.path.join(BASE_DIR,'excel/2-1-1更新IPCC.xls')
    # upcc,ipcc=excel2m(upcc_path,True),excel2m(ipcc_path,True);

    upcc_path=os.path.join(BASE_DIR,'excel/2-1-2更新UPCC.xls')
    ipcc_path=os.path.join(BASE_DIR,'excel/2-1-2更新IPCC.xls')
    upcc,ipcc=excel2m(upcc_path,True),excel2m(ipcc_path,True);

    ans_over=get_over_corrcoef(ipcc,upcc,50,1,0.9);
    p1=get_optics_data(ans_over,50,ipcc,upcc,is_complex=True)
    ipccn,upccn=p1.get('ipccn'),p1.get('upccn')
    ipccn,upccn=np.array(ipccn),np.array(upccn)
    # print(ipccn.shape)
    data= np.concatenate((ipccn,upccn),axis=1);
    le=data.shape[0]
    res=get_optics(data,4);
    order,RD,CD=res.get('order'),res.get('RD'),res.get('CD');
    mark=get_cluster(le,order,RD,CD);
    # print(mark.shape)
    # print(order)
    # draw_scatter(ipcc,upcc,ipccn,upccn)
    # data=get_ordered_data(RD,order,data);
    # print(data)
    # draw_ordered_graph(range(len(data)),data)
    sections=get_three_section(le,mark,ipccn,upccn)
    one=sections.get('pccn_1');
    two=sections.get('pccn_2');
    three=sections.get('pccn_3');
    # draw_three_section(one[0],one[1],
    # two[0],two[1],three[0],three[1]);
    # print(len(one[0]))
    p=get_three_section_plsregress(one,two,three);
    # print(p.get('pccn_1_pls')[0])
   
    draw()

    






