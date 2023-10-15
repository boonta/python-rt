# Vec3 
import math
import numpy as np
from PIL import Image as im
import sys

global infinity_number
global pi 

infinity_number = sys.float_info.max
pi = 3.1415926535897932385

class Vec3:
    def __init__(self, e0=0.0, e1=0.0, e2=0.0) -> None:
        self.e = [e0, e1, e2]
        pass

    def x(self):
        return self.e[0]
    def y(self):
        return self.e[1]
    def z(self):
        return self.e[2]

    def len_squared(self):
        return self.e[0]*self.e[0] + self.e[1]*self.e[1] + self.e[2]*self.e[2]

    def len(self):
        return math.sqrt(self.len_squared())

    def __truediv__(self, val):
        return Vec3(self.e[0]/val, self.e[1]/val, self.e[2]/val)
    
    def __add__(self, vec):
        return Vec3(self.e[0] + vec.x(), self.e[1] + vec.y(), self.e[2] + vec.z())
    
    def __sub__(self, vec):
        return Vec3(self.e[0] - vec.x(), self.e[1] - vec.y(), self.e[2] - vec.z())
    
    def __mul__(self, val):
        return Vec3(self.e[0]*val, self.e[1]*val, self.e[2]*val)
    
    def __neg__(self):
        return Vec3(-self.e[0], -self.e[1], -self.e[2])

    def printout(self):
        print('{%.5f},{%.5f},{%.5f}'.format(self.e[0], self.e[1], self.e[2]))

    @staticmethod
    def unit_vector(v):
        return v / v.len()

    @staticmethod
    def cross_product(u, v):
        return Vec3(u.y()*v.z() - u.z()*v.y(),
                    u.z()*v.x() - u.x()*v.z(),
                    u.x()*v.y() - u.y()*v.x())
    
    @staticmethod
    def dot_product(u, v):
        return u.x()*v.x() + u.y()*v.y() + u.z()*v.z()
    
class Color(Vec3):
    def __init__(self, e0=0, e1=0, e2=0) -> None:
        super().__init__(e0, e1, e2)

    def r(self):
        return self.e[0]
    
    def g(self):
        return self.e[1]
    
    def b(self):
        return self.e[2]
    
    def write_to_256(self):
        return Color(int(self.e[0]*255), int(self.e[1]*255), int(self.e[2]*255))
    
    def __truediv__(self, val):
        return Color(self.e[0]/val, self.e[1]/val, self.e[2]/val)
    
    def __add__(self, vec):
        return Color(self.e[0] + vec.r(), self.e[1] + vec.g(), self.e[2] + vec.b())
    
    def __sub__(self, vec):
        return Color(self.e[0] - vec.r(), self.e[1] - vec.g(), self.e[2] - vec.b())
    
    def __mul__(self, val):
        return Color(self.e[0]*val, self.e[1]*val, self.e[2]*val)
    
    def __neg__(self):
        return Color(-self.e[0], -self.e[1], -self.e[2])


class Hitinfo:
    def __init__(self, p, vNormal, t) -> None:
        self.point = p
        self.normal = vNormal
        self.t = t
        self.front_face = True
        pass

    def set_face_normal(self, vRay, outwardNormal):
        self.front_face = Vec3.dot_product(vRay.getDirection(), outwardNormal) < 0
        if self.front_face:
            self.normal = outwardNormal
        else:
            self.normal = -outwardNormal
        pass

    def getT(self):
        return self.t
    
    def getNormal(self):
        return self.normal
    
class Interval:
    def __init__(self, minval, maxval) -> None:
        self.min_val = minval
        self.max_val = maxval 
        pass

    def contains(self, x):
        return self.min_val <= x and x <= self.max_val
    
    def surrounds(self, x):
        return self.min_val < x and x < self.max_val
    
    @staticmethod
    def Empty():
        return Interval(+infinity_number, -infinity_number)
    
    @staticmethod
    def Universe():
        return Interval(-infinity_number, +infinity_number)
