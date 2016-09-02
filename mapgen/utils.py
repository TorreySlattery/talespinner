import random
import sys
from itertools import repeat, count
from collections import OrderedDict
from heapq import heappush, heappop

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

    def get_path_between(self, source, dest):
        """
        Tries to determine whether there is a continuous arrangement of non-blocked spaces connecting two positions
        using an implementation of Dijkstra's algorithm and a min-priority queue.

        Args:
            pos1: the x,y coordinate tuple to start from
            pos2: the x,y coordinate tuple of the destination
        """

        x1, y1 = source
        x2, y2 = dest
        if self.room[y1][x1] < 0 or self.room[y2][x2] < 0: # Can't pathfind if we're starting blocked off
            return False

        def get_neighbors(_pos):
            nearby = []
            _x, _y = _pos

            try:
                # Up
                if self.room[_y+1][_x] > 0:
                    nearby.append(((_x,_y+1), (0,1)))
            except IndexError:
                pass  # pythonic index checking is weird

            try:
                # Down
                if _y-1 >= 0:
                    if self.room[_y-1][_x] > 0:
                        nearby.append(((_x, _y-1), (0,-1)))
            except IndexError:
                pass

            try:
                # Left
                if _x-1 >= 0:
                    if self.room[_y][_x-1] > 0:
                        nearby.append(((_x-1, _y), (-1,0)))
            except IndexError:
                pass

            try:
                # Right
                if self.room[_y][_x+1] > 0:
                    nearby.append(((_x+1, _y), (1,0)))
            except IndexError:
                pass

            # B,A Start
            return nearby

        dist = dict()
        prev = dict()
        unvisited = PriorityQueue()

        for x in range(self.width):
            for y in range(self.height):
                dist[(x,y)] = sys.maxsize
                unvisited.add_task((x,y), priority=sys.maxsize)
        dist[source] = 0

        while unvisited:
            u = unvisited.pop_task()
            if u == dest:
                # Found our destination
                path = []
                last_spot = dest
                while True:
                    path.append(last_spot)
                    try:
                        lx, ly = last_spot
                        dx, dy = prev[last_spot]
                        last_spot = (lx-dx, ly-dy)
                    except KeyError:
                        # We've grabbed all of our path values
                        return dist, path
            elif dist[u] == sys.maxsize:
                # The only remaining nodes aren't connected to the start point.
                return False
            for neighbor, direction in get_neighbors(u):
                alt = dist[u] + 1
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = direction
                    unvisited.add_task(neighbor, priority=alt)

        # If we somehow get here, we've failed. 
        return False

    def dig_path_between(self, pos1, pos2):
        """
        Digs a path between two points in the Room

        Args:
            pos1: the x,y coordinate tuple to start from
            pos2: the x,y coordinate tuple of the destination

        Returns:
            True if it dug a path, False otherwise, which only happens if we tried to access an invalid index
        """

        # Start with an as-the-crow-flies approach: draw a line between pos1 & pos2

        x1,y1 = pos1
        x2,y2 = pos2

        try:
            if x2-x1 == 0:
                top = max(y1, y2)
                bottom = min(y1, y2)
                for y in range(bottom, top+1):
                    self.room[y][x1] = 1
                return True

            m = float(y2-y1)/float(x2-x1)
            left = min(x1, x2)
            right = max(x1, x2)

            y_previous = round(left * m)
            for x in range(left, right+1):
                y = round(x*m)
                self.room[y][x] = 1

                # We need to widen the tunnel when we cut through a diagonal
                if y_previous != y:
                    self.room[y_previous][x] = 1
                y_previous = y

            return True
        except IndexError:
            return False


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
        # Give plenty of room to grow, as we expect to shrinkwrap the finished product
        kwargs['height'] = kwargs.get('height', 200)
        kwargs['width'] = kwargs.get('width', 200)
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

    def __str__(self):
        self.set_shrinkwrapped()
        return super().__str__()

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
        kwargs.setdefault('width', 40)
        kwargs.setdefault('height', 40)
        super().__init__(**kwargs)
        if not kwargs.get('slumber'):
            num_l = kwargs.get('num_l', 1)
            num_m = kwargs.get('num_m', 2)
            num_s = kwargs.get('num_s', 4)
            self.anchor_coords = self.populate(num_l, num_m, num_s)

    def populate(self, num_l, num_m, num_s):
        """
        Takes whatever parameters we come up with and builds an assortment of Rooms

        Args:
            large: a positive integer of how many large rooms to try to place
            medium: a positive integer of how many medium rooms to try to place
            small: a positive integer of how many small rooms to try to place

        Returns:
            A list of anchor coordinates of rooms successfully placed

        """
        room_positions = []
        dimensions = self.width * self.height
        l_area = max(dimensions//6, 1)
        m_area = max(dimensions//12, 1)
        s_area = max(dimensions//24, 1)

        def _place(area):
            c = Cave(min_area=area)
            c.set_shrinkwrapped()
            success = self.place(c.room)
            if success:
                room_positions.append(success)
                return True
            return False

        for _ in repeat(None, num_l):
            _place(l_area)

        for _ in repeat(None, num_m):
            _place(m_area)

        for _ in repeat(None, num_s):
            _place(s_area)


        return room_positions

    def place(self, room, retries=10):
        """
        Takes a 2D list of values and attempts to place it without collisions in the room property

        Args:
            room: a list of lists containing various map values

        Returns:
            x,y tuple of a dug space if the room was placed successfully, False otherwise
        """
        def _place(posx, posy):
            for idx_r, row in enumerate(room):  # I should work on my naming conventions -.-
                for idx_c, col in enumerate(row):
                    if room[idx_r][idx_c] > 0:  # undug spaces might overwrite previous placements, like layering jpgs
                        if self.room[idx_r+posy][idx_c+posx] < 1:
                            self.area += 1
                        self.room[idx_r+posy][idx_c+posx] = room[idx_r][idx_c]

        for _ in range(retries):
            rx = random.randint(0, self.width-1)
            ry = random.randint(0, self.height-1)
            if self.check_available((rx,ry), room):
                _place(rx,ry)
                return (rx,ry)

        # If we couldn't place the room randomly, try a brute force approach
        from_edge = random.randint(0,3)

        if from_edge == 0:  # left
            for yy in range(self.height):
                for xx in range(self.width):
                    if self.check_available((xx, yy), room):
                        _place(xx, yy)
                        return (xx, yy)
        elif from_edge == 1:  # top
            for xx in range(self.width):
                for yy in reversed(range(self.height)):
                    if self.check_available((xx, yy), room):
                        _place(xx, yy)
                        return (xx, yy)
        elif from_edge == 2:  # right
            for xx in reversed(range(self.width)):
                for yy in range(self.height):
                    if self.check_available((xx, yy), room):
                        _place(xx, yy)
                        return (xx, yy)
        else:
            for yy in reversed(range(self.height)):
                for xx in range(self.width):
                    if self.check_available((xx, yy), room):
                        _place(xx, yy)
                        return (xx, yy)

        return False

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

        if not self.area:
            return True

        overlap_points = 0
        for idx_y, row in enumerate(room):
            for idx_x, col in enumerate(row):
                ox = x + idx_x
                oy = y + idx_y
                if room[idx_y][idx_x] > 0: #todo: go back and change others like this so we can use negative values
                    if self.room[oy][ox] > 0:
                        overlap_points += 1

        # The comparison value will need tweaking, but we want some overlap, but not too much if possible.
        if not overlap_points or overlap_points > (self.width * self.height) // 20:
            return False

        return True


class PriorityQueue():
    """
    https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    """
    pq = []
    entry_finder = {}
    REMOVED = '<removed-task>'
    counter = count()

    def add_task(self, task, priority=0):
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task):
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError("pop from an empty priority queue")


