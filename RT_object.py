# object class
import RT_ray as rtr
import RT_utility as rtu

class Object:
    def __init__(self) -> None:
        pass

    def intersect(self, vRay):
        pass

class Sphere(Object):
    def __init__(self, vCenter, fRadius) -> None:
        super().__init__()
        self.center = vCenter
        self.radius = fRadius

    def intersect(self, vRay):
        oc = vRay.getOrigin() - self.center
        a = rtu.Vec3.dot_product(vRay.getDirection(), vRay.getDirection())
        b = 2.0 * rtu.Vec3.dot_product(oc, vRay.getDirection())
        c = rtu.Vec3.dot_product(oc, oc) - self.radius*self.radius
        discriminant = b*b - 4*a*c 
        return discriminant >= 0

