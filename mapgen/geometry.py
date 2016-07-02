
class Rectangle(object):
    def __init__(self, **kwargs):
        self.x1 = kwargs.get('x1', 0)
        self.x2 = kwargs.get('x2', self.x1+1)
        self.y1 = kwargs.get('y1', 0)
        self.y2 = kwargs.get('y2', self.y1+1)

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    def intersects(self, rect):
        return self.contains((rect.x1, rect.y1)) or \
        self.contains((rect.x1, rect.y2)) or \
        self.contains((rect.x2, rect.y1)) or \
        self.contains((rect.x2, rect.y2)) or \
        rect.contains((self.x1, self.y1)) or \
        rect.contains((self.x1, self.y2)) or \
        rect.contains((self.x2, self.y1)) or \
        rect.contains((self.x2, self.y2))

    def contains(self, vertex):
        x,y = vertex
        return (self.x1 < x < self.x2) and (self.y1 < y < self.y2)

