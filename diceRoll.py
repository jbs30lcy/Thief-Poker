from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
import random, sys
import time

form_class = uic.loadUiType("DiceRollQT.ui")[0]

class DiceRollQT(QMainWindow, form_class): #QT로 만든 Director 프로그램

    def __init__(self):
        #초기 설정
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("다이스롤 전용 파일")
        
        #버튼에 기능 연결
        self.btn_diceStart.clicked.connect(self.btn_dice_start)
        
    def btn_dice_start(self):
        for i in range(5 ):
            dice = random.randrange(1, 7)
            self.txt_diceNum.setText(str(dice))
            time.sleep(5)
        

if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    myWindow = DiceRollQT() 

    myWindow.show()

    app.exec_()
    