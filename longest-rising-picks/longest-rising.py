#!/usr/bin/env python3
from itertools import combinations


def is_rising(values):
    return all(a <= b for a, b in zip(values[:-1], values[1:]))


def longest_rising(data):
    positions = range(len(data))
    for slen in range(len(data), 0, -1):
        for xi in combinations(positions, slen):
            values = [data[i] for i in xi]
            if is_rising(values):
                return slen
    return 0


def test_longest_rising_seq():
    given = [-1, 0, 9, 8, -5, 6, -24]
    assert longest_rising(given) == 3


def main():
    print("anything")


if __name__ == "__main__":
    main()
