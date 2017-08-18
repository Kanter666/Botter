import sys

from os import listdir
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

qtViewFile = "./Design/ScreenMapper.ui"  # Enter file here.

Ui_StartWindow, QtBaseClass = uic.loadUiType(qtViewFile)


class ScreenMapperView(QtWidgets.QMainWindow, Ui_StartWindow):

    clicked_cancel = pyqtSignal()

    def __init__(self):

        self.folder = None

        QtWidgets.QMainWindow.__init__(self)
        Ui_StartWindow.__init__(self)
        self.setupUi(self)

        self.cancel_bt.clicked.connect(self.clicked_cancel.emit)
        self.finish_bt.clicked.connect(self.print_arguments)
        self.screens_cb.currentIndexChanged.connect(self.screen_changed)

        # Image is displayed as a QPixmap in a QGraphicsScene attached to this QGraphicsView.
        self.scene = QtWidgets.QGraphicsScene()
        self.image_view_gv.setScene(self.scene)

    def set_arguments(self, arguments):
        self.folder = arguments[0]
        files = listdir(self.folder)
        self.screens_cb.clear()
        self.screens_cb.addItems(files)
        self.screens_cb.setCurrentIndex(0)

    def screen_changed(self, i):
        image = QImage(self.folder+"/"+self.screens_cb.currentText())
        if type(image) is QPixmap:
            pixmap = image
        elif type(image) is QImage:
            pixmap = QPixmap.fromImage(image)
        else:
            raise RuntimeError("ImageViewer.setImage: Argument must be a QImage or QPixmap.")
        if self.hasImage():
            self._pixmapHandle.setPixmap(pixmap)
        else:
            self._pixmapHandle = self.scene.addPixmap(pixmap)
        self.setSceneRect(QRectF(pixmap.rect()))  # Set scene size to image size.
        self.updateViewer()

    def updateViewer(self):
        if not self.hasImage():
            return
        if len(self.zoomStack) and self.sceneRect().contains(self.zoomStack[-1]):
            self.fitInView(self.zoomStack[-1], Qt.IgnoreAspectRatio)  # Show zoomed rect (ignore aspect ratio).
        else:
            self.zoomStack = []  # Clear the zoom stack (in case we got here because of an invalid zoom).
            self.fitInView(self.sceneRect(), self.aspectRatioMode)  # Show entire image (use current aspect ratio mode).

    def print_arguments(self):
        print(self.text)
