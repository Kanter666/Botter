from PyQt5 import uic, QtWidgets
from Models.BoxFunction import BoxFunction
import sys

class FunctionDialog(QtWidgets.QDialog):
    def __init__(self):
        super(FunctionDialog, self).__init__()
        uic.loadUi('./Design/BoxDialog.ui', self)
        self.show()

    @staticmethod
    def get_function(box):
        print ("returning name")
        dialog = FunctionDialog()
        result = dialog.exec_()
        return dialog.name_le.text()

    def get_radio_button_clicked(self):
        return self.function_type.checkedButton().text()
