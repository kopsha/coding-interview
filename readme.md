# Programming challenges

A collection of interesting questions or challenges encountered on programming
interviews.

## Aesthetic tree cutting

A gardener consider aesthetically appealing gardens in which the tops of sequential physical trees (eg palm trees) are always sequentially going up and down, that is:

```
|               |
|       |       |
|   |   |   |   |
```

On the other hand, the following configurations would be invalid:

```
|
|  |
|  |  |  
```

reason: 3rd tree should be higher than the 2nd one

```
|  |
|  |
|  |    
```

reason: consecutive trees cannot have the same height

Given a sequence of physical trees in a garden, what is the minimum number of physical trees which must be cropped/cut in order to achieve the pattern desired by that gardener?


### Solution(s)

* [an easy to understand solution](aesthetic_tree_cutting/functional.py)
* [a memory efficient solutiuon](aesthetic_tree_cutting/iterative.py)


## Closing thoughts

During an interview there is very little time to find and implement an optimal
solution, so I am more interested in how the candidate approaches a difficult
(maybe impossible) task and here's how you can gain some points:
* first, identify what kind of problem is it: path finding, sorting, merging, exploring, computation
  * maybe this problem be solved with classical algorithms, explain which
  one and how it works?
* break down the big problem into smaller / simpler parts (remember "divide et impera" ?)
  * solve at least one part of the problem
* if the problem is apparently overwhelming, propose a simpler
alternative version which you can solve
* classify your solution time complexity
  * if your solution is not optimal, describe how the optimal should look like
