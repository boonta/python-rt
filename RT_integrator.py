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
    def __init__(self, bDlight=True) -> None:
        self.bool_direct_lighting = bDlight
        pass

    def compute_scattering(self, rGen_ray, scene, maxDepth):

        if maxDepth <= 0:
            return rtu.Color()

        found_hit = scene.find_intersection(rGen_ray, rtu.Interval(0.000001, rtu.infinity_number))
        if found_hit == True:
            hinfo = scene.getHitList()
            hmat = hinfo.getMaterial()
            sinfo = hmat.scattering(rGen_ray, hinfo)
            if sinfo is None:   # if no scattering (light)
                return hmat.emitting()  # emit the light color

            Le = rtu.Color()
            if self.bool_direct_lighting:
                for light in scene.point_light_list:    # for now handle only point lights
                    tolight_dir = light.center - hinfo.getP()
                    tolight_ray = rtr.Ray(hinfo.getP(), tolight_dir)
                    max_distance = tolight_dir.len()
                    occlusion_hit = scene.find_occlusion(tolight_ray, rtu.Interval(0.000001, max_distance))
                    # if not occluded.
                    if not occlusion_hit:
                        # accumulate all unoccluded light
                        Le = Le + (light.material.emitting() * (1/max_distance))

            return Le + self.compute_scattering(rtr.Ray(hinfo.getP(), sinfo.scattered_ray.getDirection()), scene, maxDepth-1) * sinfo.attenuation_color

        return scene.getBackgroundColor()

    # def background_color(self, rGen_ray):
    #     unit_direction = rtu.Vec3.unit_vector(rGen_ray.getDirection())
    #     a = (unit_direction.y() + 1.0)*0.5
    #     return rtu.Color(1,1,1)*(1.0-a) + rtu.Color(0.5, 0.7, 1.0)*a

    # def get_color(self, rGen_ray, scene):

    #     found_hit = scene.find_intersection(rGen_ray, rtu.Interval(0.000001, rtu.infinity_number))
    #     if found_hit == True:
    #         tmpN = scene.getHitList().getNormal()
    #         return (rtu.Color(tmpN.x(), tmpN.y(), tmpN.z()) + rtu.Color(1,1,1))*0.5

    #     return self.background_color(rGen_ray)
