import RT_utility as rtu
import RT_ray as rtr
import RT_camera as rtc
import RT_object as rto
import RT_scene as rts

def background_color(rGen_ray):
    unit_direction = rtu.Vec3.unit_vector(rGen_ray.getDirection())
    a = (unit_direction.y() + 1.0)*0.5
    return rtu.Color(1,1,1)*(1.0-a) + rtu.Color(0.5, 0.7, 1.0)*a

# def get_color(rGen_ray, scene):

#     found_hit = scene.find_intersection(rGen_ray, 0, rtu.infinity_number)
#     if found_hit == True:
#         tmpN = scene.getHitList().getNormal()
#         return (rtu.Color(tmpN.x(), tmpN.y(), tmpN.z()) + rtu.Color(1,1,1))*0.5

#     return background_color(rGen_ray)

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
    main_camera.focal_length = 1.0
    main_camera.viewport_height = 2.0
    main_camera.center = rtu.Vec3(0,0,0)

    # add objects to the scene
    # obj_s1 = rto.Sphere(rtu.Vec3(0,0,-1), 0.5)

    world = rts.Scene()
    world.add_object(rto.Sphere(rtu.Vec3(0,0,-1), 0.5))
    world.add_object(rto.Sphere(rtu.Vec3(0,-100.5,-1), 100))


    for j in range(main_camera.img_height):
        for i in range(main_camera.img_width):
            pixel_center = main_camera.pixel00_location + (main_camera.pixel_du*i) + (main_camera.pixel_dv*j)
            ray_direction = pixel_center - main_camera.center
            generated_ray = rtr.Ray(main_camera.center, ray_direction)

            # pixel_color = background_color(generated_ray)

            # # for each object in the scene
            # # compute intersection information
            # t = obj_s1.intersect(generated_ray)
            # if t > 0.0:
            #     vNormal = rtu.Vec3.unit_vector(generated_ray.at(t) - rtu.Vec3(0,0,-1))
            #     pixel_color = rtu.Color(vNormal.x()+1, vNormal.y()+1, vNormal.z()+1)*0.5

            pixel_color = get_color(generated_ray, world)


            main_camera.film[j,i,0] = pixel_color.r()
            main_camera.film[j,i,1] = pixel_color.g()
            main_camera.film[j,i,2] = pixel_color.b()


    main_camera.write_img('test_renderer2.png')


if __name__ == "__main__":
    render()


