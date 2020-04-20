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


## Questions:

### Question:

How would you implement the property decorator ?

### Answer(s)

Return a descriptor that holds the initial method and when accessed it calls the initial method injecting the received object instead of the self argument.

### Question:

How would you implement a class that makes requests to a remote server that exposes some procedures? The api should look like this. When a method of the object is called:  ```my_class_instance.some_method()``` the instance should call the procedure named ```some_method``` on the remote server.

### Answer(s)
Override the ```__getattr__``` and return a dynamic created function that calls the wanted procedure using the received name.   
### Question:

Why are some websites asking for your permission to use cookies?

### Answer(s)

The cookies on the respective site might be used on other websites as well. For instance if some website uses the js facebook api, it will send the cookies to facebook as well and they might use your private data. 


----


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
    from random import shuffle

    a = list(range(9, 1, -1))

    def is_sorted(a):
        return all([a[i] <= a[i+1] for i in range(len(a)-1)])

    steps = 0
    while not is_sorted(a):
        shuffle(a)
        steps += 1

    print(f'{a} was sorted in {steps} iterations.')
  ```
