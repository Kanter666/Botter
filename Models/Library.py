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
            file.write("from mss import mss\n")
            file.write("\n\n")
            file.write("class {}(object):\n".format(name))
            file.write("\n")
            file.write("    def __init__(self):\n")
            file.write("        self.box = {}\n".format(self.screen_box))
            file.write("\n")
            file.write("    def grab_screen(self):\n")
            if self.screen_box:
                file.write("        img = self.sct.grab(self.box)")
            else:
                file.write("        with mss() as sct:\n")
                file.write("            img = sct.shot()\n")
            file.write("        return img\n")
            file.write("")
            file.write("")
            file.write("")
            file.write("")
            file.write("")

