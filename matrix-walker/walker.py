"""
A pythonic alternative to this horror:
https://kopsha.github.io/hopeless-programming/#the-code-must-go-on

This one has an easier interface, having a grid size and a walk order,
you get a position (row, col tuple) generator starting from top left corner:

Example:
```
grid = [[None] * cols for _ in range(rows)]

zig_zag_walk = grid_walk("zig_zag_vertical"), rows, cols)
for i, position in enumerate(zig_zag_walk):
    row, col = position
    grid[row][col] = i + 1
```
"""
from itertools import cycle, repeat, chain, zip_longest


def count_repeated(count, times):
    """
    Count up sequence with each element repeated n times
    """
    for i in range(count):
        yield from repeat(i, times)


def count_up_down(count):
    """
    Count up and back down sequence
    """
    yield from chain(range(count), reversed(range(count)))


def count_up_down_repeated(count):
    """
    Count up and back down sequence with each element repeated
    """
    yield from chain.from_iterable(zip(count_up_down(count), count_up_down(count)))


def double_step_count_repeated(count, times):
    """
    Count up sequence with consecutive pairs repeated n times
    """
    natural = range(count)
    for di in zip_longest(natural[::2], natural[1::2]):
        yield from chain.from_iterable(repeat(di, times))


def grid_walk(walk_order, rows, cols):
    """Grid position generator, given a strategy and a grid size (no transforms)"""

    if rows <= 0 or cols <= 0:
        raise ValueError("Grid size cannot be zero or negative")

    walk_strategies = {
        "left_right": (count_repeated(count=rows, times=cols), cycle(range(cols))),
        "top_down": (cycle(range(rows)), count_repeated(count=cols, times=rows)),
        "zig_zag_horizontal": (count_repeated(count=rows, times=cols), cycle(count_up_down(cols))),
        "zig_zag_vertical": (cycle(count_up_down(rows)), count_repeated(count=cols, times=rows)),
        "2rows_horizontal": (
            double_step_count_repeated(count=rows, times=cols),
            cycle(count_up_down_repeated(cols)),
        ),
    }

    row_gen, col_gen = walk_strategies[walk_order]

    if walk_order == "2rows_horizontal" and rows % 2:
        for _ in range((rows - 1) * cols):
            yield next(row_gen), next(col_gen)

        ## on last row switch to zig-zag single row strategy
        # if (rows // 2) % 2:
        #     for col in reversed(range(cols)):
        #         yield rows - 1, col
        # else:
        #     for col in range(cols):
        #         yield rows - 1, col
    else:
        for _ in range(rows * cols):
            yield next(row_gen), next(col_gen)


def starting_corner_transform(starting_corner, rows, cols, position):
    row, col = position
    transformations = dict(
        top_left=(row, col),
        top_right=(row, cols - (col + 1)),  # horizontal reflection
        bottom_left=(rows - (row + 1), col),  # vertical reflection
        bottom_right=(rows - (row + 1), cols - (col + 1)),  # diagonal_reflection
    )
    return transformations[starting_corner]


def one_based_index_transform(position):
    row, col = position
    return row + 1, col + 1


def natural_grid_walk(walk_order, starting_corner, rows, cols):
    """
    Grid position generator, given a strategy, starting corner and a grid size
    Using quicktrials specific transformations:
    * starting corner
    * 1 based indexing
    """

    raw_walker = grid_walk(walk_order, rows, cols)
    for position in raw_walker:
        new_position = starting_corner_transform(starting_corner, rows, cols, position)
        new_position = one_based_index_transform(new_position)
        yield new_position


def print_grid(grid):
    for row in grid:
        print("    [", end="")
        for item in row:
            print(f"{item:5}" if item else "   --", end="")
        print("  ]")


def main():

    rows, cols = 5, 4

    available_starting_corners = (
        "top_left",
        "top_right",
        "bottom_left",
        "bottom_right",
    )

    available_strategies = (
        "left_right",
        "top_down",
        "zig_zag_horizontal",
        "zig_zag_vertical",
        "2rows_horizontal",
    )

    for walk_order in available_strategies:

        for starting_corner in available_starting_corners:
            walker = natural_grid_walk(walk_order, starting_corner, rows, cols)

            print(f"\n .. {walk_order} strategy, starting on {starting_corner} .. [{rows} x {cols}]\n")
            grid = [[None] * cols for _ in range(rows)]

            for i, position in enumerate(walker):
                row, col = position
                grid[row - 1][col - 1] = i + 1

            print_grid(grid)


if __name__ == "__main__":
    main()
