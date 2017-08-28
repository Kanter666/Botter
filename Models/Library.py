import os


class Library(object):

    def __init__(self, destination, screen_box, directory, functions):

        self.destination = destination
        self.screen_box = screen_box
        self.directory = directory
        self.functions = functions

    def create_library(self):
        name = os.path.basename(os.path.normpath(self.destination))
        with open(self.destination+".py", 'w') as file:
            if any(function.name == "number" or function.name == "string" for function in self.functions):
                file.write("from PIL import Image\n")
                file.write("import pytesseract\n")
            file.write("from mss import mss\n")
            file.write("\n\n")
            file.write("class {}(object):\n".format(name))
            file.write("\n")
            file.write("    def __init__(self):\n")
            file.write("        self.box = {}\n".format(self.screen_box))
            file.write("        self.img = None\n")
            file.write("\n")
            file.write("    def grab_screen(self):\n")
            if self.screen_box:
                file.write("        img = self.sct.grab(self.box)")
            else:
                file.write("        with mss() as sct:\n")
                file.write("            self.img = sct.shot()\n")
            file.write("        return self.img\n")
            file.write("\n")
            for function in self.functions:
                if function.type == "string":
                    file.write("    def {}(self):\n".format(function.name))
                    file.write("        print (pytesseract.image_to_string(self.img.crop({})))\n".format(function.box))
                    file.write("        return pytesseract.image_to_string(self.img.crop({}))\n".format(function.box))
                    file.write("\n")
            file.write("")
            file.write("")
            file.write("")
            file.write("")

