import random

class Maze(object):
    maze = [[]]

    def __init__(self, **kwargs):
        self.width = kwargs.get('width', 40)
        self.height = kwargs.get('height', 20)

        self.generate(**kwargs)

        origin_x = random.randint(0, self.width)
        origin_y = random.randint(0, self.height)
        self.cursor = (origin_x, origin_y)  # Set a start position

    def __str__(self):
        _str = ''
        for row in self.maze:
            _str += ''.join(str(x) for x in row) + "\n"
        return _str

    def generate(self, **kwargs):
        self.maze = [[0 for jj in range(self.width)] for ii in range(self.height)]

    def get_feat_char(self, index):
        if 0 < index < 10:
            pass
        elif 10 < index < 40:
            pass
        elif 40 < index < 95:
            pass
        elif 95 < index < 100:
            pass
        else:
            return '?'

    def dig(self, curr):
        x,y = curr
        directions = self.get_dirs()
        for direction in directions:
            # Check if we can dig in that direction. If so, change the cell
            # and then move the cursor to this position, then recurse
            pass

    def get_dirs(self):
        directions = [(1,0), (-1, 0), (0, 1), (0,-1)]
        random.shuffle(directions)
        return directions

    def get_quad(self, point):
        """
        Get the cells N,E,S,W of the given point
        """
        x,y = point

        return {
                "N": self.maze[y-1][0] if y!= 0 else None,
                "E": self.maze[y][x+1] if x < self.width-1 else None,
                "S": self.maze[y+1][x] if y < self.height-1 else None,
                "W": self.maze[y][x-1] if x!= 0 else None
               }


