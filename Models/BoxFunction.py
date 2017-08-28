class BoxFunction(object):

    def __init__(self, name, ftype, box, image=None):

        self.name = name
        self.type = ftype
        self.box = box

        if self.type == "position" or self.type == "is_there":
            if image:
                self.image = image
            else:
                raise ValueError('{} needs to have an image to '.format(self.name))

