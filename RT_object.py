# object class
import RT_ray as rtr
import RT_utility as rtu
import math

class Hitinfo:
    def __init__(self, p, vNormal, t) -> None:
        self.point = p
        self.normal = vNormal
        self.t = t
        self.front_face = True
        pass

    def set_face_normal(self, vRay, outwardNormal):
        self.front_face = rtu.Vec3.dot_product(vRay.getDirection(), outwardNormal) < 0
        if self.front_face:
            self.normal = outwardNormal
        else:
            self.normal = -outwardNormal
        pass

    def getT(self):
        return self.t
    
    def getNormal(self):
        return self.normal

class Object:
    def __init__(self) -> None:
        pass

    def intersect(self, vRay):
        pass

    def intersect(self, vRay, tmin, tmax):
        pass

class Sphere(Object):
    def __init__(self, vCenter, fRadius) -> None:
        super().__init__()
        self.center = vCenter
        self.radius = fRadius

    def printInfo(self):
        self.center.printout()        
        

    def intersect(self, vRay):
        oc = vRay.getOrigin() - self.center
        a = rtu.Vec3.dot_product(vRay.getDirection(), vRay.getDirection())
        b = 2.0 * rtu.Vec3.dot_product(oc, vRay.getDirection())
        c = rtu.Vec3.dot_product(oc, oc) - self.radius*self.radius
        discriminant = b*b - 4*a*c 

        if discriminant < 0:
            return -1.0
        else:
            return (-b -math.sqrt(discriminant)) / (2.0*a)

    def intersect(self, vRay, tmin, tmax):

        if tmin < 0:
            return None
        
        oc = vRay.getOrigin() - self.center
        a = vRay.getDirection().len_squared()
        half_b = rtu.Vec3.dot_product(oc, vRay.getDirection())
        c = oc.len_squared() - self.radius*self.radius
        discriminant = half_b*half_b - a*c 

        if discriminant < 0:
            return None
        sqrt_disc = math.sqrt(discriminant)

        root = (-half_b - sqrt_disc) / a 
        if root <= tmin or root >= tmax:
            root = (-half_b + sqrt_disc) / a 
            if root <= tmin or root >= tmax:
                return None
            
        hit_t = root
        hit_point = vRay.at(root)
        hit_normal = (hit_point - self.center) / self.radius
        hinfo = Hitinfo(hit_point, hit_normal, hit_t)

        hinfo.set_face_normal(vRay, hit_normal) 
        return hinfo


