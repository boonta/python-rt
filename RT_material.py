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
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())
        
    def scattering(self, vRayIn, vPoint, vNormal):
        reflected_ray = rtr.Ray(vPoint, self.reflect(vRayIn, vNormal))
        attenuation_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())

        return rtu.Scatterinfo(reflected_ray, attenuation_color)
    
    def reflect(self, vRayIn, vNormal):
        return vRayIn.getDirection() - vNormal*rtu.Vec3.dot_product(vRayIn.getDirection(), vNormal)*2.0


class Metal(Material):
    def __init__(self, cAlbedo, fRoughness) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())
        self.roughness = fRoughness
        if self.roughness > 1.0:
            self.roughness = 1.0

    
    def scattering(self, vRayIn, vPoint, vNormal):
        reflected_direction = self.reflect(vRayIn, vNormal) + rtu.Vec3.random_vec3_unit()*self.roughness
        reflected_ray = rtr.Ray(vPoint, reflected_direction)
        attenuation_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())

        # check if the reflected direction is below the surface normal
        if rtu.Vec3.dot_product(reflected_direction, vNormal) <= 1e-8:
            attenuation_color = rtu.Color(0,0,0)

        return rtu.Scatterinfo(reflected_ray, attenuation_color)
    
    def reflect(self, vRayIn, vNormal):
        return vRayIn.getDirection() - vNormal*rtu.Vec3.dot_product(vRayIn.getDirection(), vNormal)*2.0


