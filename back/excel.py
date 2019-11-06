import numpy as np
import xlrd
from util import *

np.set_printoptions(precision=20)
np.set_printoptions(suppress=True)
class Excel(object):
    '''
    parmas:  ipcc_path,
             upcc_path
    '''
    def __init__(self,ipcc_path,upcc_path):
        self.ipcc_path=ipcc_path;
        self.upcc_path=upcc_path;
        self.util=Util();
    '''
    return: dict----> 
    type of each:  numpy.
    including is_complex
    '''
    def read(self):
        data1,data2 = xlrd.open_workbook(self.ipcc_path),xlrd.open_workbook(self.upcc_path);
        table1,table2 = data1.sheets()[0],data2.sheets()[0];
        nrows1,nrows2 = table1.nrows,table2.nrows;
        ncols1,ncols2 = table1.ncols  ,table2.ncols;
        data=table1.col_values(0)[0];
        is_complex = self.util.is_complex(data);
        if is_complex:
            datamatrix1 = np.zeros((nrows1 ,ncols1),dtype="complex128");
            datamatrix2 = np.zeros((nrows2, ncols2),dtype="complex128");
        else:
            datamatrix1 = np.zeros((nrows1, ncols1),dtype="float64");
            datamatrix2 = np.zeros((nrows2, ncols2),dtype="float64");
        '''
        默认：ncols1=ncols2
        '''
        for x in range(ncols1):
            cols1 = table1.col_values(x);
            cols2 = table2.col_values(x);
            if is_complex:
                cols1=[(complex(i)) for i in cols1];
                cols2=[(complex(i)) for i in cols2];
            else:
                cols1=[i for i in cols1];
                cols2=[i for i in cols2];
            cols1 = np.matrix(cols1)  # 把list转换为矩阵进行矩阵操作
            cols2 = np.matrix(cols2)  # 把list转换为矩阵进行矩阵操作
            datamatrix1[:, x] = cols1 # 把数据进行存储
            datamatrix2[:, x] = cols2 # 把数据进行存储
        return {'ipcc':datamatrix1,'upcc':datamatrix2,'is_complex':is_complex}


