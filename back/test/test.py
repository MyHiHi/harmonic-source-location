# with open(r'D:\谐波源python\matlab\upcc.txt','r') as f:
#     p=f.read()
#     print(p)
import math;
def sqrt(x):
    if x<=1:
        return x;
    r=x;
    e=x/r
    while r>e:
        r=(r+x/r)//2;
        e=x/r;
    return int(r);
print(sqrt(6))