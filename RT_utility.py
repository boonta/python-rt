# Vec3 
import math
import numpy as np
from PIL import Image as im
import sys

global infinity_number
global pi 

infinity_number = sys.float_info.max
pi = 3.1415926535897932385

def random_double(min=0.0, max=1.0):
    return np.random.uniform(min, max)

def linear_to_gamma(val, gammaVal):
    return math.pow(val, 1.0/gammaVal)

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
        print('{},{},{}'.format(self.e[0], self.e[1], self.e[2]))

    def near_zero(self):
        tol = 1e-8
        return (math.fabs(self.e[0]) < tol) and (math.fabs(self.e[1]) < tol) and (math.fabs(self.e[2]) < tol)

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
    
    @staticmethod
    def random_vec3(minval=0.0, maxval=1.0):
        return Vec3(random_double(minval, maxval), random_double(minval, maxval), random_double(minval, maxval))

    @staticmethod
    def random_vec3_in_unit_disk():
        while True:
            p = Vec3(random_double(-1,1), random_double(-1,1), 0)
            if p.len_squared() < 1:
                return p

    @staticmethod
    def random_vec3_in_unit_sphere():
        while True:
            p = Vec3.random_vec3(-1, 1)
            if p.len_squared() < 1:
                return p 
    
    @staticmethod
    def random_vec3_unit():
        return Vec3.unit_vector(Vec3.random_vec3_in_unit_sphere())

    @staticmethod
    def random_vec3_on_hemisphere(vNormal):
        in_unit_sphere = Vec3.random_vec3_unit()
        if Vec3.dot_product(in_unit_sphere, vNormal) > 0.0:
            return in_unit_sphere
        else:
            return -in_unit_sphere

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
        if isinstance(val, Color):
            return Color(self.e[0]*val.r(), self.e[1]*val.g(), self.e[2]*val.b())

        return Color(self.e[0]*val, self.e[1]*val, self.e[2]*val)
    

    def __neg__(self):
        return Color(-self.e[0], -self.e[1], -self.e[2])


class Hitinfo:
    def __init__(self, vP, vNormal, fT, mMat=None, tcTex=None) -> None:
        self.point = vP
        self.normal = vNormal
        self.t = fT
        self.front_face = True
        self.mat = mMat
        self.texture_uv = tcTex
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
    
    def getP(self):
        return self.point
    
    def getMaterial(self):
        return self.mat

    def getTextureUV(self):
        return self.texture_uv

class Scatterinfo:
    def __init__(self, vRay, fAttenuation) -> None:
        self.scattered_ray = vRay
        self.attenuation_color = fAttenuation


class Interval:
    def __init__(self, minval, maxval) -> None:
        self.min_val = minval
        self.max_val = maxval 
        pass

    def contains(self, x):
        return self.min_val <= x and x <= self.max_val
    
    def surrounds(self, x):
        return self.min_val < x and x < self.max_val
    
    def clamp(self, x):
        if x < self.min_val:
            return self.min_val
        if x > self.max_val:
            return self.max_val
        return x
    
    @staticmethod
    def near_zero(self, x, fTol=1e-8):
        tol = fTol
        return math.fabs(x) < tol
    
    @staticmethod
    def Empty():
        return Interval(+infinity_number, -infinity_number)
    
    @staticmethod
    def Universe():
        return Interval(-infinity_number, +infinity_number)
