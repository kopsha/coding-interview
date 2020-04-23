#!/usr/bin/env python3

import timeit
from datetime import datetime
from itertools import combinations, product


def print_stage(text, row_size=80):
    filler = ' ' * (row_size - 4 - len(text))
    print(f'{"*" * row_size}')
    print(f'* {text}{filler} *')
    print(f'{"*" * row_size}')


def neighbours(row, col):
    keyboard = [
        [None, None, None, None, None],
        [None,  '1',  '2',  '3', None],
        [None,  '4',  '5',  '6', None],
        [None,  '7',  '8',  '9', None],
        [None,  '*',  '0',  '#', None],
        [None, None, None, None, None],
    ]

    result = {
        keyboard[row + y][col + x]
        for y, x in [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]
    }

    return result ^ {None}


def pin_variations(pin):
    focus_map = {
        '1': neighbours(1, 1),
        '2': neighbours(1, 2),
        '3': neighbours(1, 3),
        '4': neighbours(2, 1),
        '5': neighbours(2, 2),
        '6': neighbours(2, 3),
        '7': neighbours(3, 1),
        '8': neighbours(3, 2),
        '9': neighbours(3, 3),
        '*': neighbours(4, 1),
        '0': neighbours(4, 2),
        '#': neighbours(4, 3),
    }

    options = (''.join(sorted(focus_map[c])) for c in pin)
    result = [''.join(z) for z in product(*options)]

    return result


def main():
    pin = '13'
    print(f'pin {pin} variations: {pin_variations(pin)}')

    pin = '139'
    print(f'pin {pin} variations: {pin_variations(pin)}')

    pin = '3*'
    print(f'pin {pin} variations: {pin_variations(pin)}')



if __name__ == '__main__':
    duration = timeit.timeit(main, number=1)
    now = datetime.now().strftime('%H:%M:%S')
    print_stage(f'[{now}] Finished in {duration:.2f} seconds.')
