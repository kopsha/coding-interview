#zombies.py
import sys
import math
import random

from statistics import mean

def distance( p0, p1 ):
    d = math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
    return int(d)

def reduce_stick( aList, width=3000 ):

    aList.sort()

    l = len(aList)
    s1 = 0
    s2 = l-1
    lx = aList[s2]-aList[s1]

    while lx > width:
        # try to reduce it, from which end ?
        left = aList[s1+(1,2)[l>3]] - aList[s1]
        right = aList[s2] - aList[s2-(1,2)[l>3]]

        if (left <= right):
            s2 -= 1
        else:
            s1 += 1

        l -= 1
        lx = aList[s2]-aList[s1]

    #print( aList, file=sys.stderr )
    #print( "became", aList[s1:(s2+1)], file=sys.stderr )
    return aList[s1:(s2+1)]

def findLucky( people ):
    # shortcuts
    l = len(people)
    
    if l == 0:
        return (8000,4500)      # move to center
    elif l == 1:
        p = list(people.values())
        return p[0]            # save that dude at any cost
    elif l == 2:
        (p1, p2) = people.values()
        if distance( p1, p2 ) <= 4000:
            return (p1[0]+p2[0])>>1,(p1[1]+p2[1])>>1
        else:
            # pick one, the last one ;-)
            return p2
    
    xes = [ people[p][0] for p in people ]
    yes = [ people[p][1] for p in people ]

    stx = reduce_stick( xes )
    sty = reduce_stick( yes )
    
    left = stx[0]
    right = stx[-1]
    top = sty[0]
    bottom = sty[-1]

    schx = []
    schy = []

    for h in people:
        if ((left <= people[h][0]) and (people[h][0] <= right) and
            (top <= people[h][1]) and (people[h][1] <= bottom)):
                schx.append( people[h][0] )
                schy.append( people[h][1] )


    if schx:
        xx = int(mean( schx ))
        yy = int(mean( schy ))
    else:
        k = list(people.keys())[0]
        del people[k]
        return findLucky( people )

    #print( "should save", len(schx), "souls" )

    return (xx,yy)


# Save humans, destroy zombies!

# game loop
while True:
    # me
    x, y = [int(i) for i in input().split()]

    # read humans
    humans = {}
    human_count = int(input())
    for i in range(human_count):
        hid, hu_x, hu_y = [int(j) for j in input().split()]
        humans[hid] = (hu_x, hu_y)
    
    #print( "humans", humans, file=sys.stderr )
    # read zombies
    zombies = {}
    zombie_count = int(input())
    for i in range(zombie_count):
        zid, zo_x, zo_y, zo_nx, zo_ny = [int(j) for j in input().split()]
        zombies[zid] = (zo_x, zo_y)
    
    # eliminate dead people
    toRemove = []
    for h in humans:
        p = humans[h]
        dd = [ distance(p,zombies[z]) for z in zombies ]
        deadIn = min(dd)//400+1
        saveIn = (distance(p, (x,y))-2000)//1000
        #print( "dude", h, "dies in", deadIn, "reach in", saveIn, file=sys.stderr )
        if deadIn <= saveIn:
            toRemove.append( h )
    
    #print( "dead people", toRemove, file=sys.stderr )
    for h in toRemove: del humans[h]
    
    (nx,ny) = findLucky( humans )

    print( nx, ny )