import math, time, os, multiprocessing
from PIL import Image

# Object definitions
class Vector3():
    # A tuple of three values that represent a vector of x, y, z
    __slots__ = ("x", "y", "z") # the 'args'

    def __init__(self, x: float, y: float, z: float):
        # Initiate x, y, z
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vector3(self.x * other, self.y * other, self.z * other)
    
    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
    
    def length(self):
        return math.sqrt(self.x **2 + self.y ** 2 + self.z ** 2)
    
    def Unit(self):
        length = self.length()

        if length == 0:
            return Vector3(0, 0, 0)
        
        return self * ( 1.0 / length )

class Colour3(Vector3):
    """
    Identical to a Vector3 (inherits all properties), but 
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    # Run the parent class init function 

class Sphere():
    # A sphere that is rendered in the scene and raytraced
    __slots__ = (
        "centre", # The position of the sphere
        "radius", # The radius in aribtrary units
        "colour", # The colour as a Vector3
        "specular", # Glossiness (more glossy = more demanding)
        "texture" # image on the object
    )

    def __init__(self, centre: Vector3, radius: float, colour: Colour3, specular: float = 50.0, texture: Image.Image = None):
        self.centre = centre
        self.radius = radius
        self.colour = colour
        self.specular = specular
        self.texture = texture

class Scene():
    """
    A list of Spheres. Class made for clarity and abstraction rather than
    functionality.
    """

    def __init__(self, scene_list = list[Sphere]):
        self.content = scene_list

def sphere_uv(hit_point: Vector3, sphere: Sphere, u_offset: float = 0.0):
    point = (hit_point - sphere.centre).Unit()
    u = 0.5 + (math.atan2(point.z, point.x) / (2 * math.pi)) + u_offset
    u = u % 1.0  # wrap around

    v = 0.5 - (math.asin(point.y) / math.pi)

    return u, v

def intersect_sphere(ray_origin: Vector3, ray_direction: Vector3, sphere: Sphere):
    """
    Check if the ray hits a sphere, and if it does, return how far along 
    the ray the hit occurs
    """
    origin_to_centre = ray_origin - sphere.centre # find the distance from the origin to the centre, returns Vector3

    # ax^2 + bx + c
    a = ray_direction.dot(ray_direction) # dot product with itself
    b = 2.0 * origin_to_centre.dot(ray_direction)
    c = origin_to_centre.dot(origin_to_centre) - (sphere.radius ** 2)

    discriminant = (b**2) - (4 * a * c)

    if discriminant < 0: # No real solutions, return none
        return
    
    # ( -b (+-) sqrt(b^2 -4ac) ) / 2a
    sqrt_discriminant = math.sqrt(discriminant)

    root_0 = (-b - sqrt_discriminant) / (2 * a)
    root_1 = (-b + sqrt_discriminant) / (2 * a)

    if root_0 > 1e-6:
        return root_0
    
    if root_1 > 1e-6:
        return root_1
    
    return # Both roots are way too small or negative, so return nothing

def shade_hit_point(hit_point: Vector3, surface_normal: Vector3, view_direction: Vector3, sphere: Sphere, light_position: Vector3):
    """
    This simulates shading the point hit by passed light at the passed hit point
    using the phong shading method. This is the more demanding version of shading,
    but this is also commonly used in ray-tracing, so it simulates a realistic
    workload.

    Uses ambient, diffuse, and specular (base colour, shadow map, reflection map) to fully shade an object.
    """
    ambient = 0.05 # the ambient layer, a constant low-level light
    # this means 5% of the object's base colour contributes to the final
    # colour even if no light hits it.

    light_direction = (light_position - hit_point).Unit() # .Unit uses the class' function which normalises all values to be below 1 and identical proportionally and directionally, just not in magnitude
    diffuse_intensity = max(0, surface_normal.dot(light_direction)) # calculate the intensity of light diffusion at a point
    half_vector = (light_direction + view_direction).Unit()
    specular_intensity = (max(0, surface_normal.dot(half_vector)) ** sphere.specular) # calculate the intensity of the reflections

    # textures because yay
    if sphere.texture:
        u, v = sphere_uv(hit_point, sphere, u_offset=0.25)
        tex_width, tex_height = sphere.texture.size
        tex_x = int(u * tex_width) % tex_width
        tex_y = int(v * tex_height) % tex_height
        tex_colour = sphere.texture.getpixel((tex_x, tex_y))
        base_colour = Colour3(tex_colour[0]/255, tex_colour[1]/255, tex_colour[2]/255)
    else:
        base_colour = sphere.colour

    r = min(1.0, base_colour.x * (ambient + diffuse_intensity) + specular_intensity)
    g = min(1.0, base_colour.y * (ambient + diffuse_intensity) + specular_intensity)
    b = min(1.0, base_colour.z * (ambient + diffuse_intensity) + specular_intensity)

    return Colour3(r, g, b)


def trace_ray(ray_origin: Vector3, ray_direction: Vector3, scene: Scene, light_position: Vector3):
    """
    Trace an individual ray from the ray origin, in the ray direction (with magnitude),
    in the given scene.
    """

    nearest_t = 1e+30 # very large number to begin with, most likely nearest t is lower than this (t = distance from the origin)
    hit_sphere = None # Initialise hit sphere

    for sphere in scene.content:
        t = intersect_sphere(
            ray_origin=ray_origin,
            ray_direction=ray_direction,
            sphere=sphere
        ) # distance along the ray

        if t and t < nearest_t:
            nearest_t = t
            hit_sphere = sphere

    if hit_sphere is None:
        # normalised vertical position
        # (-1, 1) -> (0, 2)
        # (0, 1)
        t = 0.5 * (ray_direction.y + 1)
        # t = 0, pointing straight down, 1 = straight up

        return Colour3(  
            # rays pointing up -> brighter blue, pointing down -> less saturated blue
            0.6 * (1 - t)+ (0.2 * t),
            0.7*(1-t)+0.8*t,
            1.0*(1-t)+1.0*t
        )
    
    hit_point = ray_origin +  ( ray_direction * nearest_t )
    normal_at_hit = (hit_point - hit_sphere.centre).Unit()

    view_direction = ray_direction * -1.0
    return shade_hit_point(hit_point, normal_at_hit, view_direction, hit_sphere, light_position) # shade area based on sphere

def render_frame(width, height, camera_position: Vector3, camera_target: Vector3, fov_degrees: float, scene: list, light_position: Vector3, save_output: bool = False):
    aspect_ratio = width / float(height) # calculate the aspect ratio of the frame
    field_of_view = math.tan(math.radians(fov_degrees)*0.5) # and the field of view as a unit

    forward = (camera_target - camera_position).Unit() # calculate the (forward) camera direction
    up_vector = Vector3(0, 1, 0) # pre-unit-ed 

    right_vector = Vector3(
        forward.y*up_vector.z - forward.z*up_vector.y,
        forward.z*up_vector.x - forward.x*up_vector.z,
        forward.x*up_vector.y - forward.y*up_vector.x
    ).Unit()

    up_vector = Vector3(
        right_vector.y*forward.z - right_vector.z*forward.y,
        right_vector.z*forward.x - right_vector.x*forward.z,
        right_vector.x*forward.y - right_vector.y*forward.x
    ).Unit()

    total_pixels_processed = 0
    if save_output:
        image = [[None for _ in range(width)] for _ in range(height)]
    
    for pixel_y in range(height):
        # get y coordinate from pixel
        screen_y = (1 - 2 * ((pixel_y+0.5)/height)) * field_of_view

        for pixel_x in range(width):
            # get x coord from pixel
            screen_x = (2 * ((pixel_x+0.5)/width) - 1) * field_of_view * aspect_ratio
            ray_direction = (right_vector*screen_x + up_vector*screen_y + forward).Unit()

            # actually trace the ray
            colour = trace_ray(camera_position, ray_direction, scene, light_position)
            if save_output:
                image[pixel_y][pixel_x] = colour

            # add a pixel processed!
            total_pixels_processed += 1

    # now render...
    if save_output:
        img = Image.new("RGB", (width, height))
        for y in range(height):
            for x in range(width):
                color = image[y][x]
                r = int(255 * min(max(color.x,0),1))
                g = int(255 * min(max(color.y,0),1))
                b = int(255 * min(max(color.z,0),1))
                img.putpixel((x, y), (r, g, b))

        img.save("output.png")

    return total_pixels_processed

# For async
def render_chunk(start_y: int, end_y: int, width: int, height: int, camera_position: Vector3, camera_target: Vector3, fov_degrees: float, scene: Scene, light_position: Vector3, return_dict: dict, chunk_index: int):
    """
    Renders a vertical chunk of the image and stores the results
    in the return_dict parameter. Used for the multicore ray tracer.
    """

    aspect_ratio = width/float(height) # calculate ar
    field_of_view = math.tan(math.radians(fov_degrees) * 0.5) # and fov

    forward = (camera_target - camera_position).Unit() # calculate the (forward) camera direction
    up_vector = Vector3(0, 1, 0) # pre-unit-ed 

    right_vector = Vector3(
        forward.y*up_vector.z - forward.z*up_vector.y,
        forward.z*up_vector.x - forward.x*up_vector.z,
        forward.x*up_vector.y - forward.y*up_vector.x
    ).Unit()

    up_vector = Vector3(
        right_vector.y*forward.z - right_vector.z*forward.y,
        right_vector.z*forward.x - right_vector.x*forward.z,
        right_vector.x*forward.y - right_vector.y*forward.x
    ).Unit()

    # make the empty chunk that needs to be rendered
    chunk_image = [[None for _ in range(width)] for _ in range(end_y - start_y)]

    for pixel_y in range(start_y, end_y):
        # for each y pixel in the chunk
        screen_y = (1 - 2 * ((pixel_y + 0.5)/height)) * field_of_view # get screen coord
        for pixel_x in range(width):
            # for each x pixel in that y layer
            screen_x = (2 * ((pixel_x + 0.5)/width) - 1) * field_of_view * aspect_ratio # get screen coord
            ray_direction = (right_vector * screen_x + up_vector * screen_y + forward).Unit() # get ray dir

            chunk_image[pixel_y - start_y][pixel_x] = trace_ray(camera_position, ray_direction, scene, light_position) # trace the ray and set the chunk data

    return_dict[chunk_index] = chunk_image # add rendered data to the dict

def render_frame_multicore(width: int, height: int, camera_position: Vector3, camera_target: Vector3, fov_degrees: float, scene: Scene, light_position: Vector3, save_output: bool = False):
    logical_cores = os.cpu_count() # number of virtualized processoors
    chunk_height = height // logical_cores # y range assigned to each core
    proc_manager = multiprocessing.Manager() # new manager object

    return_dict = proc_manager.dict()
    processes = []

    for idx in range(logical_cores):
        start_y = idx * chunk_height
        end_y = height if idx == logical_cores - 1 else (idx + 1) * chunk_height # last core may have different amount of work to do depending on the remainder

        p = multiprocessing.Process(
            target=render_chunk,
            args=(
                start_y,
                end_y,
                width,
                height,
                camera_position,
                camera_target,
                fov_degrees,
                scene,
                light_position,
                return_dict,
                idx
            )
        )

        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()

    # once finished, manage results in return dict

    image = []
    for i in range(logical_cores):
        image.extend(return_dict[i]) # .extend, truncate lists together

    if save_output:
        from PIL import Image
        img = Image.new("RGB", (width, height))
        for y in range(height):
            for x in range(width):
                color = image[y][x]
                r = int(255 * min(max(color.x, 0), 1))
                g = int(255 * min(max(color.y, 0), 1))
                b = int(255 * min(max(color.z, 0), 1))
                img.putpixel((x, y), (r, g, b))

        img.save("output.png")

    return width * height

TEST_SCENE = Scene(scene_list=[
    Sphere(centre=Vector3(2,1,3), radius=0.9, colour=Colour3(0.9,0.2,0.2), specular=80.0),
    Sphere(centre=Vector3(-2,1,3), radius=0.7, colour=Colour3(0.5,0.9,0.3), specular=30.0),
    Sphere(centre=Vector3(0.0,-100.5,3.5), radius=100.0, colour=Colour3(0.8,0.8,0.8), specular=10.0)
])

# test vectors
TEST_CAMERA_POSITION = Vector3(0.0,0.0,0.0)
TEST_CAMERA_TARGET = Vector3(0.0,0.0,1.0)
TEST_LIGHT_POSITION = Vector3(5.0,5.0,-2.0)