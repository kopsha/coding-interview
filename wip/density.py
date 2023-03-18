#density.py
import math
from statistics import mean

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def reduce_stick( aList, width=4000 ):

    aList.sort()

    l = len(aList)
    s1 = 0
    s2 = l-1
    lx = aList[s2]-aList[s1]

    while lx > width:
        # try to reduce it, from which end ?
        left = aList[s1+1] - aList[s1]
        right = aList[s2] - aList[s2-1]

        if (left < right):
            s2 -= 1
        else:
            s1 += 1

        l -= 1
        lx = aList[s2]-aList[s1]

    return aList[s1:(s2+1)]

def findLucky( people ):
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

    xx = int(mean( schx ))
    yy = int(mean( schy ))

    #print( "should save", len(schx), "souls" )

    return (xx,yy)
humans = {
        0: (0, 1000),
        1: (0, 8000)
    }
zombies = {
        0: (5000, 1000),
        1: (5000, 8000),
        2: (7000, 1000),
        3: (7000, 8000),
        4: (9000, 1000),
        5: (9000, 8000),
        6: (11000, 1000),
        7: (11000, 8000),
        8: (13000, 1000),
        9: (13000, 8000),
        10: (14000, 1000),
        11: (14000, 8000),
        12: (14500, 1000),
        13: (14500, 8000),
        14: (15000, 1000),
        15: (15000, 8000)
    }

(x,y) = findLucky( humans )
me = ( 0,4000 )
print( "should aim to: ", x,y )

dangerzone = {}
z2k = None
for zid in zombies:
    z = zombies[zid]
    print( "zombie", zid, "at", z )
    d2p = [ distance( humans[p], z ) for p in humans ]
    dangerzone[zid] = int(min(d2p))
    dangerSteps = dangerzone[zid]//400
    deadDistance = distance( me, z )
    print( "closest human at ", dangerzone[zid], "reaches target in", dangerSteps )
    print( "distance to it", deadDistance, "dead in", (deadDistance-2000)//1400 )
    if dangerzone[zid]==min(dangerzone.values()):
        z2k = zid

print( "closest zombie", min(dangerzone.values()), "id", z2k )
