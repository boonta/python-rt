import RT_utility as rtu
import RT_ray as rtr
import RT_camera as rtc
import RT_object as rto
import RT_scene as rts
import RT_material as rtm
import RT_integrator as rti
import RT_renderer as rtren


def render():
    main_camera = rtc.Camera()
    main_camera.aspect_ratio = 16.0/9.0
    main_camera.img_width = 400
    main_camera.center = rtu.Vec3(0,0,0)
    main_camera.samples_per_pixel = 50
    main_camera.max_depth = 7
    main_camera.vertical_fov = 20
    main_camera.look_from = rtu.Vec3(-2, 2, 1)
    main_camera.look_at = rtu.Vec3(0, 0, -1)
    main_camera.vec_up = rtu.Vec3(0, 1, 0)

    defocus_angle =0.0
    focus_distance = 10.0
    main_camera.init_camera(defocus_angle, focus_distance)
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

    pathtracing = rti.PathTracing()
    pathRenderer = rtren.Renderer(main_camera, pathtracing, world)

    pathRenderer.render()
    pathRenderer.write_img2png('test_renderer13.png')


if __name__ == "__main__":
    render()


