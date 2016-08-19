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

    def get_shrinkwrapped(self):
        """
        Culls as much of self.room as possible, down to only above-0 values at its edges.
        """
        reduced_map = []

        least_x, least_y = self.width, self.height
        greatest_x, greatest_y = 0,0

        for idx_r, row in enumerate(self.room):
            for idx_c, col in enumerate(row):
                if self.room[idx_r][idx_c] > 0:
                    if idx_c < least_x:
                        least_x = idx_c
                    if idx_r < least_y:
                        least_y = idx_r

                    if idx_c > greatest_x:
                        greatest_x = idx_c
                    if idx_r > greatest_y:
                        greatest_y = idx_r

        return [row[least_x:greatest_x+1] for row in self.room[least_y:greatest_y+1]]

    def set_shrinkwrapped(self):
        """
        Shrinkwraps the current Cave
        """
        self.room = self.get_shrinkwrapped()
        self.height = len(self.room)
        self.width = len(self.room[0])

class Map(Room):
    """
    Represents a collection of Rooms and how they're oriented spatially in
    regards to one another, e.g. the first level of a dungeon or temple would
    be a Map.
    """

    def __init__(self, **kwargs):
        kwargs['width'] = kwargs.get('width', 140)
        kwargs['height'] = kwargs.get('height', 30)
        super().__init__(**kwargs)
        self.populate(**kwargs)

    def populate(self, retries=10, **kwargs):
        """
        Takes whatever parameters we come up with and builds an assortment of related Rooms, creating a map or dungeon
        level.

        Args:

        """
        room_positions = []

        c = Cave(**kwargs)
        room = c.room
        for _ in range(retries):
            success = self.place(room)
            if success:
                room_positions.append(success)
                break

    def place(self, room):
        """
        Takes a 2D list of values and attempts to place it without collisions in the room property 

        Args:
            room: a list of lists containing various map values

        Returns:
            True if the room was placed successfully, False otherwise
        """
        pass

    def check_available(self, position, room):
        """
        Checks if a smaller Room can be placed at the given position. For the current iteration, undug (0-value) Room
        values still count for boundary detection. That is, if room is 40x40, even if it only has one spot dug out, it
        will be checked as if it's 40x40. This behavior may change, but I need a starting point

        Args:
            position: a tuple containing the x,y indices of the room property to begin at
            room: a list of lists containing various map values

        Returns:
            True if the room can be placed at position, False if not.
        """
        rw = len(room[0])
        rh = len(room)
        x,y = position

        # If room would have edges outside of Map, we can skip everything else
        if x + rw > self.width or y + rh > self.height:
            return False

        for idx_y, row in enumerate(room):
            for idx_x, col in enumerate(row):
                ox = x + idx_x
                oy = y + idx_y
                if room[idx_y][idx_x] > 0: #todo: go back and change others like this so we can use negative values
                    if self.room[oy][ox] > 0:
                        return False

        return True

