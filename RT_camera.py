# Camera class

import RT_utility as rtu
import RT_ray as rtr

import numpy as np
from PIL import Image as im

class Camera:
    def __init__(self) -> None:
        self.img_spectrum = 3
        self.aspect_ratio = 16.0/9.0
        self.focal_length = 1.0
        self.img_width = 400
        self.viewport_height = 2.0
        self.center = rtu.Vec3()
        self.intensity = rtu.Interval(0.000, 0.999)
        self.samples_per_pixel = 10
        self.max_depth = 2

        self.init_camera()
        
        pass

    def compute_img_height(self):
        h = int(self.img_width / self.aspect_ratio)
        return  h if h > 1 else 1
    
    def compute_viewport_width(self):
        vp_width = self.viewport_height * float(self.img_width/self.img_height)
        return vp_width

    def init_camera(self):
        self.img_height = self.compute_img_height()
        self.viewport_width = self.compute_viewport_width()
        self.viewport_u = rtu.Vec3(self.viewport_width, 0, 0)
        self.viewport_v = rtu.Vec3(0, -self.viewport_height, 0)
        self.pixel_du = self.viewport_u / self.img_width
        self.pixel_dv = self.viewport_v / self.img_height
        self.viewport_upper_left = self.center - rtu.Vec3(0, 0, self.focal_length) - self.viewport_u/2 - self.viewport_v/2
        self.pixel00_location = self.viewport_upper_left + (self.pixel_du+self.pixel_dv)*0.5
        self.film = np.zeros((self.img_height, self.img_width, self.img_spectrum))


    def write_to_film(self, widthId, heightId, cPixelColor):
        scale = 1/self.samples_per_pixel
        r = cPixelColor.r()*scale
        g = cPixelColor.g()*scale
        b = cPixelColor.b()*scale

        r = rtu.linear_to_gamma(r, 2.0)
        g = rtu.linear_to_gamma(g, 2.0)
        b = rtu.linear_to_gamma(b, 2.0)

        self.film[heightId,widthId,0] = self.intensity.clamp(r)
        self.film[heightId,widthId,1] = self.intensity.clamp(g)
        self.film[heightId,widthId,2] = self.intensity.clamp(b)


    def write_img(self, strPng_filename):
        png_film = self.film * 255
        data = im.fromarray(png_film.astype(np.uint8))
        data.save(strPng_filename)

    def get_center_ray(self, i, j):
        pixel_center = self.pixel00_location + (self.pixel_du*i) + (self.pixel_dv*j)
        ray_direction = pixel_center - self.center
        return rtr.Ray(self.center, ray_direction)

    def get_ray(self, i, j):
        pixel_center = self.pixel00_location + (self.pixel_du*i) + (self.pixel_dv*j)
        pixel_sample = pixel_center + self.random_pixel_in_square(self.pixel_du, self.pixel_dv)
        ray_direction = pixel_sample - self.center
        return rtr.Ray(self.center, ray_direction)

    def random_pixel_in_square(self, vDu, vDv):
        px = -0.5 + rtu.random_double()
        py = -0.5 + rtu.random_double()
        return (vDu*px) + (vDv*py)

    def render(self, scene):

        for j in range(self.img_height):
            for i in range(self.img_width):

                # generated_ray = self.get_center_ray(i, j)
                # pixel_color = self.get_color(generated_ray, scene)

                pixel_color = rtu.Color(0,0,0)
                for ssp in range(self.samples_per_pixel):
                    generated_ray = self.get_ray(i, j)
                    # pixel_color = pixel_color + self.get_color(generated_ray, scene)
                    pixel_color = pixel_color + self.compute_scattering(generated_ray, self.max_depth, scene)


                self.write_to_film(i, j, pixel_color)
        pass

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

    # def compute_scattering(self, rGen_ray, maxDepth, scene):

    #     if maxDepth <= 0:
    #         return rtu.Color()

    #     found_hit = scene.find_intersection(rGen_ray, rtu.Interval(0, rtu.infinity_number))
    #     if found_hit == True:
    #         hinfo = scene.getHitList()
    #         scattered_direction = rtu.Vec3.random_vec3_on_hemisphere(hinfo.getNormal())

    #         return self.compute_scattering(rtr.Ray(hinfo.getP(), scattered_direction), maxDepth-1, scene) *0.1

    #     return self.background_color(rGen_ray)

    def compute_scattering(self, rGen_ray, maxDepth, scene):

        if maxDepth <= 0:
            return rtu.Color()

        found_hit = scene.find_intersection(rGen_ray, rtu.Interval(0.000001, rtu.infinity_number))
        if found_hit == True:
            hinfo = scene.getHitList()
            hmat = hinfo.getMaterial()
            sinfo = hmat.scattering(rGen_ray, hinfo.getP(), hinfo.getNormal())

            return self.compute_scattering(rtr.Ray(hinfo.getP(), sinfo.scattered_ray.getDirection()), maxDepth-1, scene) * sinfo.attenuation_color

        return self.background_color(rGen_ray)

