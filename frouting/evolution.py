#!/usr/bin/env python3

import timeit
from datetime import datetime

import csv
import copy
import math
import matplotlib.pyplot as plt

import queue  
from collections import defaultdict
from collections import namedtuple
from random import shuffle


def print_stage(text, row_size=80):
    filler = ' ' * (row_size - 4 - len(text))
    print(f'{"*" * row_size}')
    print(f'* {text}{filler} *')
    print(f'{"*" * row_size}')


def mystr(x):
    return '  .' if x == None else f'{x:>3}'


def print_array(a):
    for row in a:
        print(' '.join(list(map(mystr, row))))

####

def boxed_labels(data, node):
    rows = len(data)
    cols = len(data[0])
    r,c = node
    nb = [
        data[i][j]
        for i,j in [
            (r-1, c-1), (r-1, c  ), (r-1, c+1),
            (r  , c-1),             (r  , c+1),
            (r+1, c-1), (r+1, c  ), (r+1, c+1),
        ]
        if (0 <= i < rows) and (0 <= j < cols)
    ]
    return nb

def crossed_labels(data, node):
    rows = len(data)
    cols = len(data[0])
    r,c = node
    nb = [
        data[i][j]
        for i,j in [
            (r-1, c), (r, c-1),
            (r+1, c), (r, c+1),
        ]
        if (0 <= i < rows) and (0 <= j < cols)
    ]
    return nb

def scan_target_set(data):
    result = set()
    for rows in data:
        for value in rows:
            if value > 0:
                result.add(value)
    return result

WALL_MARK = -1

def main():

    data_files = [
        'step_one.csv',
        'step_one_solved.csv',
        'step_two.csv',
        'step_two_solved.csv',
        'step_three.csv',
    ]

    for filename in data_files:
        print_stage(filename)
        data = []
        with open(filename, newline='') as csvfile:
            content = csv.reader(csvfile, delimiter=',')
            for row in content:
                data.append( list(map(lambda x: WALL_MARK if x == 'Z' else int(x), row)) )

        original_data = copy.deepcopy(data)
        rows = len(original_data)
        assert rows > 1
        cols = len(original_data[0])
        assert cols > 1
        print(f'shape: {rows} x {cols}')

        targets = list(scan_target_set(original_data))

        fig, (ax0, ax1) = plt.subplots(1, 2)
        ax0.matshow(original_data)
        ax1.matshow(data)
        fig.savefig(f'solutions/evo_{filename.rstrip(".csv")}.png')


if __name__ == '__main__':
    duration = timeit.timeit(main, number=1)
    now = datetime.now().strftime('%H:%M:%S')
    print_stage(f'[{now}] Finished in {duration:.2f} seconds.')
