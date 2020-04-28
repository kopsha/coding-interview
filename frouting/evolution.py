#!/usr/bin/env python3

import timeit
from datetime import datetime

import csv
import copy
import math
import matplotlib.pyplot as plt

from collections import deque
from collections import defaultdict
from collections import namedtuple
from random import shuffle
from operator import mul
from functools import reduce
import math

import statistics


def print_stage(text, row_size=80):
    filler = ' ' * (row_size - 4 - len(text))
    print(f'{"*" * row_size}')
    print(f'* {text}{filler} *')
    print(f'{"*" * row_size}')


def mystr(x):
    if type(x) is list:
        x = str(x)
    return '  .' if x == None else f'{x:>3}'


def print_array(a):
    for row in a:
        print(' '.join(list(map(mystr, row))))

####

def boxed_labels(layout, node):
    data, rows, cols = layout
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

def crossed_labels(layout, node):
    data, rows, cols = layout
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


def crossed_nodes(layout, node):
    data, rows, cols = layout
    r,c = node
    nb = [
        (i,j)
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
            if type(value) is not int:
                raise TypeError(f'Data is {type(value)}')
            if value > 0:
                result.add(value)
    return result


fig_counter = 0
def save_figure(layout):
    global fig_counter
    fig_counter += 1
    data, rows, cols = layout
    fig, ax0 = plt.subplots(1)
    ax0.matshow(data)
    fig.savefig(f'solutions/evo_data_{fig_counter:>03}.png')
    plt.close()

def scan_target_nodes(layout, targets):
    data, rows, cols = layout
    nodes = defaultdict(list)

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            node = (i, j)
            if value in targets:
                nodes[value].append(node)

    return nodes

def inflate_step(layout, target_nodes):
    data, rows, cols = layout
    mdata = copy.deepcopy(data)
    dirty_flag = False

    updates = defaultdict(list)

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            node = (i, j)
            if value == 0:  ## open space
                nbs = [l for l in crossed_labels(layout, node) if l > 0]
                nearbys = set(nbs)
                if len(nearbys) == 1 and len(nbs) == 1:
                    updates[node].append(nearbys.pop())

    for node, lvalue in updates.items():
        i, j = node
        if len(lvalue) != 1:
            print('more updates: ', lvalue)
        value = lvalue[0]

        cn = crossed_nodes(layout, node)
        for cnode in cn:
            if cnode in updates:
                mdata[i][j] = WALL_MARK
            else:
                mdata[i][j] = value

    return (mdata, rows, cols), bool(updates)


def alternator(left, right):
    count = 0
    while True:
        yield left if count % 2 == 0 else right
        count += 1


def distance(left, right):
    left_row, left_col = left
    right_row, right_col = right
    dist = ((right_row - left_row) ** 2 + (right_col - left_col) ** 2)
    return int(dist)


def nearest_target(node, target_nodes):
    assert len(target_nodes) > 0

    distances = []
    for tk, tnodes in target_nodes.items():
        dd = [ distance(node, tnode) for tnode in tnodes ]
        dd.sort()
        middle = int(float(len(dd)) / 1.6180339887498948482)
        dd = dd[:middle+1]
        distances.append( (tk, reduce(mul, dd, 1)) )

    distances.sort(key=lambda pair: pair[1])

    value, dist = distances[0]
    return value, dist

def grab_same_nodes(layout, value):
    data, rows, cols = layout

    nodes = []

    for i, row in enumerate(data):
        for j, v in enumerate(row):
            node = (i, j)
            if v == value:
                nodes.append(node)

    return nodes

def group_nodes_in_regions(layout, nodes):
    region_id = 0
    regions = defaultdict(list)
    remaining_nodes = deque(nodes)
    queue = deque()

    while len(remaining_nodes):
        node = remaining_nodes.popleft()
        visited = set()
        queue.append(node)
        while len(queue):
            vnode = queue.popleft()
            visited.add(vnode)

            nbs = [n for n in crossed_nodes(layout, vnode) if n in remaining_nodes and n not in visited and n not in queue]
            queue.extend(nbs)

        regions[region_id].extend(list(visited))
        region_id += 1
        remaining_nodes = deque(set(remaining_nodes) - visited)

    return regions




def search_solution(layout, target, target_nodes):
    import pathfinding

    def get_left_node(data, node, target):
        i, j = node
        j -= 1
        return (i, j) if (j >= 0) and (data[i][j] == target) else None

    def get_top_node(data, node, target):
        i, j = node
        i -= 1
        return (i, j) if (i >= 0) and (data[i][j] == target) else None

    mdata, rows, cols = layout

    # assume target zone is connected
    vertices = []
    edges = []
    for i, row in enumerate(mdata):
        for j, value in enumerate(row):
            node = (i, j)
            if value == target:
                vertices.append(node)
                left_node = get_left_node(mdata, node, target)
                if left_node is not None:
                    edges.append( (left_node, node, 1) )
                top_node = get_top_node(mdata, node, target)
                if top_node is not None:
                    edges.append( (top_node, node, 1) )


    g = pathfinding.GraphUndirectedWeighted( len(vertices) )
    for edge in edges:
        left, right, dist = edge
        g.add_edge( vertices.index(left), vertices.index(right), dist )
        g.add_edge( vertices.index(right), vertices.index(left), dist )

    t_nodes = target_nodes[target]
    for left, right in zip(t_nodes[:-1], t_nodes[1:]):    
        path, distance = pathfinding.dijkstra(g, vertices.index(left), vertices.index(right))
        if distance == float('inf'):
            print('no route found for target', target, ', nodes', left, right)
        else:
            for ndx, node in enumerate(vertices):
                i, j = node
                if ndx in path:
                    mdata[i][j] = target
                else:
                    mdata[i][j] = 0

    return mdata


def evolve(layout, target_nodes):
    data, rows, cols = layout

    updates = defaultdict(list)

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            node = (i, j)
            if value == 0:
                nt_val, dist = nearest_target(node, target_nodes)
                nbs = set(boxed_labels(layout, node)) - {0, TEMP_WALL_MARK, WALL_MARK}
                if len(nbs) > 1:
                    updates[node].append( TEMP_WALL_MARK )
                else:
                    updates[node].append( nt_val )


    # perform updates
    mdata = copy.deepcopy(data)
    for node, update in updates.items():
        i, j = node
        mdata[i][j] = update.pop()


    for target in [1, 2, 3, 4, 5]:
        mlayout = (mdata, rows, cols)
        mdata = search_solution(mlayout, target, target_nodes)


    for i, row in enumerate(mdata):
        for j, value in enumerate(row):
            node = (i, j)
            if value == TEMP_WALL_MARK:
                mdata[i][j] = 0

    return mdata

def evolve_back(layout, target_nodes):
    data, rows, cols = layout

    updates = defaultdict(list)

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            node = (i, j)
            if value == 0:
                nt_val, dist = nearest_target(node, target_nodes)
                updates[node].append( nt_val )

    # perform updates
    mdata = copy.deepcopy(data)
    for node, update in updates.items():
        i, j = node
        mdata[i][j] = update.pop()

    return mdata


WALL_MARK = -1
TEMP_WALL_MARK = -2

def main():

    data_files = [
        'step_one.csv',
#        'step_one_solved.csv',
        'step_two.csv',
#        'step_two_solved.csv',
#        'step_three.csv',
    ]

    for filename in data_files:
        print_stage(filename)
        data = []
        with open(filename, newline='') as csvfile:
            content = csv.reader(csvfile, delimiter=',')
            for row in content:
                row_data = list(map(lambda x: WALL_MARK if x == 'Z' else int(x), row))
                data.append( row_data )

        pair_filename = filename.replace('.csv', '_solved.csv')
        solved_data = []
        with open(pair_filename, newline='') as csvfile:
            content = csv.reader(csvfile, delimiter=',')
            for row in content:
                row_data = list(map(lambda x: WALL_MARK if x == 'Z' else int(x), row))
                solved_data.append( row_data )

        original_data = copy.deepcopy(data)
        rows = len(original_data)
        assert rows > 1
        cols = len(original_data[0])
        assert cols > 1
        print(f'shape: {rows} x {cols}')

        layout = (data, rows, cols)
        targets = scan_target_set(data)
        target_nodes = scan_target_nodes(layout, targets)

        data = evolve(layout, target_nodes)

        fig, (ax0, ax1) = plt.subplots(1, 2)
        ax0.matshow(data)
        ax1.matshow(solved_data)
        fig.savefig(f'solutions/evo_{filename.rstrip(".csv")}.png')


if __name__ == '__main__':
    duration = timeit.timeit(main, number=1)
    now = datetime.now().strftime('%H:%M:%S')
    print_stage(f'[{now}] Finished in {duration:.2f} seconds.')
