import pandas as pd
 
import scipy
 
from scipy import io
 
import os
 
 
 
# matPath='.\\mat\\'
matPath=r'C:\Users\Administrator\Desktop\我的资料\项目\谐波源定位\我的资料\单点法软件程序数据参考\输入数据\输入数据'
 
outPath=r'C:\Users\Administrator\Desktop\我的资料\项目\谐波源定位\我的资料\单点法软件程序数据参考\输入数据\csv'
 
for i in os.listdir(matPath):
    
    inputFile=os.path.join(matPath,i)
    print(inputFile)
    outputFile=os.path.join(outPath,os.path.split(i)[1][:-4]+'.csv')
    features_struct = scipy.io.loadmat(inputFile)
    
    data=list(features_struct.values())[-1]
    
    dfdata = pd.DataFrame(data)
    
    dfdata.to_csv(outputFile, index=False)

print('ok')
