## contains a gridgroup, with some additional functionality for editing the group
class MetaCircle(object):
    def __init__(self, x,y,r):
        super().__init__()
        self.x = x
        self.y = y
        self.r = r


    def inside_circle(self, x, y):
        x_factor = (x-self.x)**2
        y_factor = (y-self.y)**2
        return ((r**2)/(x_factor+y_factor) >= 1)
