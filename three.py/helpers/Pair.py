class Pair(object):

    def __init__(self, x, y):
  
        super().__init__()
        self.x = x
        self.y = y

    def toList(self):
        return [self.x, self.y, 0]
