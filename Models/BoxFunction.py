class BoxFunction(object):

    def __init__(self, name, ftype, box, image=None):

        self.name = name
        self.type = ftype
        self.box = box
        self.image = image

        if self.type == "position" or self.type == "is_there":
            if not image:
                raise ValueError('{} needs to have an image to work properly'.format(self.name))
