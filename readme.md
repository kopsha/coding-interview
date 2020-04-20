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

[Solution](aesthetic_tree_cutting.py)
