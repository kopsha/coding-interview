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

Edge = namedtuple('Edge', ['vertex', 'weight'])

class GraphUndirectedWeighted(object):  
    def __init__(self, vertex_count):
        self.vertex_count = vertex_count
        self.adjacency_list = [[] for _ in range(vertex_count)]

    def add_edge(self, source, dest, weight):
        assert source < self.vertex_count
        assert dest < self.vertex_count
        self.adjacency_list[source].append(Edge(dest, weight))
        self.adjacency_list[dest].append(Edge(source, weight))

    def get_edge(self, vertex):
        for e in self.adjacency_list[vertex]:
            yield e

    def get_vertex(self):
        for v in range(self.vertex_count):
            yield v


def dijkstra(graph, source, dest):  
    q = queue.PriorityQueue()
    parents = []
    distances = []
    start_weight = float("inf")

    for i in graph.get_vertex():
        weight = start_weight
        if source == i:
            weight = 0
        distances.append(weight)
        parents.append(None)

    q.put(([0, source]))

    while not q.empty():
        v_tuple = q.get()
        v = v_tuple[1]

        for e in graph.get_edge(v):
            candidate_distance = distances[v] + e.weight
            if distances[e.vertex] > candidate_distance:
                distances[e.vertex] = candidate_distance
                parents[e.vertex] = v
                # primitive but effective negative cycle detection
                if candidate_distance < -1000:
                    raise Exception("Negative cycle detected")
                q.put(([distances[e.vertex], e.vertex]))

    shortest_path = []
    end = dest
    while end is not None:
        shortest_path.append(end)
        end = parents[end]

    shortest_path.reverse()

    return shortest_path, distances[dest]

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


def join_target_pins(data, target):
    rows = len(data)
    assert rows > 1
    cols = len(data[0])
    assert cols > 1

    def mask_other_data(data, target):
        walls = []
        target_nodes = []
        masked_data = copy.deepcopy(data)
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                node = (i, j)

                if val == target:
                    target_nodes.append(node)
                elif val > 0:
                    walls.append(node)
                elif val == 0:
                    something_else = set(boxed_labels(data, node)) - {0, target}
                    if len(something_else) >= 1:
                        walls.append(node)

        assert len(target_nodes) > 1

        for node in walls:
            i, j = node
            masked_data[i][j] = WALL_MARK

        return masked_data, target_nodes, walls

    def mark_target_grid(data, target_nodes):
        masked_data = copy.deepcopy(data)

        target_cols = [j for _, j in target_nodes]
        target_rows = [i for i, _ in target_nodes]

        for i, row in enumerate(masked_data):
            previous = None
            for j, val in enumerate(row):
                node = (i, j)

                if i in target_rows or j in target_cols:
                    if val == 0:
                        masked_data[i][j] = IMPORTANT_MARK

        return masked_data

    def mark_important_nodes(data):
        masked_data = copy.deepcopy(data)
        for i, row in enumerate(masked_data):
            previous = None
            for j, val in enumerate(row):
                node = (i, j)

                if val == 0:
                    if previous == None:
                        previous = val
                        masked_data[i][j] = IMPORTANT_MARK
                    else:
                        nbs = boxed_labels(masked_data, node)
                        something_else = set(nbs) - {0, IMPORTANT_MARK}
                        if len(nbs) in [3, 5] or len(something_else) > 0:
                            masked_data[i][j] = IMPORTANT_MARK

        return masked_data

    def mark_critical_nodes(data, target):
        masked_data = copy.deepcopy(data)

        for i, row in enumerate(masked_data):
            previous = None
            for j, val in enumerate(row):
                node = (i, j)
                if val == IMPORTANT_MARK:
                    all_nbs = boxed_labels(masked_data, node)
                    if len(all_nbs) == 3:
                        masked_data[i][j] = CRITICAL_MARK
                    nbs = [l for l in crossed_labels(masked_data, node) if l in [IMPORTANT_MARK, CRITICAL_MARK]]
                    vip_nbs = [l for l in crossed_labels(masked_data, node) if l == target]
                    if len(nbs) > 2 or len(vip_nbs) > 0:
                        masked_data[i][j] = CRITICAL_MARK

        return masked_data

    def crossed_neighbours(data, node):
        i,j = node
        directions = ( (i-1, j), (i, j-1), (i+1, j), (i, j+1) )
        connected_neighbours = [
            (di, dj)
            for di, dj in directions
            if (0 <= di < rows) and (0 <= dj < cols) and \
                data[di][dj] in [IMPORTANT_MARK, CRITICAL_MARK, target]
        ]
        return connected_neighbours

    def next_critical_from(data, from_node, to_node, step):
        i,j = to_node
        if data[i][j] in [CRITICAL_MARK, target]:
            return ((to_node, step), [from_node, to_node])

        options = crossed_neighbours(data, to_node)
        options.remove(from_node)

        if not options:
            return None, []

        assert len(options) == 1
        next_move = options.pop()
        di, dj = next_move

        nc, trace = next_critical_from(data, to_node, next_move, step + 1)
        if nc:
            dest, dist = nc
            return (dest, dist), [from_node, *trace]

        return None, []

    def create_nodes(data, target, target_nodes):
        vertices = []
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                node = (i, j)
                if val in [CRITICAL_MARK, target]:
                    vertices.append(node)

        edges = []

        for node in vertices:
            options = crossed_neighbours(data, node)
            for direction in options:
                di, dj = direction
                nc, trace = next_critical_from(data, node, direction, 1)
                if nc:
                    dest, dist = nc
                    edges.append( ((node, dest, dist), trace) )
            
        return vertices, edges


    masked_data, target_nodes, walls = mask_other_data(data, target)
    masked_data = mark_target_grid(masked_data, target_nodes)
    masked_data = mark_important_nodes(masked_data)
    masked_data = mark_critical_nodes(masked_data, target)


    ## build the search graph, finally
    v, e = create_nodes(masked_data, target, target_nodes)

    g = GraphUndirectedWeighted( len(v) )
    gd = {}

    for sdd, trace in e:
        src, dest, dist = sdd
        g.add_edge( v.index(src), v.index(dest), dist )
        gd[(src, dest)] = dist, trace
        gd[(dest, src)] = dist, trace

    # print(f'search graph for {target} has {len(v)} nodes and {len(e)} edges.')
    # print(f'{len(target_nodes)} targets: {target_nodes}')

    # restore masks
    masked_data = copy.deepcopy(data)
    for left, right in zip(target_nodes[:-1], target_nodes[1:]):    
        path, distance = dijkstra(g, v.index(left), v.index(right))
        if distance == float('inf'):
            print(f'no path found from {left} to {right}, for pin {target}')
            continue
        # paint the solution
        for lx, rx in zip(path[:-1], path[1:]):
            left = v[lx]
            right = v[rx]
            distance, trace = gd[(left, right)]
            for n in trace:
                i,j = n
                masked_data[i][j] = target

    return masked_data

def scan_target_set(data):
    result = set()
    for rows in data:
        for value in rows:
            if value > 0:
                result.add(value)
    return result

IMPORTANT_MARK = -1
CRITICAL_MARK = -2
WALL_MARK = -3

def main():

    data = []
    with open('Step_Two.csv', newline='') as csvfile:
        content = csv.reader(csvfile, delimiter=',')
        for row in content:
            data.append( list(map(lambda x: WALL_MARK if x == 'Z' else int(x), row)) )

    print_stage('input data')
    original_data = copy.deepcopy(data)
    rows = len(original_data)
    assert rows > 1
    cols = len(original_data[0])
    assert cols > 1
    print(f'shape: {rows} x {cols}')

    targets = list(scan_target_set(original_data))
    shuffle(targets)
    print('target set: ', targets)

    for t in targets:
        data = join_target_pins(data, t)

    fig, (ax0, ax1) = plt.subplots(1, 2)

    ax0.matshow(original_data)
    ax1.matshow(data)

    plt.show()


if __name__ == '__main__':
    duration = timeit.timeit(main, number=1)
    now = datetime.now().strftime('%H:%M:%S')
    print_stage(f'[{now}] Finished in {duration:.2f} seconds.')
