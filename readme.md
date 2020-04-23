# Programming challenges

A collection of interesting questions or challenges encountered on programming
interviews.


## Problematic list

* [Aesthetic tree cutting](aesthetic_tree_cutting/)
* [PIN variations](pin-variations/)


## F.A.Q.

* [Q & A](questions/)


## Closing thoughts

During an interview there is very little time to find and implement an optimal
solution, so I am more interested in how the candidate approaches a difficult
(maybe impossible) task and here's how you can gain some points:
* first, identify what kind of problem is it: path finding, sorting, merging, exploring, computation
  * maybe this problem can be solved with classical algorithms, explain which
  one and how it works?
* break down the big problem into smaller / simpler parts (remember "divide et impera" ?)
  * if the problem is apparently overwhelming, propose a simpler
alternative version which you can solve
* classify your solution time complexity
  * if your solution is not optimal, describe how the optimal should look like
* if you have time, offer another solution (even if is less efficient)
  * here's the funniest example I have ever seen for sorting a list
  ```python
    def is_sorted(a):
        return all([a[i] <= a[i+1] for i in range(len(a)-1)])

    while not is_sorted(a):
        shuffle(a)
  ```
