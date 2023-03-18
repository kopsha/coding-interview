import sys
import math
import operator

# Save humans, destroy zombies!
def distance( p0, p1 ):
    d = math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
    #print( d, " rounded ", int(d) )
    return int(d)

# game loop
while True:
    x, y = [int(i) for i in input().split()]
    myx = x
    myy = y

    humans = {}
    human_count = int(input())
    for i in range(human_count):
        hid, hu_x, hu_y = [int(j) for j in input().split()]
        humans[hid] = (hu_x, hu_y)
    
    zombies = {}
    zombie_count = int(input())
    
    kid = -1
    kd = 16000
    
    for i in range(zombie_count):
        zid, zo_x, zo_y, zo_nx, zo_ny = [int(j) for j in input().split()]
        #dist2humans = [ distance( (zo_nx,zo_ny),humans[h] ) for h in humans ]
        zombies[zid] = (zo_nx, zo_ny)
        dist = distance((x,y), (zo_nx,zo_ny))
        
        #closest zombie
        if (kid == -1):
            kid = zid
            kd = dist
        elif kd > dist:
            kid = zid
            kd = dist

    #print( "humans", humans, file=sys.stderr )
    #print( "zombies", zombies, file=sys.stderr )
    
    if zombies:
        myx,myy = zombies[kid]
    else:
        myx,myy = humans[0]
        
    print( myx, myy )
