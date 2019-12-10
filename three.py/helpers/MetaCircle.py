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
        if((x_factor+y_factor) == 0):
            return True
        return ((self.r**2)/(x_factor+y_factor) >= 1)

    def get_value_of_point(self,x,y):
        x_factor = (x-self.x)**2
        y_factor = (y-self.y)**2
        if(x_factor + y_factor == 0):
            return 1
        return (self.r**2)/(x_factor+y_factor)

    def translate(self,x,y):
        self.x += x
        self.y += y

    def set_position(self, x, y):
        self.x = x
        self.y = y
