from itertools import islice

def solution(A):
    l = len(A)
    if l < 2:
        return 0
    a = iter(A)
    le1, le2 = next(a), next(a)
    bonus = 0
    if le1 == le2:
        bonus += 1
        le1 -= 1
    first = compute_solution(le1, le2, a) + bonus
    sign = get_sign(le1 - le2)
    if le1 == 1:
        le1 += 1
    le1, le2, bonus = punishment(le1, le2, -sign)
    second = compute_solution(le1, le2, islice(A, 2, l)) + bonus
    return min(first, second)
 
def compute_solution(le1, le2, A):
    sign = -get_sign(le1 - le2)
    c = 0
    for e in A:
        le2, e, b = punishment(le2, e, sign)
        c += b
        le2 = e
        sign = -sign
    return c
 
def punishment(e1, e2, sign):
    if get_sign(e1 - e2) != sign:
        if sign == -1:
            return 1, e2, 1
        else:
            return e1, 1, 1
    return e1, e2, 0
 
def get_sign(e):
    if not e:
        return 0
    return e // abs(e)
    
# rez =  solution([2, 7])
# assert rez == 0
# rez = solution([12   ,11   ,10    ,9    ,8    ,7    ,6,    5    ,4])
# assert rez == 4
# rez = solution([3    ,4    ,5    ,6    ,7    ,8    ,9   ,10])
# assert rez == 3
# rez = solution([9    ,9    ,9    ,9,    6    ,9    ,2])
# assert rez == 2
# rez = solution([9, 3, 2, 8, 6, 9 , 15, 9, 8, 2, 10, 11])
# assert rez == 4 
# rez = solution([9,9,9])
# assert rez == 1
# rez = solution([7,7])
# assert rez == 1
# rez = solution([9,9,9,9]) 
# assert rez == 2
# rez = solution([9,9,9,9,9])
# assert rez == 2
# rez = solution([12   ,11   ,10    ,9    ,8    ,7    ,6    ,5])
# assert rez == 3
# rez = solution([6,7,8])
# assert rez == 1
# rez = solution([8,7,6])
# assert rez == 1
# rez = solution([10, 5, 8, 9,9,9,  ])
# assert rez == 2
# rez = solution([4, 10, 3, 9,9,9,  ])
# assert rez == 1
# rez = solution([4, 10, 3, 9,9,9, 4, 10, 3])
# assert rez == 1
# rez = solution([9, 9, 8, 10, 11, 8, 8])
# assert rez == 3
# rez = solution([9, 9, 8, 10, 8, 8, 8])
# assert rez == 3
# rez = solution([13, 3, 2, 3, 13])
# assert rez == 2
# rez = solution([10, 3 ,11 ,19, 13, 18, 9, 9, 18, 16])
# assert rez == 3
# rez = solution([12, 8, 13, 12, 2 ,10, 18, 19, 16, 19, 14])
# assert rez == 3
# rez = solution([17, 7, 20, 14, 8, 7, 18, 3, 8])
# assert rez == 1
# rez = solution([2 ,2, 2, 9, 5, 2, 13, 15, 8 ])
# assert rez == 3

# import timeit
# n = 10
# print(timeit.timeit("solution(rez)", number=n, setup="from random import randint;rez = [randint(2, 20) for _ in range(1_000_000)];from __main__ import solution") / n)