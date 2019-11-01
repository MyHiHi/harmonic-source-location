from sklearn import linear_model
import numpy as np
import scipy.linalg as la
from util import Util
from matplotlib import pyplot as plt;
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  
class Plsregress(object):
    def __init__(self,ipcc,upcc):
        self.ipcc=np.array(ipcc);
        self.upcc=np.array(upcc);
        self.util=Util();
    def get_plsregress(self):
        try:
            ipcc,upcc=self.ipcc,self.upcc;
            A = np.hstack([ipcc**0, ipcc**1]);
            sol, r, rank, s =la.lstsq(A,upcc);
        except Exception as e:
            return None;
        return {'zs':sol[1],'us':sol[0]};
    
    def get_responsibility(self):
        '''
        Return :
            *100(%)
            abs(numpy.ndarray) of dc and ds
        '''
        zs=np.array(self.get_plsregress().get('zs'));
        ipcc,upcc=self.ipcc,self.upcc;
        t1=ipcc*zs;
        t2=upcc;
        
        deg=self.util.get_degree_from_complex(t1)-self.util.get_degree_from_complex(t2);
        cos_deg=np.cos(deg);
        dc=np.abs(ipcc*zs)/np.abs(upcc)*cos_deg;
        return {'dc':dc*100,'ds':(1-dc)*100};
    def draw_responsibility(self,label1='用户侧',label2='系统侧',title='实时谐波责任图',xlabel='时间',ylabel='谐波责任(%)'):
        resp=self.get_responsibility();
        y1,y2=resp.get('dc'),resp.get('ds');
        x1,x2=(range(len(y1))),(range(len(y2)))
        plt.figure(title,figsize=(7,5));
        plt.subplot(211);
        plt.title(title);
        plt.plot(x1,y1,c='red',label='用户侧');
        plt.xlabel(xlabel);
        plt.ylabel(ylabel);
        plt.legend(loc='upper left');
        if x2!=None:
            plt.subplots_adjust(hspace=0.3,wspace=0.7);
            plt.subplot(212)
            plt.plot(x2,y2,c='b',label=label2);
            plt.xlabel(xlabel);
            plt.ylabel(ylabel);
            plt.legend(loc='upper left');
        plt.show();
    def get_c_s_dev_mean(self):
        pls=self.get_plsregress();
        zs,us=pls.get('zs'),pls.get('us');
        return self.util.get_c_s_dev_mean(self.ipcc,zs,us);