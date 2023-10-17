# material class
import RT_utility as rtu
import RT_ray as rtr

class Material:
    def __init__(self) -> None:
        pass

    def scattering(self, vRayIn, vPoint, vNormal):
        pass

class Lambertian(Material):
    def __init__(self, cAlbedo) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())

    def scattering(self):
        return super().scattering()
    
    def scattering(self, vRayIn, vPoint, vNormal):
        scattered_direction = vNormal + rtu.Vec3.random_vec3_unit()
        if scattered_direction.near_zero():
            scattered_direction = vNormal

        scattered_ray = rtr.Ray(vPoint, scattered_direction)
        attenuation_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())
        return rtu.Scatterinfo(scattered_ray, attenuation_color)
    
class Mirror(Material):
    def __init__(self, cAlbedo) -> None:
        super().__init__()

class Metal(Material):
    def __init__(self, cAlbedo, fRoughness) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())
        self.roughness = fRoughness

    def scattering(self):
        return super().scattering()
    
    def scattering(self, vRayIn, vPoint, vNormal):
        pass
