#!/usr/bin/env python3

import timeit
from datetime import datetime

import csv
import copy
import math
import matplotlib.pyplot as plt

from collections import defaultdict

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


def flatten(array):
    result = []
    for x in array:
        if type(x) == list:
            result.extend( flatten(x) )
        else:
            result.append(x)
    return result

def split_connected(data):

    def connected_spaces(of):
        i,j = of
        label = data[i][j]
        spaces = [
            (r, c)
            for r, c in [
                (i, j-1), (i-1, j),
                (i, j+1), (i+1, j),
            ]
            if (0 <= r < rows) and (0 <= c < cols) \
                and  data[r][c] == 0
        ]
        return spaces

    def neighbours(of):
        r,c = of
        nb = [
            data[i][j]
            for i,j in [(r-1, c),(r+1, c),(r,c-1),(r,c+1),]
            if (0 <= i < rows) and (0 <= j < cols)
        ]
        return nb

    def diagonal_neighbours(of):
        r,c = of
        nb = [
            data[i][j]
            for i,j in [(r-1, c-1),(r-1, c+1),(r+1,c-1),(r+1,c+1),]
            if (0 <= i < rows) and (0 <= j < cols)
        ]
        return nb

    def connected_neighbours(of):
        i,j = of
        label = data[i][j]
        nb = [
            (r, c)
            for r, c in [
                (i, j-1), (i-1, j),
                (i, j+1), (i+1, j),
            ]
            if (0 <= r < rows) and (0 <= c < cols) \
                and  label == data[r][c]
        ]
        return nb

    def inflate_region(region):
        occupy = set()

        print('inflate_region', region)

        for node in region:
            spaces = set(connected_spaces(node))
            expansion_nodes = spaces - region
            occupy |= expansion_nodes

        return occupy


    def collect_connected_regions():
        remaining = {(i // cols, i % cols) for i, val in enumerate(flatten(data))}
        connected_areas = defaultdict(list)

        while remaining:
            node = remaining.pop()
            prospects = set()
            cnb = set(connected_neighbours(node))
            prospects.update(cnb)
            visited = {node}

            while prospects:
                a_node = prospects.pop()
                
                if a_node in visited:
                    continue

                visited.add(a_node)

                cnb = set(connected_neighbours(a_node))
                prospects.update(cnb - visited)

            val = data[node[0]][node[1]]
            connected_areas[val].append(visited)
            remaining -= visited
        return connected_areas


    rows = len(data)
    cols = len(data[0])

    start_connex = collect_connected_regions()
    for label in start_connex:
        if label != 0:
            print(label, 'has -->', start_connex[label])

    updates = []
    spaces = copy.deepcopy(start_connex[0][0])

    blacklist = {0}

    while True:
        updates.clear()
        for node in spaces:
            nearby_labels = neighbours(node)
            dnb = diagonal_neighbours(node)
            pin_labels = [l for l in nearby_labels if l != 0]

            if len(set(pin_labels)) == 1:
                next_label = pin_labels.pop()
                if next_label not in blacklist:
                    d = set(dnb) - {0}
                    if len(d) > 1:
                        continue
                    elif len(d) == 1 and d.pop() != next_label:
                        continue
                    updates.append( (node, next_label) )

        for node, label in updates:

            if label in blacklist:
                continue

            i, j = node
            data[i][j] = label
            spaces.remove(node)

            # if this connection has unified any region then block list it
            connex = collect_connected_regions()
            for label in connex:
                if label == 0:
                    continue

                if len(connex[label]) == 1 and label not in blacklist:
                    print('## ', label, 'was blacklisted.')
                    blacklist.add(label)
                    print(blacklist)
                    # let's trim off the extra

                    trimable = set.union(*connex[label]) - set.union(*start_connex[label])

                    for node in trimable.copy():
                        i,j = node
                        data[i][j] = 0
                        test_connex = collect_connected_regions()
                        if len(test_connex[label]) > 1:
                            trimable.remove(node)
                        data[i][j] = label

                    for node in trimable:
                        i,j = node
                        data[i][j] = 0

        if not updates:
            break

        fig, ax0 = plt.subplots(1)
        ax0.matshow(data)
        plt.show()

    return data


# def grow_worms(data):
#     rows = len(data)
#     cols = len(data[0])
#     flat_data = flatten(data)
#     worms = defaultdict(list)
#     for k in range(0, max(flat_data)+1):
#         worms[k].extend([ (i // cols, i % cols) for i, val in enumerate(flat_data) if val == k])

#     areas = {}

#     for wid, worm in worms.items():
#         nnn = flood_fill(data, wid, worm)
#         areas[wid] = nnn


#     print(areas)
#     print_array(data)

#     return data

def main():

    data = []
    with open('Step_One.csv', newline='') as csvfile:
        content = csv.reader(csvfile, delimiter=',')
        for row in content:
            data.append( list(map(int, row)) )
    # data = [
    #     [0, 0, 1, 0, 0],
    #     [0, 0, 0, 0, 2],
    #     [0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 2],
    #     [0, 0, 1, 0, 0],
    # ]
    

    print_stage('working')
    print_array(data)
    original_data = copy.deepcopy(data)

    traces = split_connected(data)

    fig, (ax0, ax1) = plt.subplots(1, 2)

    ax0.matshow(original_data)
    ax1.matshow(traces)

    plt.show()


if __name__ == '__main__':
    duration = timeit.timeit(main, number=1)
    now = datetime.now().strftime('%H:%M:%S')
    print_stage(f'[{now}] Finished in {duration:.2f} seconds.')
