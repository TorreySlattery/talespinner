import random

class Maze(object):
    maze = [[]]

    def __init__(self, **kwargs):
        self.width = kwargs.get('width', 40)
        self.height = kwargs.get('height', 20)

        origin_x = random.randint(0, self.width-1)
        origin_y = random.randint(0, self.height-1)
        self.cursor = (origin_x, origin_y)  # Set a start position

        self.generate(**kwargs)

    def __str__(self):
        _str = ''
        upright = [row for row in reversed(self.maze)]
        for row in upright:
            _str += ''.join(str(x) for x in row) + "\n"
        return _str

    def generate(self, **kwargs):
        self.maze = [[0 for jj in range(self.width)] for ii in range(self.height)]
        x,y = self.cursor
        self.maze[y][x] = 5
        self.dig(self.cursor)

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
            dx,dy = direction

            if x+dx < 0 or self.width <= x+dx:
                continue
            if y+dy < 0 or self.height <= y+dy:
                continue

            if self.maze[y+dy][x+dx]:
                #Diggable cells are zeroes
                continue
            quad = self.get_quad((x+dx, y+dy))
            occupied = False
            for cardinal in quad:
                cx,cy = cardinal
                foo = (dx+cx, dy+cy)
                if quad[cardinal] and foo != (0,0):
                    occupied = True
                    break

            if occupied:
                continue

            # If we make it this far, our expected dig site is clear, so let's excavate and recurse
            self.maze[y+dy][x+dx] = 1  # Sure, what the hell
            self.dig((x+dx, y+dy))

    def get_dirs(self):
        directions = [(1,0), (-1, 0), (0, 1), (0,-1)]
        random.shuffle(directions)
        return directions

    def get_quad(self, point):
        """
        Get the cells N,E,S,W of the given point
        """
        x,y = point

        quad = {
                (0,1): None,
                (1,0): None,
                (0,-1): None,
                (-1,0): None
                }
        try:
            quad[(0,1)] = self.maze[y+1][x] if y < self.height-1 else None
        except IndexError:
            pass

        try:
            quad[(1,0)] = self.maze[y][x+1] if x < self.width else None
        except IndexError:
            pass

        try:
            quad[(0,-1)] = self.maze[y-1][x] if 0 < y else None
        except IndexError:
            pass

        try:
            quad[(-1,0)] = self.maze[y][x-1] if 0 < x else None
        except IndexError:
            pass

        return quad

