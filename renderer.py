import RT_utility as rtu
import RT_ray as rtr
import RT_camera as rtc
import RT_object as rto
import RT_scene as rts
import RT_material as rtm

def background_color(rGen_ray):
    unit_direction = rtu.Vec3.unit_vector(rGen_ray.getDirection())
    a = (unit_direction.y() + 1.0)*0.5
    return rtu.Color(1,1,1)*(1.0-a) + rtu.Color(0.5, 0.7, 1.0)*a

def get_color(rGen_ray, scene):

    found_hit = scene.find_intersection(rGen_ray, rtu.Interval(0, rtu.infinity_number))
    if found_hit == True:
        tmpN = scene.getHitList().getNormal()
        return (rtu.Color(tmpN.x(), tmpN.y(), tmpN.z()) + rtu.Color(1,1,1))*0.5

    return background_color(rGen_ray)

def render():
    main_camera = rtc.Camera()
    main_camera.aspect_ratio = 16.0/9.0
    main_camera.img_width = 400
    # main_camera.focal_length = 1.0
    main_camera.center = rtu.Vec3(0,0,0)
    main_camera.samples_per_pixel = 50
    main_camera.max_depth = 7
    main_camera.vertical_fov = 20
    main_camera.look_from = rtu.Vec3(-2, 2, 1)
    main_camera.look_at = rtu.Vec3(0, 0, -1)
    main_camera.vec_up = rtu.Vec3(0, 1, 0)

    defocus_angle = 10.0
    focus_distance = 3.4
    # add objects to the scene

    mat_ground = rtm.Lambertian(rtu.Color(0.8, 0.8, 0.0))
    mat_center = rtm.Lambertian(rtu.Color(0.7, 0.3, 0.3))
    mat_glass1 = rtm.Mirror(rtu.Color(0.8, 0.8, 0.8))
    mat_glass2 = rtm.Metal(rtu.Color(0.8, 0.6, 0.2), 0.5)
    mat_dielect1 = rtm.Dielectric(rtu.Color(1.0, 1.0, 1.0), 1.5)

    world = rts.Scene()
    world.add_object(rto.Sphere(rtu.Vec3(   0,-100.5,-1),  100, mat_ground))
    world.add_object(rto.Sphere(rtu.Vec3(   0,   0.0,-1),  0.5, mat_center))
    world.add_object(rto.Sphere(rtu.Vec3(-1.0,   0.0,-1),  0.5, mat_dielect1))
    world.add_object(rto.Sphere(rtu.Vec3(-1.0,   0.0,-1), -0.4, mat_dielect1))
    world.add_object(rto.Sphere(rtu.Vec3( 1.0,   0.0,-1),  0.5, mat_glass1))

    main_camera.init_camera(defocus_angle, focus_distance)
    main_camera.render(world)
    main_camera.write_img('test_renderer11.png')


if __name__ == "__main__":
    render()


