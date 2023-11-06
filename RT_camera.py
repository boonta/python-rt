# Camera class

import RT_utility as rtu
import RT_ray as rtr

import numpy as np
import math
from PIL import Image as im

class Camera:
    def __init__(self) -> None:
        self.img_spectrum = 3
        self.aspect_ratio = 16.0/9.0
        # self.focal_length = 1.0
        self.img_width = 400
        self.center = rtu.Vec3()
        self.intensity = rtu.Interval(0.000, 0.999)
        self.samples_per_pixel = 10
        self.max_depth = 4
        self.vertical_fov = 90
        self.look_from = rtu.Vec3(0, 0, -1)
        self.look_at = rtu.Vec3(0, 0, 0)
        self.vec_up = rtu.Vec3(0, 1, 0)

        
        self.init_camera()
        

        pass

    def compute_img_height(self):
        h = int(self.img_width / self.aspect_ratio)
        return  h if h > 1 else 1
    
    def compute_viewport_width(self):
        vp_width = self.viewport_height * float(self.img_width/self.img_height)
        return vp_width

    def init_camera(self,fDefocusAngle=0.0, fFocusDist=10.0):
        self.set_Lens(fDefocusAngle, fFocusDist)

        self.img_height = self.compute_img_height()
        # self.focal_length = (self.look_from - self.look_at).len()
        self.center = self.look_from

        h = math.tan(math.radians(self.vertical_fov)/2.0)
        # self.viewport_height = 2.0 * h * self.focal_length
        self.viewport_height = 2.0 * h * self.Lens.get_focus_dist()
        self.viewport_width = self.compute_viewport_width()

        self.camera_frame_w = rtu.Vec3.unit_vector(self.look_from - self.look_at)
        self.camera_frame_u = rtu.Vec3.unit_vector(rtu.Vec3.cross_product(self.vec_up, self.camera_frame_w))
        self.camera_frame_v = rtu.Vec3.cross_product(self.camera_frame_w, self.camera_frame_u)

        # self.viewport_u = rtu.Vec3(self.viewport_width, 0, 0)
        # self.viewport_v = rtu.Vec3(0, -self.viewport_height, 0)
        self.viewport_u = self.camera_frame_u*self.viewport_width
        self.viewport_v = -self.camera_frame_v*self.viewport_height
        self.pixel_du = self.viewport_u / self.img_width
        self.pixel_dv = self.viewport_v / self.img_height
        # self.viewport_upper_left = self.center - rtu.Vec3(0, 0, self.focal_length) - self.viewport_u/2 - self.viewport_v/2
        self.viewport_upper_left = self.center - (self.camera_frame_w*self.Lens.get_focus_dist()) - self.viewport_u/2 - self.viewport_v/2
        self.pixel00_location = self.viewport_upper_left + (self.pixel_du+self.pixel_dv)*0.5
        self.film = np.zeros((self.img_height, self.img_width, self.img_spectrum))

        self.set_Lens_frame()

    # call right before init_camera()
    def set_Lens(self, fDefocusAngle, fFocusDist):
        self.Lens = Thinlens(fDefocusAngle, fFocusDist)

    # call right after init_camera()
    def set_Lens_frame(self):
        self.Lens.compute_defocus_disk(self.camera_frame_u, self.camera_frame_v)

    def write_to_film(self, widthId, heightId, cPixelColor):
        scale = 1/self.samples_per_pixel
        r = cPixelColor.r()*scale
        g = cPixelColor.g()*scale
        b = cPixelColor.b()*scale

        r = rtu.linear_to_gamma(r, 1.8)
        g = rtu.linear_to_gamma(g, 1.8)
        b = rtu.linear_to_gamma(b, 1.8)

        self.film[heightId,widthId,0] = self.intensity.clamp(r)
        self.film[heightId,widthId,1] = self.intensity.clamp(g)
        self.film[heightId,widthId,2] = self.intensity.clamp(b)

    def get_center_ray(self, i, j):
        pixel_center = self.pixel00_location + (self.pixel_du*i) + (self.pixel_dv*j)
        ray_direction = pixel_center - self.center
        return rtr.Ray(self.center, ray_direction)

    def get_ray(self, i, j):
        pixel_center = self.pixel00_location + (self.pixel_du*i) + (self.pixel_dv*j)
        pixel_sample = pixel_center + self.random_pixel_in_square(self.pixel_du, self.pixel_dv)

        ray_origin = self.center
        if self.Lens.get_defocus_angle() > 0:
            ray_origin = self.Lens.random_in_lens(self.center)
        ray_direction = pixel_sample - ray_origin

        return rtr.Ray(ray_origin, ray_direction)

    def random_pixel_in_square(self, vDu, vDv):
        px = -0.5 + rtu.random_double()
        py = -0.5 + rtu.random_double()
        return (vDu*px) + (vDv*py)

    # def render(self, scene):

    #     for j in range(self.img_height):
    #         for i in range(self.img_width):

    #             # generated_ray = self.get_center_ray(i, j)
    #             # pixel_color = self.get_color(generated_ray, scene)

    #             pixel_color = rtu.Color(0,0,0)
    #             for ssp in range(self.samples_per_pixel):
    #                 generated_ray = self.get_ray(i, j)
    #                 # pixel_color = pixel_color + self.get_color(generated_ray, scene)
    #                 pixel_color = pixel_color + self.compute_scattering(generated_ray, self.max_depth, scene)


    #             self.write_to_film(i, j, pixel_color)
    #     pass

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

    # # def compute_scattering(self, rGen_ray, maxDepth, scene):

    # #     if maxDepth <= 0:
    # #         return rtu.Color()

    # #     found_hit = scene.find_intersection(rGen_ray, rtu.Interval(0, rtu.infinity_number))
    # #     if found_hit == True:
    # #         hinfo = scene.getHitList()
    # #         scattered_direction = rtu.Vec3.random_vec3_on_hemisphere(hinfo.getNormal())

    # #         return self.compute_scattering(rtr.Ray(hinfo.getP(), scattered_direction), maxDepth-1, scene) *0.1

    # #     return self.background_color(rGen_ray)

    # def compute_scattering(self, rGen_ray, maxDepth, scene):

    #     if maxDepth <= 0:
    #         return rtu.Color()

    #     found_hit = scene.find_intersection(rGen_ray, rtu.Interval(0.000001, rtu.infinity_number))
    #     if found_hit == True:
    #         hinfo = scene.getHitList()
    #         hmat = hinfo.getMaterial()
    #         sinfo = hmat.scattering(rGen_ray, hinfo)

    #         return self.compute_scattering(rtr.Ray(hinfo.getP(), sinfo.scattered_ray.getDirection()), maxDepth-1, scene) * sinfo.attenuation_color

    #     return self.background_color(rGen_ray)


class Lens():
    def __init__(self) -> None:
        pass

class Thinlens(Lens):
    def __init__(self, fDefocusAngle=0.0, fFocusDist=10.0) -> None:
        super().__init__()

        self.defocus_angle = fDefocusAngle
        self.focus_distance = fFocusDist
        self.set_defocus_radius()
        pass

    def set_defocus_radius(self):
        self.defocus_radius = self.focus_distance*math.tan(math.radians(self.defocus_angle/2.0))

    def compute_defocus_disk(self, vU, vV):
        self.defocus_disk_u = vU*self.defocus_radius
        self.defocus_disk_v = vV*self.defocus_radius

    def random_in_lens(self, cameraCenter):
        p = rtu.Vec3.random_vec3_in_unit_disk()
        return cameraCenter + (self.defocus_disk_u*p.x()) + (self.defocus_disk_v*p.y())

    def get_focus_dist(self):
        return self.focus_distance
    def get_defocus_angle(self):
        return self.defocus_angle
    def get_defocus_disk_u(self):
        return self.defocus_disk_u
    def get_defocus_disk_v(self):
        return self.defocus_disk_v
    