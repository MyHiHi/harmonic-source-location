import sys,os
from sys import path
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
path.append(BASE_DIR)
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget,QLabel
window_wid,window_hei=700,500;
title='谐波源定位'
class Center(QtWidgets.QWidget):
    def __init__(self,  parent = None):
        QtWidgets.QWidget.__init__(self,  parent);
        self.setWindowTitle(title);
        self.resize(window_wid,  window_hei);
        self.center();
        self.is_client();
        self.read_excel();
        self.complex_simple();
        self.complex_complicate();
        self.no_complex_simple();
        self.no_complex_complicate();

    '''
    定性模式-有功功率法（定性分析主谐波源位置）
    '''
    def is_client(self):
        pass
    '''
    选取文件，读取
    '''
    def read_excel(self):
        pass
    '''
    有相位，简单模式
    '''
    def complex_simple(self):
        lb11 = QLabel('Zetcode',self)
        lb11.move(15,10)
    '''
    有相位,复杂模式
    '''
    def complex_complicate(self):
        pass
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

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,  
        (screen.height() - size.height()) / 2)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv) 
    qb = Center()
    qb.show()
    sys.exit(app.exec_())
