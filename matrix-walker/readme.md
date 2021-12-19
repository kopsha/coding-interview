# An unusual walk on any matrix


When I encountered this
[matrix walking horror](https://kopsha.github.io/hopeless-programming/#the-code-must-go-on)
at work and I could not live with my self knowing that such _manure_ exists in
any of my repos.


## Problem

Given a matrix **m** x **n**, you need to write an algorithm that walks along
using the following strategies:

* _left-to-right_: the is the natural way
* _top-down_: the natural way, but walking down the columns first
* _zig-zag-horizontal_: walk each row alternating the order, start with left-to-right
* _zig-zag-vertical_: walk each column alternating the order, start with top-down

If you want to take it up a notch:

* use a different _starting-corner_

If you want to take it up another notch:

* _zig-zag-diagonals_
* _zig-zag-anti-diagonals_


## Solution(s)

* [functional walker](walker.py)
