class BoxFunction(object):

    def __init__(self, name, ftype, box, image=None, threshold=None):

        self.name = name
        self.type = ftype
        self.box = box
        self.image = image
        self.threshold = threshold

        if self.type == "position":
            if not image:
                raise ValueError('{} needs to have an image to work properly'.format(self.name))
