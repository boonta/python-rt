# renderer class

import RT_integrator as rti
import RT_utility as rtu
import numpy as np
from PIL import Image as im

class Renderer():

    def __init__(self, cCamera, iIntegrator, sScene) -> None:

        self.camera = cCamera
        self.integrator = iIntegrator
        self.scene = sScene
        pass

    def render(self):
        # gather lights to the light list
        self.scene.find_lights()
        
        for j in range(self.camera.img_height):
            for i in range(self.camera.img_width):

                pixel_color = rtu.Color(0,0,0)
                for ssp in range(self.camera.samples_per_pixel):
                    generated_ray = self.camera.get_ray(i, j)
                    pixel_color = pixel_color + self.integrator.compute_scattering(generated_ray, self.scene, self.camera.max_depth)

                self.camera.write_to_film(i, j, pixel_color)


    def write_img2png(self, strPng_filename):
        png_film = self.camera.film * 255
        data = im.fromarray(png_film.astype(np.uint8))
        data.save(strPng_filename)

