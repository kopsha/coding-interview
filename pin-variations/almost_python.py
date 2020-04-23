#!/usr/bin/env python3

# Suppose that you are part of a team that breaks electric locks.
# The way the team operates is rthat there is a spy that overlooks what
# pin is introduced into the lock’s keyboard and reports it to you.
# Unfortunately he is not completely sure that he saw the correct combination
# and all adjacent (vertical and horizontal) keys of a key could be the correct
# key.
#
# Given a keyboard and a reported pin, your task is to generate all possible
# variations of the observed pin. The pin can have any length.
#
# Example:
#
# Keyboard = [
#     [1, 2, 3]
#     [4, 5, 6]
#     [7, 8, 9]
#     [*, 0, #]
# ]
#
# Reported_pin = “13”
#
# Possible variations = [“13”, “23”, “43”, “12”, “22”, “42”, “16”, “26”, “46”]
#
# Explanation:
#
# Adjacent keys of 1 are 2 and 4 and adjacent keys of 3 are 2 and 6

from collections import defaultdict


def solution(keyboard, reported_pin):
    neighbours = get_all_neighbours(keyboard, reported_pin)
    rez = []
    get_all_possible_combinations(keyboard, neighbours, reported_pin, 0, rez, '')
    return rez


def get_all_neighbours(keyboard, reported_pin):
    neighbours = defaultdict(list)
    for i, board in enumerate(keyboard):
        for j, pin in enumerate(board):
            if pin in reported_pin:
                add_neighbours_for_pin(neighbours, keyboard, i, j)
    return neighbours


def add_neighbours_for_pin(neighbours, keyboard, i, j):
    valid_neighbours = [
        (k, l)
        for k, l in
        ((i + 1, j), (i, j - 1), (i - 1, j), (i, j + 1), (i, j))
        if not (k < 0 or k >= len(keyboard) or l < 0 or l >= len(keyboard[0]))
    ]
    for vd in valid_neighbours:
        neighbours[keyboard[i][j]].append(vd)


def get_all_possible_combinations(keyboard, neighbours, reported_pin, k, rez, solution):
    if k == len(neighbours):
        rez.append(solution)
        return

    for i, j in neighbours[reported_pin[k]]:
        new_solution = solution + keyboard[i][j]
        get_all_possible_combinations(keyboard, neighbours, reported_pin, k + 1, rez, new_solution)


keyboard = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#'],
]

print(solution(keyboard, '13'))
