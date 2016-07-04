import random

def get_feat_char(index):
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

def print_list_map(_list):
    for row in _list:
        print(''.join(row))

def generate_maze():
    width = 40
    height = 20
    map = [['#' for jj in range(height)] for ii in range(width)]
    print_list_map(map)
