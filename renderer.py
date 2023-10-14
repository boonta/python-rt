import RT_utility as rtu
import RT_ray as rtr
import RT_camera as rtc
import RT_object as rto


def background_color(rGen_ray):
    unit_direction = rtu.Vec3.unit_vector(rGen_ray.getDirection())
    a = (unit_direction.y() + 1.0)*0.5
    return rtu.Color(1,1,1)*(1.0-a) + rtu.Color(0.5, 0.7, 1.0)*a

def render():
    main_camera = rtc.Camera()
    main_camera.aspect_ratio = 16.0/9.0
    main_camera.img_width = 400
    main_camera.focal_length = 1.0
    main_camera.viewport_height = 2.0
    main_camera.center = rtu.Vec3(0,0,0)

    for j in range(main_camera.img_height):
        for i in range(main_camera.img_width):
            pixel_center = main_camera.pixel00_location + (main_camera.pixel_du*i) + (main_camera.pixel_dv*j)
            ray_direction = pixel_center - main_camera.center
            generated_ray = rtr.Ray(main_camera.center, ray_direction)

            pixel_color = background_color(generated_ray)

            main_camera.film[j,i,0] = pixel_color.r()
            main_camera.film[j,i,1] = pixel_color.g()
            main_camera.film[j,i,2] = pixel_color.b()


    main_camera.write_img('test_renderer.png')


if __name__ == "__main__":
    render()


