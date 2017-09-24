import os
import ast

from Models.BoxFunction import BoxFunction


class Library(object):

    def __init__(self, destination, screen_box, directory, functions, dict):

        self.destination = destination
        self.screen_box = screen_box
        self.directory = directory
        self.functions = functions
        self.dict = dict

    @staticmethod
    def create_library(destination, screen_box, directory, functions, dict):
        name = os.path.basename(os.path.normpath(destination))[:-3].replace(" ", "_")
        destination = destination[:-(len(name)+3)]+name+".py"
        with open(destination, 'w') as file:
            file.write("import random\n"
                       "import numpy\n"
                       "import cv2\n"
                       "import pyautogui\n"
                       "import pyocr\n"
                       "import pyocr.builders\n"
                       "from PIL import Image, ImageFilter\n"
                       "from mss import mss\n")
            file.write("\n\n")
            file.write("""class {}(object):\n"""
                       """# c {{'screen_box': {}, 'directory': '{}', 'dict': {}}}\n"""
                       """\n"""
                       """    def __init__(self):\n"""
                       """        self.img = None\n"""
                       """        tools = pyocr.get_available_tools()\n"""
                       """        if len(tools) == 0:\n"""
                       """            print('No OCR tool found')\n"""
                       """            sys.exit(1)\n"""
                       """        self.tool = tools[0]\n"""
                       """        self.screen_box = {}\n"""
                       """        print("Will use tool '%s'" % (self.tool.get_name()))\n""".format(
                name, screen_box, directory, dict, screen_box
            ))
            for function in functions:
                if function.type == "change":
                    file.write("        self.grab_screen()\n"
                               "        self.{}_img = self.img.crop([{}, {}, {}, {}])\n".format
                    (
                        function.name, int(function.box[0]), int(function.box[1]),
                        int(function.box[0] + function.box[2]), int(function.box[1] + function.box[3])
                    ))
            file.write("\n")
            file.write("    def grab_screen(self):\n"
                       "        with mss() as sct:\n")
            if screen_box:
                file.write("            img = sct.grab(self.screen_box)\n")
            else:
                file.write("            img = sct.grab(sct.monitors[0])\n")
            file.write("        self.img = Image.frombytes('RGB', img.size, img.rgb)\n"
                       "        return self.img\n"
                       "\n")
            file.write("    def grab_file(self, file):\n"
                       "        self.img = Image.open(file)\n"
                       "\n")
            file.write("    def write_text(self, text):\n"
                       "        pyautogui.typewrite(text)\n"
                       "\n")
            file.write("    def press_button(self, text):\n"
                       "        pyautogui.press(text)\n"
                       "\n")
            if "position_image" in dict and dict["position_image"]:
                file.write("    def locate_screen(self):\n"
                           "        image = cv2.imread('{}/Images/position_img.png')\n"
                           "        with mss() as sct:\n"
                           "            screen = sct.grab(sct.monitors[0])\n"
                           "        screen = Image.frombytes('RGB', screen.size, screen.rgb)\n"
                           "        cropped = numpy.array(screen)[:, :, ::-1].copy()\n"
                           "        res = cv2.matchTemplate(cropped, image, cv2.TM_CCOEFF_NORMED)\n"
                           "        loc = numpy.where( res >= 0.8)\n"
                           "        if len(loc[0])>0:\n"
                           "            self.screen_box['left']=loc[0][0]+{}\n"
                           "            self.screen_box['left']=loc[1][0]+{}\n"
                           "\n".format(directory, dict["position_image"][0], dict["position_image"][1]))

            for function in functions:
                file.write("    def {}(self):\n"
                           "# f BoxFunction('{}', '{}', {}, {})\n".format(
                    function.name,
                    function.name, function.type, function.box, function.dictionary
                )
                )
                if function.type == "click":
                    file.write(
                        """        pyautogui.click({}, {})\n""".format((int(screen_box["left"] + function.box[0] + function.box[2] / 2)),
                                                                       int(screen_box["top"] + function.box[1] + function.box[3] / 2)))
                elif function.type == "game_box":
                    file.write("""        return {}\n""".format(function.box))
                else:
                    file.write("        cropped = self.img.crop([{}, {}, {}, {}])\n".format
                    (
                        int(function.box[0]), int(function.box[1]), int(function.box[0] + function.box[2]),
                        int(function.box[1] + function.box[3])
                    )
                    )
                    if "threshold" in function.dictionary.keys() and function.dictionary["threshold"]:
                        file.write("        im = cropped.filter(ImageFilter.EDGE_ENHANCE_MORE)\n"
                                   "        npcropped = numpy.array(im)[:, :, ::-1].copy()\n"
                                   "        npcropped = cv2.resize(npcropped, (0,0), fx=3, fy=3)\n"
                                   "        im = Image.fromarray(npcropped)\n"
                                   "        im = im.convert('L')\n"
                                   "        cropped = im.point(lambda x: 0 if x<{} else 255, '1')\n".format(function.dictionary["threshold"]))
                    if function.type == "string":
                        file.write("""        return self.tool.image_to_string(cropped, lang="eng", builder=pyocr.builders.TextBuilder())\n""")
                    elif function.type == "number":
                        file.write("""        return float(self.tool.image_to_string(cropped, lang="eng", builder=pyocr.builders.DigitBuilder()))\n""")
                    elif function.type == "position":
                        file.write("        image = cv2.imread('{}')\n"
                                   "        cropped = numpy.array(cropped)[:, :, ::-1].copy()\n"
                                   "        res = cv2.matchTemplate(cropped, image, cv2.TM_CCOEFF_NORMED)\n"
                                   "        threshold = 0.{}\n"
                                   "        loc = numpy.where( res >= threshold)\n".format(
                            function.dictionary["image"], function.dictionary["match_threshold"]
                            )
                        )
                        if "rotate" in function.dictionary and function.dictionary["rotate"]:
                            file.write("        for angle in [90, 180, 270]:\n"
                                       "            if len(loc[0])>0:\n"
                                       "                break\n"
                                       "            image = numpy.rot90(image)\n"
                                       "            res = cv2.matchTemplate(cropped, image, cv2.TM_CCOEFF_NORMED)\n"
                                       "            threshold = 0.{}\n"
                                       "            loc = numpy.where( res >= threshold)\n".format(
                                function.dictionary["match_threshold"]
                            )
                            )
                        file.write("        return loc\n\n")
                    elif function.type == "change":
                        file.write("        if self.{}_img == cropped:\n"
                                   "            return False\n"
                                   "        else:\n"
                                   "            self.{}_img = cropped\n"
                                   "            return True\n".format(function.name, function.name))
                file.write("\n")

            file.write("\n")

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

                if len(lines[i])<4:
                    i += 1
                    continue
                else:
                    if lines[i][:3] == "# c":
                        class_data = ast.literal_eval(lines[i][4:])
                        directory = class_data["directory"]
                        dictionary = class_data["dict"]
                        print("Directory is {} . and we increased curent line to {}".format(directory, i))
                        i += 8
                    elif lines[i][:3] == "# f":
                        functions.append(eval(lines[i][4:]))
                        i += 2
                i += 1

        return directory, functions, dictionary




