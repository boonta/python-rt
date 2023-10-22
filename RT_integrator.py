# integrator class such as whitted ray tracing / path tracing
# It is the rendering equation solver.
import RT_utility as rtu
import RT_ray as rtr


class Integrator():
    def __init__(self) -> None:
        pass

    def compute_scattering(self, rGen_ray, maxDepth, scene):
        pass


class Whitted():
    def __init__(self) -> None:
        pass


class PathTracing():
    def __init__(self) -> None:
        pass

    def compute_scattering(self, rGen_ray, maxDepth, scene):

        if maxDepth <= 0:
            return rtu.Color()

        found_hit = scene.find_intersection(rGen_ray, rtu.Interval(0.000001, rtu.infinity_number))
        if found_hit == True:
            hinfo = scene.getHitList()
            hmat = hinfo.getMaterial()
            sinfo = hmat.scattering(rGen_ray, hinfo)

            return self.compute_scattering(rtr.Ray(hinfo.getP(), sinfo.scattered_ray.getDirection()), maxDepth-1, scene) * sinfo.attenuation_color

        return self.background_color(rGen_ray)

    def background_color(self, rGen_ray):
        unit_direction = rtu.Vec3.unit_vector(rGen_ray.getDirection())
        a = (unit_direction.y() + 1.0)*0.5
        return rtu.Color(1,1,1)*(1.0-a) + rtu.Color(0.5, 0.7, 1.0)*a

    def get_color(self, rGen_ray, scene):

        found_hit = scene.find_intersection(rGen_ray, rtu.Interval(0.000001, rtu.infinity_number))
        if found_hit == True:
            tmpN = scene.getHitList().getNormal()
            return (rtu.Color(tmpN.x(), tmpN.y(), tmpN.z()) + rtu.Color(1,1,1))*0.5

        return self.background_color(rGen_ray)
