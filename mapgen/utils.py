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
            _str += ''.join(row) + "\n"
        return _str

    def generate(self, **kwargs):
        self.maze = [[0 for jj in range(self.height)] for ii in range(self.width)]

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

    def can_dig(self, direction):
        # We check 2*x and 2*y because our maze cells also represent walls; without doubling the distance we dig
        # we'd still get a maze, but it'd look much less "mazelike" without a way to mark passages next to one another
        x, y = direction
        cx, cy = self.cursor

        # Check outer boundaries
        if cx+x+x < 0 or self.width-1 < cx+x+x:
           return False
        if cy+y+y < 0 or self.height-1 < cy+y+y:
            return False

        if self.maze[cy + y + y][cx + x + x] == 0: 
            return True
        else:
            return False

    def dig(self, direction):
        pass

    def _get_dir(self, **kwargs):
        exclude = kwargs.get('exclude', [])
        dir = random.choice(list(set(list(range(1,5)))-set(exclude)))
        if dir == 1:
            return (0, 1)
        elif dir == 2:
            return (1, 0)
        elif dir == 3:
            return (0, -1)
        elif dir == 4:
            return (-1, 0)
        else:
            return (0, 0)

