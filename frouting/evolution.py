#!/usr/bin/env python3

from datetime import datetime

import copy
import csv
import math
import math
import random
import statistics
import timeit


from collections import defaultdict
from collections import deque
from collections import namedtuple
from functools import reduce
from operator import mul

import pathfinding

import matplotlib.pyplot as plt


def print_stage(text, row_size=80):
    filler = ' ' * (row_size - 4 - len(text))
    print(f'{"*" * row_size}')
    print(f'* {text}{filler} *')
    print(f'{"*" * row_size}')


def mystr(x):
    return '  .' if x == None else f'{x:3.0f}'

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
            (r-1, c-1), (r-1, c  ), (r-1, c+1),     # top row, left to right
                                    (r  , c+1),     # right node
            (r+1, c+1), (r+1, c  ), (r+1, c-1),     # bottom row, right to left 
            (r  , c-1),                             # left node
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

def boxed_nodes(layout, node):
    data, rows, cols = layout
    r,c = node
    nb = [
        (i,j)
        for i,j in [
            (r-1, c-1), (r-1, c  ), (r-1, c+1),     # top row, left to right
                                    (r  , c+1),     # right node
            (r+1, c+1), (r+1, c  ), (r+1, c-1),     # bottom row, right to left 
            (r  , c-1),                             # left node
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
def save_figure(layout, name_tag=''):
    global fig_counter
    fig_counter += 1
    data, rows, cols = layout
    fig, ax0 = plt.subplots(1)
    ax0.matshow(data)
    fig.savefig(f'solutions/evo_{fig_counter:>03}_{name_tag}.png')
    plt.close()

    # print(f'solutions/evo_{fig_counter:>03}_{name_tag}.png')
    # print_array(data)

    return


def scan_target_nodes(layout, targets):
    data, rows, cols = layout
    nodes = defaultdict(list)

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            node = (i, j)
            if value in targets:
                nodes[value].append(node)

    return nodes


def alternator(left, right):
    count = 0
    while True:
        yield left if count % 2 == 0 else right
        count += 1

def distance(left, right):
    left_row, left_col = left
    right_row, right_col = right
    dist = (right_row - left_row) ** 2 + (right_col - left_col) ** 2
    return dist


def nearest_target(node, target_nodes):
    assert len(target_nodes) > 0

    distances = []
    for tk, tnodes in target_nodes.items():
        dd = [distance(node, tnode) for tnode in tnodes]
        distances.append( (tk, statistics.harmonic_mean(dd)) )

    distances.sort(key=lambda pair: pair[1])

    value, dist = distances[0]
    return value, dist

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


def value_of(layout, node):
    data, rows, cols = layout
    i, j = node
    return data[i][j] if (0 <= i < rows) and (0 <= j < rows) else None


def search_solution(layout, sector_layout, target, target_nodes):
    def connected_left_node(data, node):
        i, j = node
        j -= 1
        return (i, j) if (j >= 0) and (data[i][j] == target or type(data[i][j]) is float) else None

    def connected_top_node(data, node):
        i, j = node
        i -= 1
        return (i, j) if (i >= 0) and (data[i][j] == target or type(data[i][j]) is float) else None

    mdata, rows, cols = layout

    # assume target zone is connected
    vertices = []
    edges = []
    for i, row in enumerate(mdata):
        for j, value in enumerate(row):
            node = (i, j)
            if value == target or type(value) is float:
                vertices.append(node)
                left_node = connected_left_node(mdata, node)
                if left_node in vertices:
                    delta = 1 if value_of(sector_layout, left_node) == value else value
                    edges.append( (left_node, node, delta) )
                    edges.append( (node, left_node, delta) )
                top_node = connected_top_node(mdata, node)
                if top_node in vertices:
                    delta = 1 if value_of(sector_layout, top_node) == value else value
                    edges.append( (top_node, node, value) )
                    edges.append( (node, top_node, value) )

    g = pathfinding.GraphUndirectedWeighted( len(vertices) )
    for edge in edges:
        left, right, dist = edge
        g.add_edge( vertices.index(left), vertices.index(right), dist )

    solution = []
    t_nodes = target_nodes[target]
    for left, right in zip(t_nodes[:-1], t_nodes[1:]):
        #print(f'solving target {target}', 'nodes: ', left, right)
        path, dist = pathfinding.dijkstra(g, vertices.index(left), vertices.index(right))
        if dist == float('inf'):
            #print('\tno route found for target', target, ', nodes', left, right)
            path.clear()

        for ndx in path:
            solution.append( vertices[ndx] )

    return solution, dist


def apply_target_spectrum(layout, target_nodes):
    data, rows, cols = layout
    mdata = copy.deepcopy(data)

    for i, row in enumerate(mdata):
        for j, value in enumerate(row):
            node = (i, j)
            if value == 0:
                nt_val, dist = nearest_target(node, target_nodes)
                mdata[i][j] = nt_val
    return mdata


def apply_dist_spectrum(layout, target_nodes):
    data, rows, cols = layout
    mdata = copy.deepcopy(data)

    max_dist = 0
    for i, row in enumerate(mdata):
        for j, value in enumerate(row):
            node = (i, j)
            if value == 0:
                nt_val, dist = nearest_target(node, target_nodes)
                mdata[i][j] = float(dist)
                max_dist = dist if dist > max_dist else max_dist

    for i, row in enumerate(mdata):
        for j, value in enumerate(row):
            node = (i, j)
            if type(value) is float:
                mdata[i][j] = 1 + (1.0 - value/max_dist) * 100

    return mdata


def apply_marks_for_target(layout, target, target_nodes):
    data, rows, cols = layout
    mdata = copy.deepcopy(data)

    for i, row in enumerate(mdata):
        for j, value in enumerate(row):
            node = (i, j)
            if type(value) is float:
                bl = boxed_labels(layout, node)
                nbs = set(bl)
                for nb in nbs:
                    if type(nb) is int and nb > 0 and nb != target:
                        mdata[i][j] = TEMP_WALL_MARK
                        break

    return mdata


def scan_connected_targets(layout, target_nodes):
    data, rows, cols = layout

    connected_targets = []

    for target in target_nodes:
        t_nodes = target_nodes[target]

        visited = set()
        queue = deque()
        queue.append(t_nodes[0])
        while len(queue):
            vnode = queue.popleft()
            visited.add(vnode)
            nbs = [
                n
                for n in crossed_nodes(layout, vnode)
                if data[n[0]][n[1]] == target and \
                   n not in visited and \
                   n not in queue
            ]
            queue.extend(nbs)

        not_visited_targets = set(t_nodes) - visited
        if len(not_visited_targets) == 0:
            connected_targets.append(target)

    return connected_targets


def mark_solutions(mlayout, solutions):
    mdata, rows, cols = mlayout

    for k in solutions:
        for step in solutions[k]:
            i, j = step
            mdata[i][j] = k

    return mdata


def evolve(layout, target_nodes):
    data, rows, cols = layout

    repeat = True
    solved_targets = set()
    while repeat:
        whaaat = {}
        repeat = False
        mdata = copy.deepcopy(data)
        mlayout = (mdata, rows, cols)
        cost_data = apply_dist_spectrum(mlayout, target_nodes)
        sector_data = apply_target_spectrum(mlayout, target_nodes)

        cost_layout = (cost_data, rows, cols)
        #save_figure(cost_layout, name_tag='cost')

        sector_layout = (sector_data, rows, cols)
        #save_figure(sector_layout, name_tag='sectors')

        for t in target_nodes:
            if t in solved_targets:
                continue
            mdata = copy.deepcopy(cost_data)
            mlayout = (mdata, rows, cols)
            mdata = apply_marks_for_target(mlayout, t, target_nodes)
            #save_figure(mlayout, name_tag=f'marks_for_{t}')

            solution, dist = search_solution(mlayout, sector_layout, t, target_nodes)

            # restore mdata
            mdata = copy.deepcopy(data)
            mlayout = (mdata, rows, cols)

            if solution:
                 whaaat[t] = solution

        # select the shortest solution
        if len(whaaat) > 0:
            sol_paths = [(t,len(x)) for t, x in whaaat.items()]
            sol_paths.sort(key=lambda k: k[1])
            t, sol = random.choice(sol_paths)
            #t, sol = sol_paths[0]
            whaaat = { t: whaaat[t] }
            mdata = mark_solutions(mlayout, whaaat)
        else:
            return mdata, False

        connex = scan_connected_targets(mlayout, target_nodes)
        for t in connex:
            if t not in solved_targets:
                solved_targets.add(t)
                open_targets = set(target_nodes.keys()) - solved_targets
                repeat = len(open_targets) > 0

                print(f'new pad solved {t} only {len(open_targets)} remaining.')
                save_figure(mlayout, name_tag=f'new_pad')

                if repeat:
                    target_nodes = {k:target_nodes[k].copy() for k in open_targets}
                
                    data = copy.deepcopy(mdata)
                    layout = (data, rows, cols)

    return mdata, len(whaaat.keys()) == len(target_nodes.keys())



def evolve_two(layout, target_nodes):
    data, rows, cols = layout

    solved_targets = set()
    open_targets = set(target_nodes.keys()) - solved_targets

    mdata = copy.deepcopy(data)
    mlayout = (mdata, rows, cols)

    while open_targets:
        cost_data = apply_dist_spectrum(mlayout, target_nodes)
        sector_data = apply_target_spectrum(mlayout, target_nodes)
        cost_layout = (cost_data, rows, cols)
        sector_layout = (sector_data, rows, cols)

        solutions = defaultdict(list)
        distances = defaultdict(float)
        for t in open_targets:
            masked_data = apply_marks_for_target(cost_layout, t, target_nodes)
            masked_layout = (masked_data, rows, cols)
            #save_figure(masked_layout, name_tag=f'masks-{t}')
            
            path, dist = search_solution(masked_layout, sector_layout, t, target_nodes)
            if path:
                solutions[t].extend(path)
                distances[t] += dist

        # should compute path colisions
        all_paths = defaultdict(set)
        for t, path in solutions.items():
            all_paths[t].update(path)

        all_t = set(all_paths.keys())
        collisions = defaultdict(int)
        for t in all_paths.keys():
            all_others = all_t - {t}
            for other in all_others:
                collisions[t] += len(all_paths[t] & all_paths[other])
            distances[t] *= collisions[t]

        t, d = sorted(distances.items(), key=lambda k: k[1])[0]
        print(f'selected path {t} which has {d} distance and {collisions[t]} collisions.')
        mdata = mark_path(mlayout, solutions[t], t)
        mlayout = (mdata, rows, cols)
        save_figure(mlayout, name_tag=f'increment')
        solved_targets.add(t)
            
        open_targets = set(target_nodes.keys()) - solved_targets
        if open_targets: print('repeating for ', open_targets)


    return mdata


def mark_path(mlayout, path, value):
    mdata, rows, cols = mlayout

    for step in path:
        i, j = step
        mdata[i][j] = value

    return mdata


def optimize_connected_target(layout, target, target_nodes):
    data, rows, cols = layout

    cost_data = apply_dist_spectrum(layout, target_nodes)
    sector_data = apply_target_spectrum(layout, target_nodes)

    cost_layout = (cost_data, rows, cols)
    #save_figure(cost_layout, name_tag=f'cost-{target}')

    sector_layout = (sector_data, rows, cols)
    #save_figure(sector_layout, name_tag=f'sectors-{target}')

    mdata = copy.deepcopy(cost_data)
    mlayout = (mdata, rows, cols)
    mdata = apply_marks_for_target(mlayout, target, target_nodes)
    #save_figure(mlayout, name_tag=f'marks-{target}')

    mlayout = (mdata, rows, cols)
    solution, dist = search_solution(mlayout, sector_layout, target, target_nodes)

    # restore mdata
    mdata = copy.deepcopy(data)
    mlayout = (mdata, rows, cols)

    if solution:
        #print(solution)
        mdata = mark_path(mlayout, solution, target)

        # clear all inflated nodes
        for i, row in enumerate(mdata):
            for j, value in enumerate(row):
                node = (i, j)
                if value == target and node not in solution:
                    mdata[i][j] = 0
                elif value == TEMP_WALL_MARK:
                    mdata[i][j] = 0

    return mdata


def alt_inflate_regions(layout, open_targets, sector_data):
    data, rows, cols = layout
    sector_layout = (sector_data, rows, cols)
    mdata = copy.deepcopy(data)
    updates = defaultdict(list)

    for i, row in enumerate(data):
        for j, value in enumerate(row):
            node = (i, j)
            if value == 0:
                all_neighbours = boxed_labels(layout, node)
                target_nbs = set(all_neighbours) & open_targets
                other_nbs = set(all_neighbours) - {0, TEMP_WALL_MARK, WALL_MARK} - open_targets

                if len(target_nbs) == 1 and len(other_nbs) == 0:
                    value = target_nbs.pop()
                    updates[node].append(value)

    for node, values in updates.items():
        i, j = node
        if len(values) == 1:
            mdata[i][j] = values.pop()

    return mdata, bool(updates)

def mix_with_costs(layout, target_nodes):
    data, rows, cols = layout

    cost_data = apply_dist_spectrum(layout, target_nodes)
    # cost_layout = (cost_data, rows, cols)
    # save_figure(cost_layout, name_tag=f'cost')

    mdata = copy.deepcopy(data)
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            if value == 0:
                mdata[i][j] = cost_data[i][j]

    return mdata


def mix_with_sectors(layout, target_nodes):
    data, rows, cols = layout

    sector_data = apply_target_spectrum(layout, target_nodes)
    #sector_layout = (sector_data, rows, cols)
    #save_figure(sector_layout, name_tag=f'sector')

    mdata = copy.deepcopy(data)
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            if value == 0:
                mdata[i][j] = sector_data[i][j]

    return mdata


def find_constrained_nodes(layout, target_nodes):
    data, rows, cols = layout

    mdata = copy.deepcopy(data)
    dirty = True
    ss = 0

    # cost_data = apply_dist_spectrum(layout, target_nodes)
    # cost_layout = (cost_data, rows, cols)
    # save_figure(cost_layout, name_tag=f'cost')

    sector_data = apply_target_spectrum(layout, target_nodes)
    sector_layout = (sector_data, rows, cols)
    save_figure(sector_layout, name_tag=f'sector')

    solved_targets = set()

    while dirty:
        ss += 1
        open_targets = set(target_nodes.keys()) - solved_targets
        mlayout = (mdata, rows, cols)
        mdata, dirty = alt_inflate_regions(mlayout, open_targets, sector_data)

        mlayout = (mdata, rows, cols)
        save_figure(mlayout, 'expanded')

        connex = scan_connected_targets(mlayout, target_nodes)
        new_only = set(connex) - solved_targets
        if new_only:
            for t in new_only:
                mdata = optimize_connected_target(mlayout, t, target_nodes)
                mlayout = (mdata, rows, cols)
                save_figure(mlayout, 'reduced')

            solved_targets |= new_only

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

        solved = False
        cnt = 0
        while not solved and cnt < 1: ## << limit here
            print(f'run {cnt+1}')
            #mdata = evolve_two(layout, target_nodes)
            mdata = find_constrained_nodes(layout, target_nodes)
            data = copy.deepcopy(mdata)
            cnt += 1

        fig, (ax0, ax1, ax2) = plt.subplots(1, 3)

        ax0.matshow(original_data)
        ax1.matshow(data)
        ax2.matshow(solved_data)

        fig.savefig(f'solutions/evo_{filename.rstrip(".csv")}.png')


if __name__ == '__main__':
    duration = timeit.timeit(main, number=1)
    now = datetime.now().strftime('%H:%M:%S')
    print_stage(f'[{now}] Finished in {duration:.2f} seconds.')
