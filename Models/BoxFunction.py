class BoxFunction(object):

    def __init__(self, name, function_type, box, image=None):

        self.name = name
        self.function_type = function_type
        self.box = box

        if self.function_type == "position" or self.function_type == "is_there":
            if image:
                self.image = image
            else:
                raise ValueError('{} needs to have an image to '.format(self.name))

