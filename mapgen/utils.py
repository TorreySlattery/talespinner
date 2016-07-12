import random

class Maze(object):
    maze = [[]]

    def __init__(self, **kwargs):
        self.generate(**kwargs)

    def __str__(self):
        _str = ''
        for row in self.maze:
            _str += ''.join(row) + "\n"
        return _str

    def generate(self, **kwargs):
        width = kwargs.get('width', 40)
        height = kwargs.get('height', 20)
        self.maze = [['#' for jj in range(height)] for ii in range(width)]

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
        pass

    def dig(self, direction):
        pass

    def _get_dir(**kwargs):
        exclude = kwargs.get('exclude', [])
        dir = random.choice(list(range(1,5))-exclude)
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

