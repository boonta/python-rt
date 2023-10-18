# material class
import RT_utility as rtu
import RT_ray as rtr
import math

def reflect(vRay, vNormal):
    return vRay - vNormal*rtu.Vec3.dot_product(vRay, vNormal)*2.0

def refract(vRay, vNormal, fRefractRatio):
    cos_theta = min(rtu.Vec3.dot_product(-vRay, vNormal), 1.0)
    sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)
    cannot_refract = fRefractRatio*sin_theta > 1.0

    if cannot_refract or schlick(cos_theta, fRefractRatio) > rtu.random_double():
        return reflect(vRay, vNormal)
    else:
        perpendiular_dir = (vRay + vNormal*cos_theta)*fRefractRatio
        parallel_dir = vNormal*(-math.sqrt(math.fabs(1.0 - perpendiular_dir.len_squared())))
        return perpendiular_dir + parallel_dir

def schlick(fCosine, fIOR):
    r0 = (1-fIOR) / (1+fIOR)
    r0 = r0*r0
    return r0 + (1-r0)*math.pow(1-fCosine, 5)


class Material:
    def __init__(self) -> None:
        pass

    # def scattering(self, rRayIn, vPoint, vNormal):
    #     pass

    def scattering(self, rRayIn, hHinfo):
        pass

class Lambertian(Material):
    def __init__(self, cAlbedo) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())

    def scattering(self, rRayIn, hHinfo):
        scattered_direction = hHinfo.getNormal() + rtu.Vec3.random_vec3_unit()
        if scattered_direction.near_zero():
            scattered_direction = hHinfo.getNormal()

        scattered_ray = rtr.Ray(hHinfo.getP(), scattered_direction)
        attenuation_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())
        return rtu.Scatterinfo(scattered_ray, attenuation_color)

class Mirror(Material):
    def __init__(self, cAlbedo) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())

    def scattering(self, rRayIn, hHinfo):
        # reflected_ray = rtr.Ray(hHinfo.getP(), self.reflect(rRayIn, hHinfo.getNormal()))
        reflected_ray = rtr.Ray(hHinfo.getP(), reflect(rRayIn.getDirection(), hHinfo.getNormal()))
        attenuation_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())

        return rtu.Scatterinfo(reflected_ray, attenuation_color)


class Metal(Material):
    def __init__(self, cAlbedo, fRoughness) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())
        self.roughness = fRoughness
        if self.roughness > 1.0:
            self.roughness = 1.0

    def scattering(self, rRayIn, hHinfo):
        # reflected_direction = self.reflect(rRayIn, hHinfo.getNormal()) + rtu.Vec3.random_vec3_unit()*self.roughness
        reflected_direction = reflect(rRayIn.getDirection(), hHinfo.getNormal()) + rtu.Vec3.random_vec3_unit()*self.roughness
        reflected_ray = rtr.Ray(hHinfo.getP(), reflected_direction)
        attenuation_color = rtu.Color(self.color_albedo.r(), self.color_albedo.g(), self.color_albedo.b())

        # check if the reflected direction is below the surface normal
        if rtu.Vec3.dot_product(reflected_direction, hHinfo.getNormal()) <= 1e-8:
            attenuation_color = rtu.Color(0,0,0)

        return rtu.Scatterinfo(reflected_ray, attenuation_color)



class Dielectric(Material):
    def __init__(self, cAlbedo, fIor) -> None:
        super().__init__()
        self.color_albedo = rtu.Color(cAlbedo.r(), cAlbedo.g(), cAlbedo.b())
        self.IOR = fIor

    def scattering(self, rRayIn, hHinfo):
        attenuation_color = self.color_albedo
        refract_ratio = self.IOR
        if hHinfo.front_face:
            refract_ratio = 1.0/self.IOR

        uv = rtu.Vec3.unit_vector(rRayIn.getDirection())
        # refracted_dir = self.refract(uv, hHinfo.getNormal(), refract_ratio)
        refracted_dir = refract(uv, hHinfo.getNormal(), refract_ratio)
        scattered_ray = rtr.Ray(hHinfo.getP(), refracted_dir)

        return rtu.Scatterinfo(scattered_ray, attenuation_color)



