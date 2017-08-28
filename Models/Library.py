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
            if any(function.type == "number" or function.type == "string" for function in self.functions):
                file.write("from PIL import Image\n")
                file.write("import pytesseract\n")
            file.write("from mss import mss\n")
            file.write("\n\n")
            file.write("class {}(object):\n".format(name))
            file.write("# screen_box = {}\n".format(self.screen_box))
            file.write("\n")
            file.write("    def __init__(self):\n")
            file.write("        self.img = None\n")
            file.write("\n")
            file.write("    def grab_screen(self):\n")
            file.write("        with mss() as sct:\n")
            if self.screen_box:
                file.write("            img = sct.grab({})\n".format(self.screen_box))
            else:
                file.write("            img = sct.shot()\n")
            file.write("        self.img = Image.frombytes('RGB', img.size, img.rgb)\n")
            file.write("        return self.img\n")
            file.write("\n")
            for function in self.functions:
                file.write("    def {}(self):\n".format(function.name))
                file.write(
                    "        cropped = self.img.crop([{}, {}, {}, {}])\n".format(
                        int(function.box[0]),
                        int(function.box[1]),
                        int(function.box[0] + function.box[2]),
                        int(function.box[1] + function.box[3])
                    )
                )
                if function.type == "string":
                    file.write("        return pytesseract.image_to_string(cropped)\n")
                elif function.type == "number":
                    file.write("        return float(pytesseract.image_to_string(cropped))\n")
                file.write("\n")

            file.write("")
            file.write("")
            file.write("")
            file.write("")

