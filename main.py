import pygame as pg
from OpenGL.GL import *
import numpy as np
import shaderLoaderV3
from objLoaderV4 import ObjLoader
from guiV3 import SimpleGUI
import pyrr


def upload_and_configure_attributes(object, shader):
    # VAO and VBO
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, object.vertices.nbytes, object.vertices, GL_STATIC_DRAW)

    # Define the vertex attribute configurations
    # we can either query the locations of the attributes in the shader like we did in our previous assignments
    # or explicitly tell the shader that the attribute "position" corresponds to location 0.
    # It is recommended to explicitly set the locations of the attributes in the shader than querying them.
    # Position attribute
    position_loc = 0
    tex_coord_loc = 1
    normal_loc = 2
    glBindAttribLocation(shader, position_loc, "position")
    glBindAttribLocation(shader, tex_coord_loc, "uv")
    glBindAttribLocation(shader, normal_loc, "normal")

    glVertexAttribPointer(position_loc, object.size_position, GL_FLOAT, GL_FALSE, object.stride, ctypes.c_void_p(object.offset_position))
    glVertexAttribPointer(tex_coord_loc, object.size_texture, GL_FLOAT, GL_FALSE, object.stride, ctypes.c_void_p(object.offset_texture))
    glVertexAttribPointer(normal_loc, object.size_normal, GL_FLOAT, GL_FALSE, object.stride, ctypes.c_void_p(object.offset_normal))

    glEnableVertexAttribArray(tex_coord_loc)
    glEnableVertexAttribArray(position_loc)
    glEnableVertexAttribArray(normal_loc)

    return vao, vbo, object.n_vertices




'''
# Program starts here
'''


# Initialize pygame
pg.init()

# Set up OpenGL context version
pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_STENCIL_SIZE, 8)

# Create a window for graphics using OpenGL
width = 1280
height = 720
pg.display.set_mode((width, height), pg.OPENGL | pg.DOUBLEBUF)



# Set the background color (clear color)
# glClearColor takes 4 arguments: red, green, blue, alpha. Each argument is a float between 0 and 1.
glClearColor(0.3, 0.4, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)


# Write our shaders.
# Shader to render the scene with shadow from camera's point of view
shaderProgram_scene = shaderLoaderV3.ShaderProgram("shaders/scene/vert_scene.glsl", "shaders/scene/frag_scene.glsl")


'''
# **************************************************************************************************************
# Load our objects and configure their attributes
# **************************************************************************************************************
'''
# obj = ObjLoader("objects/rayman/raymanModel.obj")
obj = ObjLoader("objects/dragon.obj")
vao_obj, vbo_obj, n_vertices_obj = upload_and_configure_attributes(obj, shaderProgram_scene.shader)


# **************************************************************************************************************
# **************************************************************************************************************



'''
# **************************************************************************************************************
# Define camera attributes
# **************************************************************************************************************
'''
eye = (0,3,4)
target = (0,0,0)
up = (0,1,0)

fov = 45
aspect = width/height
near = 0.1
far = 20

lightPos = [1, 4, 1]
lightPosition = [1, 4, 1, 1]
# **************************************************************************************************************
# **************************************************************************************************************



'''
# **************************************************************************************************************
# Configure model matrices
# **************************************************************************************************************
'''
# for object
translation_mat = pyrr.matrix44.create_from_translation(-obj.center)
scaling_mat = pyrr.matrix44.create_from_scale([2 / obj.dia, 2 / obj.dia, 2 / obj.dia])
model_mat_obj = pyrr.matrix44.multiply(translation_mat, scaling_mat)

# for receiver
rotation_mat = pyrr.matrix44.create_from_x_rotation(np.deg2rad(90))
translation_mat = pyrr.matrix44.create_from_translation([0, -1, 0])
scaling_mat = pyrr.matrix44.create_from_scale([2, 2, 2])
model_mat_receiver = pyrr.matrix44.multiply(scaling_mat, rotation_mat)
model_mat_receiver = pyrr.matrix44.multiply(model_mat_receiver, translation_mat)
# **************************************************************************************************************
# **************************************************************************************************************





'''
# **************************************************************************************************************
# Setup gui
# **************************************************************************************************************
'''
gui = SimpleGUI("Skybox")

# Create a slider for the rotation angle around the Y axis
light_rotY_slider = gui.add_slider("light Y angle", -180, 180, 0, resolution=1)

camera_rotY_slider = gui.add_slider("camera Y angle", -180, 180, 0, resolution=1)
camera_rotX_slider = gui.add_slider("camera X angle", -90, 90, 0, resolution=1)
fov_slider = gui.add_slider("fov", fov, 120, fov, resolution=1)

light_color_slider = gui.add_color_picker(label_text="light color", initial_color=(0.8, 0.8, 0.8))
ambient_intensity_slider = gui.add_slider("Ambient Intensity", 0, 1, 0, resolution=0.01)
roughness_slider = gui.add_slider("Roughness", 0, 1, 0, resolution=0.01)
metallic_slider = gui.add_slider("Metallic", 0, 1, 0, resolution=0.01)
material_radio = gui.add_radio_buttons("Material", options_dict={"Iron": [0.56, 0.57, 0.58], "Copper": [0.95, 0.64, 0.54], "Gold": [1.00, 0.71, 0.29], "Aluminium": [0.91, 0.92, 0.92], "Silver": [0.95,0.93,0.88]})


# **************************************************************************************************************
# **************************************************************************************************************



# Run a loop to keep the program running
draw = True
while draw:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear color buffer and depth buffer before drawing each frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # view and projection matrices for camera's point of view
    cam_rotY_mat = pyrr.matrix44.create_from_y_rotation(np.deg2rad(camera_rotY_slider.get_value()))
    cam_rotX_mat = pyrr.matrix44.create_from_x_rotation(np.deg2rad(camera_rotX_slider.get_value()))
    cam_rot_mat = pyrr.matrix44.multiply(cam_rotX_mat, cam_rotY_mat)
    rotated_eye = pyrr.matrix44.apply_to_vector(cam_rot_mat, eye)
    print(rotated_eye)

    view_mat = pyrr.matrix44.create_look_at(rotated_eye, target, up)
    projection_mat = pyrr.matrix44.create_perspective_projection_matrix(fov_slider.get_value(), aspect, near,  far)

    # view and projection matrices for light's point of view
    light_rotY_mat = pyrr.matrix44.create_from_y_rotation(np.deg2rad(light_rotY_slider.get_value()))
    rotated_lightPos = pyrr.matrix44.apply_to_vector(light_rotY_mat, lightPos)

    light_view_mat = pyrr.matrix44.create_look_at(rotated_lightPos, target, up)
    light_projection_mat = pyrr.matrix44.create_perspective_projection_matrix(fov_slider.get_value(), aspect, near, far)



    pg.display.flip()



# Cleanup
glDeleteVertexArrays(2, [vao_obj])
glDeleteBuffers(2, [vbo_obj])

glDeleteProgram(shaderProgram_scene.shader)

pg.quit()   # Close the graphics window
quit()      # Exit the program