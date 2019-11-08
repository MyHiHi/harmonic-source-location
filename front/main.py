
import sys,os
from sys import path
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
path.append(BASE_DIR)

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *;
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from back.util import Util
from back.excel import Excel
from back.corrcoef import Corrcoef;
from back.optics import Optics;
from back.plsregress  import Plsregress
from time import sleep
window_wid, window_hei =990, 480
title = '单点谐波源定位';
ans_c='有功功率从用户侧指向系统侧, 主谐波源在用户侧';
ans_s='有功功率从系统侧指向用户侧 主谐波源在系统侧';
tip_w='结果大于0时,主谐波源在用户侧,否则系统侧,即结束程序 ：';
start_tip='请先定性分析主谐波源位置！然后选择文件';
red_style='color:red;font-weight:bold;';
big_style=red_style+'font-size:20px;text-align:center;';
small_style=red_style+'font-size:18px;text-align:center;';
blue_style='color:blue;font-weight:bold;font-size:15px';

error_two=['无','无']
class Center(QtWidgets.QWidget):
    def __init__(self,  parent=None):
        QtWidgets.QWidget.__init__(self,  parent);
        self.util=Util();
        self.switch=False;
        self.file_switch=False;
        self.setWindowTitle(title);
        self.resize(window_wid, window_hei)
        self.center();
        self.ipcc,self.upcc,self.is_complex=None,None,False;
        self.QVBox_whole=QVBoxLayout();
        self.setLayout(self.QVBox_whole);
        self.upcc_QL = QLineEdit();
        self.upcc_QL.setPlaceholderText('实数或复数');
        
        self.ipcc_QL = QLineEdit();
        self.ipcc_QL.setPlaceholderText('实数或复数');
        self.init_ui();
    def init_ui(self):
        self.is_client()
        self.read_excel()
        self.complex_simple()
        self.complex_complicate()
        self.no_complex_simple()
        self.no_complex_complicate()
    '''
    定性模式-有功功率法（定性分析主谐波源位置）
    '''
    def is_client(self):
        self.QHBox_top = QHBoxLayout();
        self.QHBox_tip=QHBoxLayout();
        top_title=QLabel('运行程序前：定性分析主谐波源位置');
        top_title.setStyleSheet(big_style);
        upcc_title = QLabel('电压值');
        ipcc_title = QLabel('电流值');
        tip = QLabel(tip_w);
        self.ans= QLabel('');
        self.ans.setStyleSheet(big_style);
        
        cal = QPushButton('定向主谐波源位置');
        cal.setStyleSheet(blue_style)
        cal.clicked.connect(self.cal);
        cancel = QPushButton('取消');
        cancel.clicked.connect(self.cancel);
        self.QHBox_top.addWidget(upcc_title,);
        self.QHBox_top.addWidget(self.upcc_QL, );
        self.QHBox_top.addWidget(ipcc_title,);
        self.QHBox_top.addWidget(self.ipcc_QL, );
        self.QHBox_top.addWidget(cal,);
        self.QHBox_top.addWidget(cancel,);
        self.QHBox_tip.addWidget(tip, );
        self.QHBox_tip.addWidget(self.ans, );
        self.QVBox_whole.addWidget(top_title,0,Qt.AlignHCenter);
        self.QVBox_whole.addLayout(self.QHBox_top);
        self.QVBox_whole.addLayout(self.QHBox_tip);
        self.QVBox_whole.addStretch(1);
    '''
    选取文件，读取
    '''
    def read_excel(self):
        QHBox_excel = QHBoxLayout();
        excel_tip = QLabel('请选择文件');
        self.open = QPushButton('打开EXCEL(电流与电压)文件');
        self.open.setStyleSheet(blue_style);
        self.open.clicked.connect(self.open_file);
        self.excel_ans = QLabel('');
        self.excel_ans.setStyleSheet(red_style);
        QHBox_excel.addStretch(1);
        QHBox_excel.addWidget(excel_tip);
        QHBox_excel.addWidget(self.open);
        QHBox_excel.addWidget(self.excel_ans);
        QHBox_excel.addStretch(1);
        self.QVBox_whole.addLayout(QHBox_excel);
    '''
    有相位，简单模式
    '''

    def complex_simple(self):
        QHBox_complex_simple = QHBoxLayout();
        QVBox_complex_simple = QVBoxLayout();
        QHBox_complex_simple2 = QHBoxLayout();
        QHBox_complex_simple3 = QHBoxLayout();
        c_tip = QLabel('（非）相位模式');
        c_tip.setStyleSheet(big_style);
        c_no = QLabel('不考虑背景谐波电压波动和阻抗变化');
        c_no.setStyleSheet(small_style);
        complex_simple_start = QPushButton('简单模式的发射水平和责任值计算');
        complex_simple_start.setStyleSheet(blue_style);
        complex_simple_start.clicked.connect(self.complex_sim_start);
        # zs_tip = QLabel('Zs: ');
        # self.zs=QLineEdit();
        # self.zs.setReadOnly(True);
        us_tip = QLabel('系统侧谐波发射水平（均值）:');
        self.us=QLineEdit();
        self.us.setReadOnly(True);
        ipcc_zs_tip = QLabel('用户侧谐波发射水平（均值）');
        self.ipcc_zs=QLineEdit();
        self.ipcc_zs.setReadOnly(True);
        resp_c_mean_tip = QLabel('用户侧谐波责任（均值）');
        self.resp_ck_mean=QLineEdit("");
        self.resp_ck_mean.setReadOnly(True);
        resp_s_mean_tip = QLabel('系统侧谐波责任（均值）');
        self.resp_sk_mean=QLineEdit();
        self.resp_sk_mean.setReadOnly(True);
        draw_resp = QPushButton('生成谐波责任图');
        draw_resp.clicked.connect(self.draw_respons);
        QVBox_complex_simple.addWidget(c_tip,0,Qt.AlignHCenter);
        QHBox_complex_simple3.addWidget(c_no,0,Qt.AlignHCenter);
        QHBox_complex_simple3.addWidget(complex_simple_start,0,Qt.AlignHCenter);
        # QHBox_complex_simple.addWidget(zs_tip);
        # QHBox_complex_simple.addWidget(self.zs);
        QHBox_complex_simple.addWidget(us_tip);
        QHBox_complex_simple.addWidget(self.us);
        QHBox_complex_simple.addWidget(ipcc_zs_tip);
        QHBox_complex_simple.addWidget(self.ipcc_zs);
        QHBox_complex_simple2.addWidget(resp_c_mean_tip);
        QHBox_complex_simple2.addWidget(self.resp_ck_mean);
        QHBox_complex_simple2.addWidget(resp_s_mean_tip);
        QHBox_complex_simple2.addWidget(self.resp_sk_mean);
        QHBox_complex_simple2.addWidget(draw_resp);
        self.QVBox_whole.addLayout(QVBox_complex_simple);
        self.QVBox_whole.addLayout(QHBox_complex_simple3);
        self.QVBox_whole.addLayout(QHBox_complex_simple);
        self.QVBox_whole.addLayout(QHBox_complex_simple);
        self.QVBox_whole.addLayout(QHBox_complex_simple2);



    '''
    有相位,复杂模式
    '''

    def complex_complicate(self):
        QHBox_complex_com = QHBoxLayout();
        QHBox_complex_com1 = QHBoxLayout();
        QHBox_complex_com2 = QHBoxLayout();
        QHBox_complex_com3 = QHBoxLayout();
        QHBox_complex_com4 = QHBoxLayout();
        QHBox_complex_com5 = QHBoxLayout();
        QHBox_complex_com6 = QHBoxLayout();
        QHBox_complex_com7 = QHBoxLayout();
        QHBox_complex_com8 = QHBoxLayout();
        c_yes = QLabel('考虑背景谐波电压波动和阻抗变化');
        c_yes.setStyleSheet(small_style);
        complex_simple_start = QPushButton('复杂模式的发射水平和责任值计算');
        complex_simple_start.setStyleSheet(blue_style);
        tip_1 = QLabel('谐波发射水平（均值）');
        tip_1.setStyleSheet(red_style);
        tip_2 = QLabel('谐波责任（均值）');
        tip_2.setStyleSheet(red_style);
        window_tip = QLabel('滑动窗口参数: ');
        self.window_QL=QLineEdit('100');
        step_tip = QLabel('每次后移参数: ');
        self.step_QL=QLineEdit('1');
        e_tip = QLabel('筛选参数: ');
        self.e_QL=QLineEdit('0.85');
        e_cluster_tip = QLabel('提取凹陷区域聚类参数: ');
        self.e_cluster_QL=QLineEdit('0.02');
        draw_order_graph = QPushButton('生成有序队列图');
        draw_order_graph.clicked.connect(self.draw_ordered_graph);
        draw_three_section = QPushButton('生成聚类图');
        draw_three_section.clicked.connect(self.draw_three_sections);
        us_tip_1 = QLabel('段一 系统侧谐波发射水平（均值）:');
        self.us_1=QLineEdit();
        self.us_1.setReadOnly(True);
        ipcc_zs_tip_1 = QLabel('段一 用户侧谐波发射水平（均值）');
        self.ipcc_zs_1=QLineEdit();
        self.ipcc_zs_1.setReadOnly(True);
        us_tip_2 = QLabel('段二 系统侧谐波发射水平（均值）:');
        self.us_2=QLineEdit();
        self.us_2.setReadOnly(True);
        ipcc_zs_tip_2 = QLabel('段二 用户侧谐波发射水平（均值）');
        self.ipcc_zs_2=QLineEdit();
        self.ipcc_zs_2.setReadOnly(True);
        us_tip_3 = QLabel('段三 系统侧谐波发射水平（均值）:');
        self.us_3=QLineEdit();
        self.us_3.setReadOnly(True);
        ipcc_zs_tip_3 = QLabel('段三 用户侧谐波发射水平（均值）');
        self.ipcc_zs_3=QLineEdit();
        self.ipcc_zs_3.setReadOnly(True);
        resp_s_tip_1 = QLabel('段一 系统侧谐波责任（均值）:');
        self.resp_s_1=QLineEdit();
        self.resp_s_1.setReadOnly(True);
        resp_c_tip_1 = QLabel('段一 用户侧谐波责任（均值）');
        self.resp_c_1=QLineEdit();
        self.resp_c_1.setReadOnly(True);
        resp_s_tip_2 = QLabel('段二 系统侧谐波责任（均值）:');
        self.resp_s_2=QLineEdit();
        self.resp_s_2.setReadOnly(True);
        resp_c_tip_2 = QLabel('段二 用户侧谐波责任（均值）');
        self.resp_c_2=QLineEdit();
        self.resp_c_2.setReadOnly(True);
        resp_s_tip_3 = QLabel('段三 系统侧谐波责任（均值）:');
        self.resp_s_3=QLineEdit();
        self.resp_s_3.setReadOnly(True);
        resp_c_tip_3 = QLabel('段三 用户侧谐波责任（均值）');
        self.resp_c_3=QLineEdit();
        self.resp_c_3.setReadOnly(True);
        resp_c_mean_tip = QLabel('用户侧谐波责任（均值）');
        self.resp_c_mean=QLineEdit();
        self.resp_c_mean.setReadOnly(True);
        resp_s_mean_tip = QLabel('系统侧谐波责任（均值）');
        self.resp_s_mean=QLineEdit();
        self.resp_s_mean.setReadOnly(True);
        complex_simple_start.clicked.connect(self.complex_com_start);
        QHBox_complex_com.addWidget(c_yes,0,Qt.AlignHCenter);
        QHBox_complex_com.addWidget(complex_simple_start,0,Qt.AlignHCenter);
        QHBox_complex_com1.addWidget(window_tip);
        QHBox_complex_com1.addWidget(self.window_QL);
        QHBox_complex_com1.addWidget(step_tip);
        QHBox_complex_com1.addWidget(self.step_QL);
        QHBox_complex_com1.addWidget(e_tip);
        QHBox_complex_com1.addWidget(self.e_QL);
        QHBox_complex_com1.addWidget(e_cluster_tip);
        QHBox_complex_com1.addWidget(self.e_cluster_QL);
        QHBox_complex_com2.addWidget(us_tip_1);
        QHBox_complex_com2.addWidget(self.us_1);
        QHBox_complex_com2.addWidget(ipcc_zs_tip_1);
        QHBox_complex_com2.addWidget(self.ipcc_zs_1);
        QHBox_complex_com3.addWidget(us_tip_2);
        QHBox_complex_com3.addWidget(self.us_2);
        QHBox_complex_com3.addWidget(ipcc_zs_tip_2);
        QHBox_complex_com3.addWidget(self.ipcc_zs_2);
        QHBox_complex_com4.addWidget(us_tip_3);
        QHBox_complex_com4.addWidget(self.us_3);
        QHBox_complex_com4.addWidget(ipcc_zs_tip_3);
        QHBox_complex_com4.addWidget(self.ipcc_zs_3);
        QHBox_complex_com5.addWidget(draw_order_graph,0,Qt.AlignHCenter);
        QHBox_complex_com5.addWidget(draw_three_section,0,Qt.AlignHCenter);
        QHBox_complex_com6.addWidget(resp_s_tip_1);
        QHBox_complex_com6.addWidget(self.resp_s_1);
        QHBox_complex_com6.addWidget(resp_c_tip_1);
        QHBox_complex_com6.addWidget(self.resp_c_1);
        QHBox_complex_com7.addWidget(resp_s_tip_2);
        QHBox_complex_com7.addWidget(self.resp_s_2);
        QHBox_complex_com7.addWidget(resp_c_tip_2);
        QHBox_complex_com7.addWidget(self.resp_c_2);

        QHBox_complex_com8.addWidget(resp_s_tip_3);
        QHBox_complex_com8.addWidget(self.resp_s_3);
        QHBox_complex_com8.addWidget(resp_c_tip_3);
        QHBox_complex_com8.addWidget(self.resp_c_3);
        self.QVBox_whole.addLayout(QHBox_complex_com);
        self.QVBox_whole.addLayout(QHBox_complex_com1);
        self.QVBox_whole.addLayout(QHBox_complex_com5);
        self.QVBox_whole.addWidget(tip_1,0,Qt.AlignHCenter);
        self.QVBox_whole.addLayout(QHBox_complex_com2);
        self.QVBox_whole.addLayout(QHBox_complex_com3);
        self.QVBox_whole.addLayout(QHBox_complex_com4);
        self.QVBox_whole.addWidget(tip_2,0,Qt.AlignHCenter);
        self.QVBox_whole.addLayout(QHBox_complex_com6);
        self.QVBox_whole.addLayout(QHBox_complex_com7);
        self.QVBox_whole.addLayout(QHBox_complex_com8);
    '''
    无相位，简单模式
    '''

    def no_complex_simple(self):
        pass
    '''
    无相位,复杂模式
    '''

    def no_complex_complicate(self):
        pass
    def cal(self):
        ipcc,upcc=self.ipcc_QL.text(),self.upcc_QL.text();
        if ipcc=='' or upcc =='' :
            self.Info();
        else:
            try:
                ipcc,upcc=eval(ipcc),eval(upcc);
                ans=self.util.IsClinet(ipcc,upcc);
                if ans:
                    self.ans.setText(ans_c);
                    self.Info(word='主谐波源在用户侧,是否进行责任划分模式？');
                    self.switch=True;
                else:
                    self.ans.setText(ans_s);
                    self.warn(word='主谐波源在系统侧，退出程序')
                    QCoreApplication.instance().quit();
            except Exception as e:
                print(e)
                self.warn(word='输入有误！请重新输入！')
                self.cancel();
    def warn(self,word=''):
        QMessageBox.about(self,'提示',word);
    # def look(self):
    #     if not self.switch:
    #         self.warn(word='请先定性分析主谐波源位置！');
    #         return ;
    def complex_sim_start(self):
        if not self.switch or not self.file_switch:
            self.warn(word=start_tip);
            return ;
        self.pls=Plsregress(self.ipcc,self.upcc);  
        plsr=self.pls.get_plsregress();
        zs,us=plsr.get('zs'),plsr.get('us');
        dev=self.pls.get_c_s_dev_mean();
        c_dev,s_dev=dev.get('c_dev'),dev.get('s_dev');
        d_s_mean=self.util.get_responsibility_mean(self.ipcc,self.upcc,zs);
        
        dc_mean,ds_mean=d_s_mean.get('dc_mean'),d_s_mean.get('ds_mean');
        # self.zs.setText(str(zs));
        self.us.setText(str(us));
        self.ipcc_zs.setText(str(c_dev));
        self.resp_ck_mean.setText(str(dc_mean));
        self.resp_sk_mean.setText(str(ds_mean));
    def complex_com_start(self):
        if not self.switch or not self.file_switch:
            self.warn(word=start_tip);
            return ;
        corrcoef=Corrcoef(self.ipcc,self.upcc);
        window,step,e,self.e_cluster=eval(self.window_QL.text()),eval(self.step_QL.text()),eval(self.e_QL.text()),eval(self.e_cluster_QL.text())
        p=corrcoef.get_optics_data(window,step,e,self.is_complex);
        ipccn,upccn=p.get('ipccn'),p.get('upccn');
        self.op=Optics(ipccn,upccn,self.e_cluster);
        dev_mean=self.op.get_three_section_c_s_dev_mean();
        dev_1,dev_2,dev_3=dev_mean.get('dev_1'),dev_mean.get('dev_2'),dev_mean.get('dev_3');
        try:
            c_dev_1=dev_1.get('c_dev');
            s_dev_1=dev_1.get('s_dev');
        except:
            c_dev_1,s_dev_1=error_two;
        try:
            c_dev_2=dev_2.get('c_dev');
            s_dev_2=dev_2.get('s_dev');
        except:
            c_dev_2,s_dev_2=error_two;
        try:
            c_dev_3=dev_3.get('c_dev');
            s_dev_3=dev_3.get('s_dev');
        except:
            c_dev_3,s_dev_3=error_two;
        self.us_1.setText(str(s_dev_1));
        self.ipcc_zs_1.setText(str(c_dev_1));
        self.us_2.setText(str(s_dev_2));
        self.ipcc_zs_2.setText(str(c_dev_2));
        self.us_3.setText(str(s_dev_3));
        self.ipcc_zs_3.setText(str(c_dev_3));

        resp_mean=self.op.get_three_section_responsibility_mean();
        print(resp_mean)
        try:
            resp_me_1=resp_mean.get('pccn_1_resp_mean');
            dc_1,ds_1=resp_me_1.get('dc_mean'),resp_me_1.get('ds_mean')
        except Exception as e:
            print(e)
            dc_1,ds_1=error_two;
        try:
            resp_me_2=resp_mean.get('pccn_2_resp_mean');
            dc_2,ds_2=resp_me_2.get('dc_mean'),resp_me_2.get('ds_mean')
        except:
            dc_2,ds_2=error_two;
        try:
            resp_me_3=resp_mean.get('pccn_3_resp_mean');
            dc_3,ds_3=resp_me_3.get('dc_mean'),resp_me_3.get('ds_mean')
        except:
            dc_3,ds_3=error_two;
        self.resp_s_1.setText(str(ds_1));
        self.resp_c_1.setText(str(dc_1));
        self.resp_s_2.setText(str(ds_2));
        self.resp_c_2.setText(str(dc_2));
        self.resp_s_3.setText(str(ds_3));
        self.resp_c_3.setText(str(dc_3));
        
        


    def draw_ordered_graph(self):
        self.op.draw_ordered_graph();
    def draw_three_sections(self):
        self.op.draw_three_section();

    def draw_respons(self):
        self.pls.draw_responsibility();
    # def warn(self):

    def cancel(self):
        self.ipcc_QL.clear();
        self.upcc_QL.clear();
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
    def open_file(self):
        if not self.switch:
            self.warn(word=start_tip);
            return ;
        ipcc_path, filetype = QFileDialog.getOpenFileName(self,
                  "选取电流文件",
                  "./",
                  "Excel Files (*.xls);;Excel Files (*.xlsx)");
        upcc_path, filetype = QFileDialog.getOpenFileName(self,
                  "选取电压文件",
                  "./",
                  "Excel Files (*.xls);;Excel Files (*.xlsx)");
        if not(ipcc_path and upcc_path):
            self.Info(word="打开失败，请重试！");
            return;
        
        else:
            self.file_switch=True;
            ipcc_tip,upcc_tip=ipcc_path.split('/')[-1],upcc_path.split('/')[-1]
            self.open.setText(ipcc_tip+" + "+upcc_tip)
        self.excel=Excel(ipcc_path,upcc_path);
        p=self.excel.read();
        self.ipcc,self.upcc,self.is_complex=p.get('ipcc'),p.get('upcc'),p.get('is_complex');
        if self.is_complex:
            self.excel_ans.setText('检测出文件含有复数,请选择相位模式！');
        else:
            self.excel_ans.setText('检测出文件为实数，请选择非相位模式！');

        
        
    def Info(self,title='警告!',word='请输入完整数据!'):
        print('提示！')
        button=QMessageBox.question(self, title, word, QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if button == QMessageBox.No:
            QCoreApplication.instance().quit();
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    qb = Center();
    font=app.font();
    qb.setWindowOpacity(0.94) # 设置窗口透明度
    # pe = QPzalette()
    qb.setAutoFillBackground(True);
    qb.setStyleSheet('''
    background-color:#D2E9FF;
    font-size:13px
    ''');
    # qb.setPalette(pe)
    font.setFamily('微软雅黑');
    app.setFont(font);
    qb.show();

    sys.exit(app.exec_())
