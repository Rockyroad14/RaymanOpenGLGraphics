# Name: Jared Reich
# ID: 4672917
# CAP 4720 Assignment 9


# Import necessary libraries
import pyrr
import numpy as np
import pygame as pg
from OpenGL.GL import *
import guiV3
from shaderLoaderV3 import ShaderProgram
from objLoaderV4 import ObjLoader
from utils import load_image, load_cubemap_texture

# Initialize pygame
pg.init()

# Set up OpenGL context version
pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)


# Create a window for graphics using OpenGL
width = 640
height = 480
pg.display.set_mode((2 * width, height), pg.OPENGL | pg.DOUBLEBUF)


glClearColor(0.3, 0.4, 0.5, 1.0)
# Todo: Enable depth testing here using glEnable()
glEnable(GL_DEPTH_TEST)

# Todo: Part 3: Write shaders (vertex and fragment shaders) and compile them here

shader = ShaderProgram(vs='shaders/vert.glsl', fs="shaders/frag.glsl")
glUseProgram(shader.shader)

# Todo: Part 1: Read the 3D model
# Lets setup our scene geometry.
obj = ObjLoader("objects/stormtrooper.obj")
center = obj.center
scale = 2 / obj.dia
point_light = np.array([2, 2, 2, 1])
directional_light = np.array([2, 2, 2, 0])
ambient_intensity = 0.25
scaling_matrix = pyrr.matrix44.create_from_scale([scale, scale, scale])
translate_matrix2 = pyrr.matrix44.create_from_translation(-obj.center)
model_matrix = pyrr.matrix44.multiply(translate_matrix2, scaling_matrix)
# Definitions for Uniform Variable setup and Input Variables
eye = np.array([0, 0, 2])
up = np.array([0, 1, 0])
look_at = np.array([0, 0, 0])
aspect = 2 * width / height
near = 0.1
far = 10
cubemap_images = ["skybox/right.png", "skybox/left.png",
                  "skybox/top.png", "skybox/bottom.png",
                  "skybox/front.png", "skybox/back.png"]




# Todo: Part 2: Upload the model data to the GPU. Create a VAO and VBO for the model data.

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, size=obj.vertices.nbytes, data=obj.vertices, usage=GL_STATIC_DRAW)



# Todo: Part 4: Configure vertex attributes using the variables defined in Part 1

position_loc = glGetAttribLocation(shader.shader, "position")
glVertexAttribPointer(index=position_loc, size=obj.size_position, type=GL_FLOAT, normalized=GL_FALSE, stride=obj.stride, pointer=ctypes.c_void_p(obj.offset_position))
glEnableVertexAttribArray(position_loc)
texture_loc = glGetAttribLocation(shader.shader, "uv")
glVertexAttribPointer(index=texture_loc, size=obj.size_texture, type=GL_FLOAT, normalized=GL_FALSE, stride=obj.stride, pointer=ctypes.c_void_p(obj.offset_texture))
glEnableVertexAttribArray(texture_loc)

# Todo: Part 5: Configure uniform variables.

img_texture, img_width, img_height = load_image("objects/stormtrooper.jpg", flip=True)
cubemap_id = load_cubemap_texture(cubemap_images)




texture_id = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture_id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_texture)
glGenerateMipmap(GL_TEXTURE_2D)




gui = guiV3.SimpleGUI("Transformations")
sliderY = gui.add_slider("RotateY", -180, 180, 0, 1)
sliderX = gui.add_slider("RotateX", -90, 90, 0, 1)
sliderFov = gui.add_slider("fov", 45, 120, 90, 1)
texturePicker = gui.add_radio_buttons("Texture Type", options_dict={"Environment mapping": 1, "2D texture": 2, "Mix": 3}, initial_option="Environment mapping")



# Todo: Part 6: Do the final rendering. In the rendering loop, do the following:
    # - Clear the color buffer and depth buffer before drawing each frame using glClear()
    # - Use the shader program using glUseProgram()
    # - Bind the VAO using glBindVertexArray()
    # - Draw the triangle using glDrawArrays()


# Run a loop to keep the program running
draw = True
while draw:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            draw = False

    # Clear color buffer and depth buffer before drawing each frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader.shader)

    # Creating Rotation and rotated eye matrixes
    Ymatrix = pyrr.matrix44.create_from_y_rotation(np.deg2rad(sliderY.get_value()))
    Xmatrix = pyrr.matrix44.create_from_x_rotation(np.deg2rad(sliderX.get_value()))
    rotation_mat = pyrr.matrix44.multiply(Xmatrix, Ymatrix)
    rotated_eye = pyrr.matrix44.apply_to_vector(rotation_mat, eye)

    view_matrix = pyrr.matrix44.create_look_at(rotated_eye, look_at, up)
    projection_matrix = pyrr.matrix44.create_perspective_projection_matrix(sliderFov.get_value(), aspect, near, far)

    shader["tex"] = 0
    shader["view_matrix"] = view_matrix
    shader["projection_matrix"] = projection_matrix
    shader["model_matrix"] = model_matrix
    shader["eye_pos"] = rotated_eye
    shader["ambient_intensity"] = ambient_intensity

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glUseProgram(shader.shader)
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, obj.n_vertices)


    # Refresh the display to show what's been drawn
    pg.display.flip()


# Cleanup
glDeleteVertexArrays(1, [vao])
glDeleteBuffers(1, [vbo])
glDeleteProgram(shader.shader)

pg.quit()   # Close the graphics window
quit()      # Exit the program