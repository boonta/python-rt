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


    def write_img(self, strPng_filename):
        png_film = self.film * 255
        data = im.fromarray(png_film.astype(np.uint8))
        data.save(strPng_filename)

