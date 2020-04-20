import timeit
from datetime import datetime


def print_stage(text, row_size=80):
    filler = ' ' * (row_size - 4 - len(text))
    print(f'{"*" * row_size}')
    print(f'* {text}{filler} *')
    print(f'{"*" * row_size}')


def padded_str(s):
    if type(s) is bool:
        result = '•' if s else ''
    else:
        result = str(s)
    return f'{result:>3}'


def flatt(arr):
    return '  '.join(map(padded_str, arr))


def alternator(left, right, count):
    for x in range(count):
        yield left if x % 2 == 0 else right


def not_equal(pair):
    l, r = pair
    return int(l != r)


def diff_mask(left, right):
    assert len(left) == len(right)
    return [l != r for l, r in zip(left, right)]


def sign(x):
    return 0 if x == 0 else (-1 if x < 0 else 1)


def solve(array):
    normal = [sign(right - left) for left, right in zip(array[:-1], array[1:])]

    target = list(alternator(-1, 1, count=len(normal)))
    alt_target = list(alternator(1, -1, count=len(normal)))

    delta = list(map(not_equal, zip(normal, target)))
    alt_delta = list(map(not_equal, zip(normal, alt_target)))

    optima = min(delta, alt_delta, key=lambda diffs: sum(diffs))
    sel_target = target if delta == optima else alt_target

    solution = list(array)
    for i, (cut, how) in enumerate(zip(optima, sel_target)):
        if cut:
            left, right = solution[i], solution[i + 1]

            if how == sign(right - left):
                continue    # this cut is not required anymore

            if how == -1:   # descending
                solution[i], solution[i + 1] = left, min(left - 1, right)
            else:           # ascending
                solution[i], solution[i + 1] = min(left, right - 1), right

    cuts = sum(diff_mask(array, solution))

    return cuts, solution


def result_equals(testcase):
    expected, actual = testcase
    assert type(actual) is tuple
    return expected == actual[0]


def validate():
    tests = (
        (0, solve([2, 7])),
        (0, solve([2, 7, 6])),
        (1, solve([2, 6, 9])),
        (1, solve([2, 3, 5, 7])),

        (3, solve(range(3, 10))),
        (3, solve(range(12, 4, -1))),
        (3, solve([9, 3, 2, 8, 6, 9, 15, 9, 8, 2])),
        (1, solve([8, 9, 9, 10, 6, 9, 1])),
        (1, solve([8, 9, 9, 9, 6, 9, 1])),
        (2, solve([10, 9, 9, 9, 6, 9, 1])),

        (1, solve([7] * 2)),
        (1, solve([7] * 3)),
        (2, solve([7] * 4)),
        (2, solve([7] * 5)),
        (3, solve([7] * 6)),
    )

    passed = sum(map(result_equals, tests))
    failed = len(tests) - passed
    all_pass = failed == 0 and passed > 0

    if not all_pass:
        # show full summary
        for t in tests:
            expected, (actual, sol) = t
            result_str = ' passed ' if result_equals(t) else ' failed '
            print(expected, '==', actual, result_str, sol)

    print(f'{passed} tests pass and {failed} tests failed.')
    return all_pass


def main():
    if not validate():
        print_stage('invalid, try again...')
        return

    samples = (
        [2, 7],
        [2, 3, 5, 7],
        range(3, 8),
        range(9, 4, -1),
        [9, 3, 2, 8, 6, 9, 15, 9, 8, 2],
        [9, 9, 10, 6, 9, 1],
        [8, 9, 9, 9, 6, 9, 1],
        [17, 7, 20, 14, 8, 7, 18, 3, 8],
    )

    for cnt, position in enumerate(samples):
        cuts, solution = solve(position)

        print('')
        print(f'  case # {1+cnt:02}\n')
        print(f'input           {flatt(position)}')
        print(f' {cuts:3} cut(s) ->  {flatt(diff_mask(position, solution))}')
        print(f'solution        {flatt(solution)}')

    print('')


if __name__ == '__main__':
    duration = timeit.timeit(main, number=1)
    now = datetime.now().strftime('%H:%M:%S')
    print_stage(f'[{now}] Finished in {duration:.2f} seconds.')
