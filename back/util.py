import math
import numpy as np

class Util(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs);
        self.error=[None,None]
    def IsClinet(self,ipcc,upcc):
        '''
        如果主谐波源在系统侧结束程序\n
        如果主谐波源在用户侧询问是否跳转到模式2\n
        定量责任划分模式，如果不结束程序\n
        '''
        degree=self.angle_one(upcc)-self.angle_one(ipcc);
        print(degree)
        P=abs(upcc)*abs(ipcc)*math.cos(degree);
        print('******: ',P)
        return P>0 ;
    '''
    type of pcc: complex;
    return degree;
    '''
    # 
    def get_degree_from_complex(self,pcc):
        r1,r2=pcc.real,pcc.imag;
        m=np.sqrt(r1*r1+r2*r2)
        degree=np.arccos(r1/m)*180/math.pi
        degree=np.arccos(r1/m)*math.pi/180
        return degree;
    def is_complex(self,data):
        return type(eval(str(data))) == type(1+1j);
    def get_responsibility_mean(self,ipcc,upcc,zs):
        '''
        Return :
            *100(%)
        '''
        # print('zs: ',zs)
        ipcc,upcc,zs=np.array(ipcc),np.array(upcc),np.array(zs);
        t1=ipcc*zs;
        t2=upcc;
        deg=self.angle(t1)-self.angle(t2);
        cos_deg=np.cos(deg);
        # print(np.mean(np.abs(zs*ipcc)/np.abs(upcc)),"MMMMMMMMMMMMMMMMMM")
        try:
            dc=np.abs(zs*ipcc)/np.abs(upcc)*cos_deg;
            dc_mean=np.mean(dc);
            ds_mean=1-dc_mean;
        except:
            dc_mean,ds_mean=self.error
        return {'dc_mean':dc_mean,'ds_mean':ds_mean}
    def angle_one(self,x):
        return math.atan2(x.imag,x.real)
    def angle(self,x):
        return np.array([math.atan2(i.imag,i.real) for i in x])
    def get_c_s_dev_mean(self,ipcc,zs,us):
        i_z_mean=np.mean(ipcc*zs);
        u_mean=np.mean(us);
        return {'c_dev':i_z_mean,'s_dev':u_mean}


