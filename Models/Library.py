import os

from Models.BoxFunction import BoxFunction


class Library(object):

    def __init__(self, destination, screen_box, directory, functions):

        self.destination = destination
        self.screen_box = screen_box
        self.directory = directory
        self.functions = functions

    @staticmethod
    def create_library(destination, screen_box, directory, functions):
        name = os.path.basename(os.path.normpath(destination))
        with open(destination+".py", 'w') as file:
            if any(function.type == "number" or function.type == "string" for function in functions):
                file.write("from PIL import Image\n")
                file.write("import pytesseract\n")
            file.write("from mss import mss\n")
            file.write("\n\n")
            file.write("class {}(object):\n".format(name))
            file.write("# screen_box = {}\n".format(screen_box))
            file.write("# directory = {}\n".format(directory))
            file.write("\n")
            file.write("    def __init__(self):\n")
            file.write("        self.img = None\n")
            file.write("\n")
            file.write("    def grab_screen(self):\n")
            file.write("        with mss() as sct:\n")
            if screen_box:
                file.write("            img = sct.grab({})\n".format(screen_box))
            else:
                file.write("            img = sct.shot()\n")
            file.write("        self.img = Image.frombytes('RGB', img.size, img.rgb)\n")
            file.write("        return self.img\n")
            file.write("\n")
            for function in functions:
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

    @staticmethod
    def load_library(destination):
        directory = None
        functions = []
        with open(destination, 'r') as file:
            lines = file.readlines()
            i = 3
            while i < len(lines):
                print("line number {} has this text: {}".format(i, lines[i]))

                splitline = lines[i].split()
                if len(splitline) < 2:
                    i += 1
                    continue
                if splitline[0] == "#" and splitline[1] == "directory":
                    directory = splitline[3]
                    i += 8
                    print("Directory is {} . and we increased curent line to {}".format(directory, i))
                elif len(splitline[1]) > 7 and splitline[1][-7:] == "(self):" \
                    and splitline[1][:-7] != "grab_screen":
                    function_name = splitline[1][:-7]
                    crop = lines[(i+1)][33:][:-3]
                    crop = crop.split(",")
                    print("Current function: {} \ncrop after splitting: {}".format(function_name, crop))
                    function_box = [int(crop[0]), int(crop[1]), (int(crop[2])-int(crop[0])), (int(crop[3])-int(crop[1]))]
                    print("Calculated box = {}".format(function_box))
                    returnline = lines[(i+2)].split()
                    if returnline[1] == "pytesseract.image_to_string(cropped)":
                        function_type = "string"
                    elif returnline[1] == "float(pytesseract.image_to_string(cropped))":
                        function_type = "number"
                    print("this function is type of {} \n".format(function_type))
                    function = BoxFunction(function_name, function_type, function_box)
                    functions.append(function)
                    i += 2
                i += 1

        return directory, functions



