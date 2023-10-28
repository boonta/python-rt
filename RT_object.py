# object class
import RT_ray as rtr
import RT_utility as rtu
import RT_material as rtm
import RT_texture as rtt
import math

class Object:
    def __init__(self) -> None:
        pass

    def intersect(self, vRay):
        pass

    def intersect(self, vRay, tmin, tmax):
        pass

    def intersect(self, vRay, cInterval):
        pass

class Sphere(Object):
    def __init__(self, vCenter, fRadius, mMat=None) -> None:
        super().__init__()
        self.center = vCenter
        self.radius = fRadius
        self.material = mMat

    def add_material(self, mMat):
        self.material = mMat

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
        hinfo = rtu.Hitinfo(hit_point, hit_normal, hit_t, self.material)

        hinfo.set_face_normal(vRay, hit_normal) 
        return hinfo
    
    # main intersection calling
    def intersect(self, vRay, cInterval):
        
        oc = vRay.getOrigin() - self.center
        a = vRay.getDirection().len_squared()
        half_b = rtu.Vec3.dot_product(oc, vRay.getDirection())
        c = oc.len_squared() - self.radius*self.radius
        discriminant = half_b*half_b - a*c 

        if discriminant < 0:
            return None
        sqrt_disc = math.sqrt(discriminant)

        root = (-half_b - sqrt_disc) / a 
        if not cInterval.surrounds(root):
            root = (-half_b + sqrt_disc) / a 
            if not cInterval.surrounds(root):
                return None
            
        hit_t = root
        hit_point = vRay.at(root)
        hit_normal = (hit_point - self.center) / self.radius
        hinfo = rtu.Hitinfo(hit_point, hit_normal, hit_t, self.material)

        hinfo.set_face_normal(vRay, hit_normal) 
        return hinfo

# Ax + By + Cz = D
class Quad(Object):
    def __init__(self, vQ, vU, vV, mMat=None) -> None:
        super().__init__()
        self.Qpoint = vQ
        self.Uvec = vU
        self.Vvec = vV
        self.material = mMat
        self.normal = rtu.Vec3.unit_vector(rtu.Vec3.cross_product(self.Uvec, self.Vvec))
        self.D = rtu.Vec3.dot_product(self.normal, self.Qpoint)
        self.Wvec = self.normal / rtu.Vec3.dot_product(self.normal, self.normal)

    def add_material(self, mMat):
        self.material = mMat

    def intersect(self, vRay, cInterval):
        super().intersect(vRay, cInterval)

        denom = rtu.Vec3.dot_product(self.normal, vRay.getDirection())
        # if parallel
        if rtu.Interval.near_zero(denom):
            return None

        # if it is hit.
        t = (self.D - rtu.Vec3.dot_product(self.normal, vRay.getOrigin())) / denom
        if not cInterval.contains(t):
            return None
        
        hit_t = t
        hit_point = vRay.at(t)
        hit_normal = self.normal

        # determine if the intersection point lies on the quad's plane.
        planar_hit = hit_point - self.Qpoint
        alpha = rtu.Vec3.dot_product(self.Wvec, rtu.Vec3.cross_product(planar_hit, self.Vvec))
        beta = rtu.Vec3.dot_product(self.Wvec, rtu.Vec3.cross_product(self.Uvec, planar_hit))
        if self.is_interior(alpha, beta):
            return None

        hinfo = rtu.Hitinfo(hit_point, hit_normal, hit_t, self.material)
        hinfo.set_face_normal(vRay, hit_normal)
        return hinfo


    def is_interior(self, fa, fb):        
        if fa<0 or 1.0<fa or fb<0 or 1.0<fb:
            return None

        return rtt.TextureCoord(fa, fb)
    
class Triangle(Object):
    def __init__(self) -> None:
        super().__init__()

    def intersect(self, vRay, cInterval):
        return super().intersect(vRay, cInterval)
    

    