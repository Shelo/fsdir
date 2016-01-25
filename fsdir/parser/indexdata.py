class Index(object):
    def __init__(self, position=0, length=0, type=0):
        self.position = position
        self.length = length
        self.type = type


class IndexData(object):
    def __init__(self, length=0, type_=0, offset_start=0, offset_stop=0):
        self.length = length
        self.type = type_
        self.offset_start = offset_start
        self.offset_stop = offset_stop
