from PyQt5 import uic, QtWidgets
import sys

class FunctionDialog(QtWidgets.QDialog):
    def __init__(self):
        print("Creating function dialog")
        super(FunctionDialog, self).__init__()
        uic.loadUi('./Design/BoxDialog.ui', self)
        self.show()

    @staticmethod
    def get_function():
        print ("returning name")
        dialog = FunctionDialog()
        result = dialog.exec_()
        return dialog.name_le.text()
