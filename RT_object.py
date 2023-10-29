# object class
import RT_ray as rtr
import RT_utility as rtu
import RT_material as rtm
import RT_texture as rtt
import math

class Object:
    def __init__(self) -> None:
        pass

    def intersect(self, rRay):
        pass

    def intersect(self, rRay, tmin, tmax):
        pass

    def intersect(self, rRay, cInterval):
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
        

    def intersect(self, rRay):
        oc = rRay.getOrigin() - self.center
        a = rtu.Vec3.dot_product(rRay.getDirection(), rRay.getDirection())
        b = 2.0 * rtu.Vec3.dot_product(oc, rRay.getDirection())
        c = rtu.Vec3.dot_product(oc, oc) - self.radius*self.radius
        discriminant = b*b - 4*a*c 

        if discriminant < 0:
            return -1.0
        else:
            return (-b -math.sqrt(discriminant)) / (2.0*a)

    def intersect(self, rRay, tmin, tmax):

        if tmin < 0:
            return None
        
        oc = rRay.getOrigin() - self.center
        a = rRay.getDirection().len_squared()
        half_b = rtu.Vec3.dot_product(oc, rRay.getDirection())
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
        hit_point = rRay.at(root)
        hit_normal = (hit_point - self.center) / self.radius
        hinfo = rtu.Hitinfo(hit_point, hit_normal, hit_t, self.material)

        hinfo.set_face_normal(rRay, hit_normal) 
        return hinfo
    
    # main intersection calling
    def intersect(self, rRay, cInterval):
        
        oc = rRay.getOrigin() - self.center
        a = rRay.getDirection().len_squared()
        half_b = rtu.Vec3.dot_product(oc, rRay.getDirection())
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
        hit_point = rRay.at(root)
        hit_normal = (hit_point - self.center) / self.radius
        hinfo = rtu.Hitinfo(hit_point, hit_normal, hit_t, self.material)

        hinfo.set_face_normal(rRay, hit_normal) 
        return hinfo

# Ax + By + Cz = D
class Quad(Object):
    def __init__(self, vQ, vU, vV, mMat=None) -> None:
        super().__init__()
        self.Qpoint = vQ
        self.Uvec = vU
        self.Vvec = vV
        self.material = mMat
        self.uxv = rtu.Vec3.cross_product(self.Uvec, self.Vvec)
        self.normal = rtu.Vec3.unit_vector(self.uxv)
        self.D = rtu.Vec3.dot_product(self.normal, self.Qpoint)
        self.Wvec = self.uxv / rtu.Vec3.dot_product(self.uxv, self.uxv)

    def add_material(self, mMat):
        self.material = mMat

    def intersect(self, rRay, cInterval):

        # for aabb method
        # if not self.is_in_boundary(rRay, cInterval):
        #     return None

        denom = rtu.Vec3.dot_product(self.normal, rRay.getDirection())
        # if parallel
        if rtu.Interval.near_zero(denom):
            return None

        # if it is hit.
        t = (self.D - rtu.Vec3.dot_product(self.normal, rRay.getOrigin())) / denom
        if not cInterval.contains(t):
            return None
        
        hit_t = t
        hit_point = rRay.at(t)
        hit_normal = self.normal
        # if not self.is_in_plane(hit_point):
        #     return None

        # determine if the intersection point lies on the quad's plane.
        planar_hit = hit_point - self.Qpoint
        alpha = rtu.Vec3.dot_product(self.Wvec, rtu.Vec3.cross_product(planar_hit, self.Vvec))
        beta = rtu.Vec3.dot_product(self.Wvec, rtu.Vec3.cross_product(self.Uvec, planar_hit))
        if self.is_interior(alpha, beta) is None:
            return None

        hinfo = rtu.Hitinfo(hit_point, hit_normal, hit_t, self.material)
        hinfo.set_face_normal(rRay, hit_normal)
        return hinfo

    def is_interior(self, fa, fb):
        delta = 0   
        if (fa<delta) or (1.0<fa) or (fb<delta) or (1.0<fb):
            return None

        return rtt.TextureCoord(fa, fb)

    # check if the hit ray is in the defined plane.
    def is_in_plane(self, vHitPoint):

        box0 = self.Qpoint
        box1 = self.Qpoint + self.Uvec + self.Vvec
        x = rtu.Interval(min(box0.x(), box1.x()), max(box0.x(), box1.x()))
        y = rtu.Interval(min(box0.y(), box1.y()), max(box0.y(), box1.y()))
        z = rtu.Interval(min(box0.z(), box1.z()), max(box0.z(), box1.z()))
        delta = 1e-08
        if x.size() < delta:
            padding = delta/2.0
            x = rtu.Interval(x.min_val-padding, x.max_val+padding)
        if y.size() < delta:
            padding = delta/2.0
            y = rtu.Interval(y.min_val-padding, y.max_val+padding)
        if z.size() < delta:
            padding = delta/2.0
            z = rtu.Interval(z.min_val-padding, z.max_val+padding)        
        if not x.contains(vHitPoint.x()):
            return False
        if not y.contains(vHitPoint.y()):
            return False
        if not z.contains(vHitPoint.z()):
            return False

        return True

    # an aabb intersection method
    def is_in_boundary(self, rRay, iRayt):

        box0 = self.Qpoint
        box1 = self.Qpoint + self.Uvec + self.Vvec
        x = rtu.Interval(min(box0.x(), box1.x()), max(box0.x(), box1.x()))
        y = rtu.Interval(min(box0.y(), box1.y()), max(box0.y(), box1.y()))
        z = rtu.Interval(min(box0.z(), box1.z()), max(box0.z(), box1.z()))

        delta = 1e-08
        if x.size() < delta:
            padding = delta/2.0
            x = rtu.Interval(x.min_val-padding, x.max_val+padding)
        if y.size() < delta:
            padding = delta/2.0
            y = rtu.Interval(y.min_val-padding, y.max_val+padding)
        if z.size() < delta:
            padding = delta/2.0
            z = rtu.Interval(z.min_val-padding, z.max_val+padding)

        # X axis boundary
        ftmin = (x.min_val - rRay.getOrigin().x())/rRay.getDirection().x()
        ftmax = (x.max_val - rRay.getOrigin().x())/rRay.getDirection().x()
        t0 = min(ftmin, ftmax)
        t1 = max(ftmin, ftmax)

        iRayt.min_val = max(t0, iRayt.min_val)
        iRayt.max_val = min(t1, iRayt.max_val)
        if iRayt.max_val <= iRayt.min_val:
            return False

        # Y axis boundary
        ftmin = (y.min_val - rRay.getOrigin().y())/rRay.getDirection().y()
        ftmax = (y.max_val - rRay.getOrigin().y())/rRay.getDirection().y()
        t0 = min(ftmin, ftmax)
        t1 = max(ftmin, ftmax)

        iRayt.min_val = max(t0, iRayt.min_val)
        iRayt.max_val = min(t1, iRayt.max_val)
        if iRayt.max_val <= iRayt.min_val:
            return False

        # Z axis boundary
        ftmin = (z.min_val - rRay.getOrigin().z())/rRay.getDirection().z()
        ftmax = (z.max_val - rRay.getOrigin().z())/rRay.getDirection().z()
        t0 = min(ftmin, ftmax)
        t1 = max(ftmin, ftmax)

        iRayt.min_val = max(t0, iRayt.min_val)
        iRayt.max_val = min(t1, iRayt.max_val)
        if iRayt.max_val <= iRayt.min_val:
            return False

        return True

class Triangle(Object):
    def __init__(self) -> None:
        super().__init__()

    def intersect(self, rRay, cInterval):
        return super().intersect(rRay, cInterval)
    

    