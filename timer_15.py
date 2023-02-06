import time, sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui

form_class = uic.loadUiType("timer_for_15.ui")[0]

#소팀 1에서 의뢰한거
class TimerQT(QMainWindow, form_class): 
    started = False
    start_time = None
    def __init__(self):
        #초기 설정
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("도둑포커 디렉터용 파일")

        self.btn_start.clicked.connect(self.btn_startF)
        self.timer_num.setSmallDecimalPoint(True)
        

    def btn_startF(self):
        if self.started :
            diff = time.time() - self.start_time
            self.timer_num.display(diff)
            
        else:
            self.timer_num.display("88888")
            self.start_time = time.time()

        self.started = not self.started




if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    myWindow = TimerQT() 

    myWindow.show()

    app.exec_()