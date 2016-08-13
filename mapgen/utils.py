import random
import sys

from mapgen.models import RoomData

class Room(object):
    room = [[]]

    def __init__(self, **kwargs):
        self.width = kwargs.get('width', 40)
        self.height = kwargs.get('height', 20)
        self.seed = str(kwargs.get('seed', random.randint(0, sys.maxsize)))
        random.seed(self.seed)

        x = random.randint(0, self.width-1)
        y = random.randint(0, self.height-1)
        self.cursor = (x, y)
        self.area = 0

        self.generate(**kwargs)

    def __str__(self):
        _str = ''
        upright = [row for row in reversed(self.room)]
        for row in upright:
            _str += ''.join(str(x).replace('0',u'\u2588').replace('1',' ')\
                                  .replace('5','S') for x in row) + "\n"
        return _str

    def generate(self, **kwargs):
        self.room = [[0 for jj in range(self.width)] for ii in range(self.height)]

    def reset(self):
        self.generate()

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
            quad[(0,1)] = self.room[y+1][x] if y < self.height-1 else None
        except IndexError:
            pass

        try:
            quad[(1,0)] = self.room[y][x+1] if x < self.width else None
        except IndexError:
            pass

        try:
            quad[(0,-1)] = self.room[y-1][x] if 0 < y else None
        except IndexError:
            pass

        try:
            quad[(-1,0)] = self.room[y][x-1] if 0 < x else None
        except IndexError:
            pass

        return quad

    def save(self, description=None):
        room_data = RoomData(description=description,
                             seed=self.seed,
                             area=self.area,
                             width=self.width,
                             height=self.height)

        room_data.save()
        return room_data


class Maze(Room):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.area = 1

    def generate(self, **kwargs):
        self.room = [[0 for jj in range(self.width)] for ii in range(self.height)]

        x,y = self.cursor
        self.room[y][x] = 5
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

            if self.room[y+dy][x+dx]:
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
            self.room[y+dy][x+dx] = 1  # Sure, what the hell
            self.area += 1
            self.dig((x+dx, y+dy))

    def get_dirs(self):
        directions = [(1,0), (-1, 0), (0, 1), (0,-1)]
        random.shuffle(directions)
        return directions

class Cave(Room):
    """
    Represents a room with staggered walls and possibly internal structures
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        x,y = self.width//2, self.height//2
        self.room[y][x] = 1
        self.area = 1  # tracking the number of dug-out spaces
        self.min_area = kwargs.get('min_area', (self.width*self.height)//3)
        if self.width * self.height < self.min_area:
            print("Min area was set too high for the size of the Room.")
            self.min_area = (self.width * self.height) - 1
        start = (x,y)
        self.dig(start, **kwargs)

        best_map = (self.room, self.area)
        for regrow in range(10):
            if self.area < self.min_area:
                self.reset(start)
                self.dig(start, **kwargs)
                if best_map[1] < self.area:
                    # We have a new winner
                    best_map = (self.room, self.area)
            else:
                break
        self.room, self.area = best_map
        print("Total area:{}".format(self.area))

    def reset(self, start):
        super().reset()
        x,y = start
        self.room[y][x] = 1
        self.area = 1

    def dig(self, start, **kwargs):
        lifespan = kwargs.get('lifespan', 555550)
        cells = [start]

        while lifespan > 0 and cells and self.area < self.min_area:
            _cells = []
            for cell in cells:
                quad = self.get_quad(cell)
                for direction in quad:
                    if quad[direction] == 0:
                        dug = random.randint(1,2) % 2
                        if dug:
                            dx,dy = direction
                            cx,cy = cell
                            self.room[cy+dy][cx+dx] = dug
                            self.area += 1
                            _cells.append((cx+dx, cy+dy))

            cells = _cells
            lifespan -= 1

