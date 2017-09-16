class BoxFunction(object):

    def __init__(self, name, ftype, box, dictionary={}):

        self.name = name
        self.type = ftype
        self.box = box
        self.dictionary = dictionary

        if self.type == "position":
            if 'image' not in self.dictionary.keys():
                raise ValueError('{} needs to have an image to work properly'.format(self.name))
