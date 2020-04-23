# Hacking all PIN variations

Suppose that you are part of a team that breaks electric locks.
The way the team operates is rthat there is a spy that overlooks what
pin is introduced into the lock’s keyboard and reports it to you.
Unfortunately he is not completely sure that he saw the correct combination
and all adjacent (vertical and horizontal) keys of a key could be the correct
key.

Given a keyboard and a reported pin, your task is to generate all possible
variations of the observed pin. The pin can have any length.

_Example_:
```python
keyboard = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#'],
]

Reported_pin = '13'

Possible variations = ['13', '23', '43', '12', '22', '42', '16', '26', '46']
```
_Explanation_: Adjacent keys of 1 are 2 and 4 and adjacent keys of 3 are 2 and 6
