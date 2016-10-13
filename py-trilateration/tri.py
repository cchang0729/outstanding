import math
import numpy as np
import numpy.linalg as ln
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""Define Sphere(Circle) class. radius(double) & center(np.array)"""
class Circle:
    def __init__(self, radius=1.0, center=0.0):
        self.radius = radius
        self.center = center

#check whether two sphere interact
def doesIntersect( c1, c2 ):
    return c1.radius + c2.radius >= ln.norm( c1.center - c2.center )

"""Solve trilateration and return position of beacon. c1 (000), c1(x00), c2(xy0)"""
def solveTrilateration( c1, c2, c3 ):

    beaconPoint = np.array([0.0, 0.0, 0.0])     #return value : point of Beacon
    
    #save value for another 
    cr1 = c1.radius
    cr2 = c2.radius
    cr3 = c3.radius

    #vector calculation
    ex = (c2.center - c1.center)/(ln.norm(c2.center - c1.center))
    i = np.dot( c3.center - c1.center, ex )
    ey = (c3.center - c1.center - i*ex) / (ln.norm(c3.center - c1.center - i*ex))
    ez = np.cross(ex, ey)
    d = ln.norm( c2.center - c1.center )
    j = np.dot(ey, c3.center - c1.center)

    while True:
        beaconPoint[0] = ( c1.radius**2 - c2.radius**2 + d**2 ) / d / 2
        beaconPoint[1] = ( c1.radius**2 - c3.radius**2 + i**2 + j**2 )/j/2 - i/j*beaconPoint[0]
        if( c1.radius**2 - beaconPoint[0]**2 - beaconPoint[1]**2 < 0 ):
            c1.radius += float(cr1) / 100
            c2.radius += float(cr2) / 100
            c3.radius += float(cr3) / 100
        else:
            beaconPoint[2] = math.sqrt(c1.radius**2 - beaconPoint[0]**2 - beaconPoint[1]**2)
            break

    #return original value
    c1.radius = cr1
    c2.radius = cr2
    c3.radius = cr3

    return c1.center + beaconPoint[0]*ex + beaconPoint[1]*ey + beaconPoint[2]*ez

def sphereSurface( c ):
   u = np.linspace(0, 2*np.pi, 100)
   v = np.linspace(0, np.pi, 300)

   x = c.radius * np.outer(np.cos(u), np.sin(v)) + c.center[0]
   y = c.radius * np.outer(np.sin(u), np.sin(v)) + c.center[1]
   z = c.radius * np.outer(np.ones(np.size(u)), np.cos(v)) + c.center[2]

   return [x, y, z]

if __name__ == '__main__':
   #create sphere
   c1 = Circle(1, np.array([3, 0, 0]))
   c2 = Circle(1, np.array([0,3, 0]))
   c3 = Circle(1, np.array([-3, 0, 0]))
   c1.radius = 4.0
   c2.radius = 3.0
   c3.radius = 3.0
   c1.center[2] = 0
   c2.center[2] = 0
   c3.center[2] = 0

   #Solve
   bp = solveTrilateration(c1, c2, c3)

   #Plot
   fig = plt.figure(figsize=(12, 12), dpi=300)
   ax = fig.add_subplot(111, projection='3d')
   ax.set_aspect('equal')

   s1 = sphereSurface(c1)
   s2 = sphereSurface(c2)
   s3 = sphereSurface(c3)
   ax.scatter(bp[0], bp[1], bp[2])
   ax.plot_surface(s1[0], s1[1], s1[2], rstride=4, cstride=4, linewidth=0.1, color='r',  alpha=0.1)
   ax.plot_surface(s2[0], s2[1], s2[2], rstride=4, cstride=4, linewidth=0.1, color='g',  alpha=0.1)
   ax.plot_surface(s3[0], s3[1], s3[2], rstride=4, cstride=4, linewidth=0.1, color='b',  alpha=0.1)


   plt.axis([-10, 10, -10, 10])
   ax.set_zlim3d(-10, 10)
   plt.show()
