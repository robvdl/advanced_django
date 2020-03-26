def named_model(cls):
    """ Uses `name` attribute for string serialization of object. """

    def __str__(self):
        return self.name

    cls.__str__ = __str__
    return cls
