import numpy as N
import numpy as np
import pylab as P
from matplotlib import pyplot as plt
from plsregress import Plsregress
from scipy.spatial.distance import pdist, squareform
from util import Util


class Optics(object):
    def __init__(self, ipccn, upccn):
        self.ipccn, self.upccn = ipccn, upccn
        self.data = np.concatenate((ipccn, upccn), axis=1)
        self.util = Util()
        self.error = [None, None];
        self.error_dev=None;

    def get_optics(self, k=4, distMethod='euclidean'):
        x = self.data
        if len(x.shape) > 1:
            m, n = x.shape
        else:
            m = x.shape[0]
            n == 1
        try:
            D = squareform(pdist(x, distMethod))
            distOK = True
        except:
            print("squareform or pdist error")
            distOK = False
        CD = N.zeros(m)
        RD = N.ones(m)*1E10
        for i in list(range(m)):
            tempInd = D[i].argsort()
            tempD = D[i][tempInd]
            CD[i] = tempD[k]
        order = []
        seeds = N.arange(m, dtype=N.int)

        ind = 0
        while len(seeds) != 1:
            ob = seeds[ind]
            seedInd = N.where(seeds != ob)
            seeds = seeds[seedInd]

            order.append(ob)
            tempX = N.ones(len(seeds))*CD[ob]
            tempD = D[ob][seeds]

            temp = N.column_stack((tempX, tempD))
            mm = N.max(temp, axis=1)
            ii = N.where(RD[seeds] > mm)[0]
            RD[seeds[ii]] = mm[ii]
            ind = N.argmin(RD[seeds])
        order.append(seeds[0])
        RD[0] = 0
        return {'RD': RD, 'CD': CD, 'order': order}

    def euclid(self, i, x):
        """euclidean(i, x) -> euclidean distance between x and y"""
        y = N.zeros_like(x)
        y += 1
        y *= i
        if len(x) != len(y):
            raise ValueError
        d = (x-y)**2
        return N.sqrt(N.sum(d, axis=1))

    def get_ordered_data(self):
        optics = self.get_optics(k=4)
        RD, order = optics.get('RD'), optics.get('order')
        le = self.data.shape[0]
        rr = np.zeros((le, 1))
        for i in range(le):
            rr[i] = RD[order[i]]
        return rr

    def draw_ordered_graph(self, label1='用户侧', title='有序队列图', xlabel='', ylabel='可达距离'):
        y1 = self.get_ordered_data()
        x1 = range(len(y1))
        plt.figure(title, figsize=(6, 4))
        plt.title(title)
        plt.plot(x1, y1, c='b')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(loc='upper left')
        plt.show()

    def get_cluster(self, e=0.02):
        le = self.data.shape[0]
        optics = self.get_optics(k=4)
        order, RD, CD = optics.get('order'), optics.get('RD'), optics.get('CD')
        mark = np.zeros((le, 1))
        ID = 0
        for i in range(le):
            xi = order[i]
            if RD[xi] > e:
                if CD[xi] <= e:
                    ID += 1
                    mark[xi] = ID
                else:
                    mark[xi] = 0
            else:
                mark[xi] = ID
        return mark

    def get_three_section(self, e=0.02):
        le = self.data.shape[0]
        mark = self.get_cluster(e)
        ipccn_1, upccn_1 = [], []
        ipccn_2, upccn_2 = [], []
        ipccn_3, upccn_3 = [], []
        ipccn, upccn = self.ipccn, self.upccn
        for i in range(le):
            if mark[i] == 0:
                ipccn_1.append(ipccn[i])
                upccn_1.append(upccn[i])
            elif mark[i] == 1:
                ipccn_2.append(ipccn[i])
                upccn_2.append(upccn[i])
            else:
                ipccn_3.append(ipccn[i])
                upccn_3.append(upccn[i])
        return {'pccn_1': [ipccn_1, upccn_1],
                'pccn_2': [ipccn_2, upccn_2],
                'pccn_3': [ipccn_3, upccn_3],
                }

    def draw_three_section(self, e=0.02, color1='b', color2='g', color3='r', label1='段一', label2='段二', label3='段三', title='聚类图', xlabel='IPCC/A', ylabel='UPCC/V'):
        pafig, ax = plt.subplots(figsize=(6, 4))
        sections = self.get_three_section(e)
        one = sections.get('pccn_1')
        two = sections.get('pccn_2')
        three = sections.get('pccn_3')
        ax.scatter(three[0], three[1], color=color3, label=label3)
        ax.scatter(two[0], two[1], color=color2, label=label2)
        ax.scatter(one[0], one[1], color=color1, label=label1)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend(loc='upper left')
        plt.show()

    def get_three_section_plsregress(self, e=0.02):
        try:
            sections = self.get_three_section(e)
            try:
                ipccn_1, upccn_1 = sections.get('pccn_1')
                one = Plsregress(ipccn_1, upccn_1).get_plsregress()
                zs_1, us_1 = one.get('zs'), one.get('us')
            except:
                zs_1, us_1 = self.error

            try:
                ipccn_2, upccn_2 = sections.get('pccn_2')
                two = Plsregress(ipccn_2, upccn_2).get_plsregress()
                zs_2, us_2 = two.get('zs'), two.get('us')
            except:
                zs_2, us_2 = self.error

            try:
                ipccn_3, upccn_3 = sections.get('pccn_3')
                three = Plsregress(ipccn_3, upccn_3).get_plsregress()
                zs_3, us_3 = three.get('zs'), three.get('us')
            except:
                zs_3, us_3 = self.error

            # ipccn_3,upccn_3=sections.get('pccn_3');
            # one=Plsregress(ipccn_1,upccn_1).get_plsregress();
            # zs_1,us_1=one.get('zs'),one.get('us');
            # two=Plsregress(ipccn_2,upccn_2).get_plsregress();
            # zs_2,us_2=two.get('zs'),two.get('us');
            # three=Plsregress(ipccn_3,upccn_3).get_plsregress();
            # zs_3,us_3=three.get('zs'),three.get('us');
        except Exception as e:
            return None
        return {'pccn_1_pls': {'zs_1': zs_1, "us_1": us_1},
                'pccn_2_pls': {'zs_2': zs_2, 'us_2': us_2},
                'pccn_3_pls': {'zs_3': zs_3, 'us_3': us_3}}

    def get_three_section_responsibility_mean(self, e=0.02):
        sections = self.get_three_section(e)
        ipccn_1, upccn_1 = sections.get('pccn_1')
        ipccn_2, upccn_2 = sections.get('pccn_2')
        ipccn_3, upccn_3 = sections.get('pccn_3')
        pccn_pls = self.get_three_section_plsregress(e)
        zs_1 = pccn_pls.get('pccn_1_pls').get('zs_1')
        zs_2 = pccn_pls.get('pccn_2_pls').get('zs_2')
        zs_3 = pccn_pls.get('pccn_3_pls').get('zs_3')
        pccn_1_resp_mean = self.util.get_responsibility_mean(
            ipccn_1, upccn_1, zs_1)
        pccn_2_resp_mean = self.util.get_responsibility_mean(
            ipccn_2, upccn_2, zs_2)
        pccn_3_resp_mean = self.util.get_responsibility_mean(
            ipccn_3, upccn_3, zs_3)
        return {'pccn_1_resp_mean': pccn_1_resp_mean,
                'pccn_2_resp_mean': pccn_2_resp_mean, "pccn_3_resp_mean": pccn_3_resp_mean}

    def get_three_section_c_s_dev_mean(self, e=0.02):
        sections = self.get_three_section(e)
        try:
            ipccn_1, upccn_1 = sections.get('pccn_1')
            one = Plsregress(ipccn_1, upccn_1).get_plsregress()
            zs_1, us_1 = one.get('zs'), one.get('us');
            dev_1=self.util.get_c_s_dev_mean(ipccn_1,zs_1,us_1);
        except:
            dev_1=self.error_dev;

        try:
            ipccn_2, upccn_2 = sections.get('pccn_2')
            two = Plsregress(ipccn_2, upccn_2).get_plsregress()
            zs_2, us_2 = two.get('zs'), two.get('us');
            dev_2=self.util.get_c_s_dev_mean(ipccn_2,zs_2,us_2);
        except:
            dev_2=self.error_dev;

        try:
            ipccn_3, upccn_3 = sections.get('pccn_3')
            three = Plsregress(ipccn_3, upccn_3).get_plsregress()
            zs_3, us_3 = three.get('zs'), three.get('us');
            dev_3=self.util.get_c_s_dev_mean(ipccn_3,zs_3,us_3);
        except:
            dev_3=self.error_dev;
        return {'dev_1':dev_1,'dev_2':dev_2,'dev_3':dev_3};
