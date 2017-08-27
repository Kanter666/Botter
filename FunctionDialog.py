from Models.BoxFunction import BoxFunction

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog


class FunctionDialog(QtWidgets.QDialog):
    def __init__(self):
        super(FunctionDialog, self).__init__()
        uic.loadUi('./Design/BoxDialog.ui', self)
        self.show()

    @staticmethod
    def get_function(box, folder):
        print ("returning name")
        dialog = FunctionDialog()
        result = dialog.exec_()
        text = dialog.get_radio_button()
        box_function = None
        if text == "Is image in box?(bool)" or text =="Get position of image(x,y)":
            image, _ = QFileDialog.getOpenFileName(
                dialog,
                "Select file of image that you want to map",
                folder+"/Images",
                "Image Files (*.png)"
            )
            print("returning: "+text+ "  with image: "+image)
            if text == "Is image in box?(bool)":
                box_function = BoxFunction(dialog.name_le.text(), "is_there", box, image=image)
            else:
                box_function = BoxFunction(dialog.name_le.text(), "position", box, image=image)
        elif text == "Get number(float)":
            box_function = BoxFunction(dialog.name_le.text(), "number", box)
        elif text == "Get string(string)":
            box_function = BoxFunction(dialog.name_le.text(), "string", box)
        return box_function

    def get_radio_button(self):
        return self.function_type.checkedButton().text()
