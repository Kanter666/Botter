import os
import time
import cv2
import _thread
import mss
import mss.tools

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal
from datetime import datetime

qtViewFile = "./Design/Record.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtViewFile)


class CreateView(QtWidgets.QMainWindow, Ui_MainWindow):

    clicked_analyse = pyqtSignal()
    clicked_cancel = pyqtSignal()

    def __init__(self):
        self.box = 0
        self.capture_screen = False
        self.sct = mss.mss()

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.start_rec_bt.clicked.connect(self.onclicked_start)
        self.analyse_rec_bt.clicked.connect(self.onclicked_analyse)
        self.stop_rec_bt.clicked.connect(self.onclicked_stop)
        self.cancel_bt.clicked.connect(self.clicked_cancel.emit)

        self.fullsc_radb.setChecked(True)
        self.fullsc_radb.toggled.connect(self.full_screen_radb)
        self.boxsc_radb.toggled.connect(self.box_screen_radb)

    def onclicked_start(self):
        print("start", self.frequency_spin_box.value())
        self.capture_screen = True
        speed = self.frequency_spin_box.value()
        if speed <= 0:
            speed = 200

        if self.name_lb.text() != "":
            folder_name = self.name_lb.text()
        else:
            folder_name = datetime.now().strftime('%m%d_%H:%M:%S')

        directory = "./" + folder_name
        if not os.path.exists(directory):
            os.makedirs(directory)

        _thread.start_new_thread(self.record_screen, (folder_name, speed))

    def record_screen(self, folder_name, speed):
        counter = 0

        speed = 1./speed

        if isinstance(self.box, int):
            while self.capture_screen:
                self.sct.shot(mon=0, output="./" + folder_name + "/" + str(counter) + ".png")
                time.sleep(speed)
                counter += 1
        else:
            while self.capture_screen:
                sct_img = self.sct.grab(self.box)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output="./" + folder_name + "/" + str(counter) + ".png")
                time.sleep(speed)
                counter += 1
            with open("./" + folder_name + "/box.txt", 'w') as file:
                file.write("{}\n".format(self.box))

        self.number_of_img_l.setText("Number of screenshots: {}".format(counter))

    def onclicked_stop(self):
        self.capture_screen = False
        print("stop")

    def onclicked_analyse(self):
        self.clicked_analyse.emit()

    def full_screen_radb(self):
        if self.fullsc_radb.isChecked():
            self.box = 0
            self.screen_mode.setText("Current mode: Full screen")

    def box_screen_radb(self):
        if self.boxsc_radb.isChecked():
            self.sct.shot(mon=-1, output='./image.png')

            img = cv2.imread('./image.png')

            # Select ROI
            showCrosshair = False
            fromCenter = False
            r = cv2.selectROI("Choose box and press any key", img, fromCenter, showCrosshair)
            self.screen_mode.setText("Current mode: not Full screen")

            print([int(r[0]), int(r[1]), int(r[2]), int(r[3])])  # x, y, width, height
            self.box = {'top': int(r[1]), 'left': int(r[0]), 'width': int(r[2]), 'height': int(r[3])}

            # Crop image
            imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

            # Display cropped image
            cv2.imshow("Press any key to finish", imCrop)
            cv2.waitKey(0)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
