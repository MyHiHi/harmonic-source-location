import numpy as np;
class Corrcoef(object):
    '''
    target: Corrcoef between ipcc and upcc
    '''
    def __init__(self, ipcc,upcc):
        self.ipcc=ipcc;
        self.upcc=upcc;
   
    def get_over_corrcoef_data(self,window=100,step=1,params=0.85):
        if step>=window:return False;
        le=self.ipcc.shape[0];
        rag=le-window+1;
        ans_over=[];
        ipcc,upcc=np.abs(self.ipcc),np.abs(self.upcc);
        for i in range(0,rag,step):
            ki,ku=ipcc[i:i+window],upcc[i:i+window];
            p1=np.corrcoef(ki,ku,rowvar=False);
            p3=p1[1,0];
            if p3>params:
                ans_over.append(i)
        return np.array(ans_over);
    '''
    return: numpy.ndarray of corrcoef over params between ipcc+window 
    and upcc+window over step
    '''
    def get_optics_data(self,window=100,step=1,params=0.85,is_complex=False):
        try:
            ans_over=self.get_over_corrcoef_data(window,step, params);
            ip_le=len(ans_over)+window-1;
        except:
            return;
        if is_complex:
            ipccn,upccn=np.zeros((ip_le,1),dtype="complex128"),np.zeros((ip_le,1),dtype="complex128");
        else:
            ipccn,upccn=np.zeros((ip_le,1),dtype="float64"),np.zeros((ip_le,1),dtype="float64");
        j=0;
        for i in ans_over:
            le1,le2=j+window,i+window;
            ipccn[j:le1]=self.ipcc[i:le2];
            upccn[j:le1]=self.upcc[i:le2];
            j+=1;
        return {'ipccn':ipccn,'upccn':upccn}


    