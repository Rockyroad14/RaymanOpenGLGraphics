# Name: Jared Reich
# ID: 4672917
# CAP 4720 Assignment 3


# Import necessary libraries
import ctypes

import numpy
import pyrr
import numpy as np
import pygame as pg
from OpenGL.GL import *
import guiV1
import shaderLoader
from objLoaderV3 import ObjLoader

# Initialize pygame
pg.init()

# Set up OpenGL context version
pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)


# Create a window for graphics using OpenGL
width = 640
height = 480
pg.display.set_mode((width, height), pg.OPENGL | pg.DOUBLEBUF)


glClearColor(0.3, 0.4, 0.5, 1.0)
# Todo: Enable depth testing here using glEnable()
glEnable(GL_DEPTH_TEST)

# Todo: Part 3: Write shaders (vertex and fragment shaders) and compile them here

shader = shaderLoader.compile_shader(vs='shaders/vert.glsl', fs="shaders/frag.glsl")
glUseProgram(shader)

# Todo: Part 1: Read the 3D model
# Lets setup our scene geometry.
obj = ObjLoader("objects/dragon.obj")
vertices = np.array(obj.vertices, dtype="float32")
center = obj.center
dia = obj.dia

# Definitions for Uniform Variable setup and Input Variables
size_position = 3
size_texture = 2
size_normal = 3
stride = (size_position + size_normal + size_texture) * 4
offset_position = 0
offset_normal = (size_position + size_texture) * 4
offset_texture = size_position * 4
n_vertices = len(obj.vertices) // (size_position + size_normal + size_texture)
scale = 2.0 / dia
aspect = width / height
identity_matrix = pyrr.matrix44.create_identity()
up_vector = np.array([0, 1, 0])
near_plane = 0.1
far_plane = 1000
eye = np.array([0, 0, dia])





# Todo: Part 2: Upload the model data to the GPU. Create a VAO and VBO for the model data.

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, size=obj.vertices.nbytes, data=obj.vertices, usage=GL_STATIC_DRAW)



# Todo: Part 4: Configure vertex attributes using the variables defined in Part 1

position_loc = glGetAttribLocation(shader, "position")
glVertexAttribPointer(index=position_loc, size=size_position, type=GL_FLOAT, normalized=GL_FALSE, stride=stride, pointer=ctypes.c_void_p(offset_position))
glEnableVertexAttribArray(position_loc)
normal_loc = glGetAttribLocation(shader, "normal")
glVertexAttribPointer(index=normal_loc, size=size_normal, type=GL_FLOAT, normalized=GL_FALSE, stride=stride, pointer=ctypes.c_void_p(offset_normal))
glEnableVertexAttribArray(normal_loc)



# Todo: Part 5: Configure uniform variables.


model_mat_loc = glGetUniformLocation(shader, "model_matrix")
glUniformMatrix4fv(model_mat_loc, 1, GL_FALSE, identity_matrix)
view_mat_loc = glGetUniformLocation(shader, "view_matrix")
proj_mat_loc = glGetUniformLocation(shader, "projection_matrix")


gui = guiV1.SimpleGUI("Transformations")
sliderY = gui.add_slider("RotateY", -180, 180, 0)
sliderX = gui.add_slider("RotateX", -180, 180, 0)
sliderFov = gui.add_slider("fov", 30, 120, 45)


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
    viewX_matrix = pyrr.matrix44.create_from_x_rotation(numpy.deg2rad(sliderX.get_value()))
    viewY_matrix = pyrr.matrix44.create_from_y_rotation(numpy.deg2rad(sliderY.get_value()))
    transformed_eye = eye - center
    rotation_matrix = pyrr.matrix44.multiply(viewX_matrix, viewY_matrix)
    rotated_eye = pyrr.matrix44.apply_to_vector(rotation_matrix, transformed_eye)
    transformed_eye = rotated_eye + center
    view_matrix = pyrr.matrix44.create_look_at(transformed_eye, center,up_vector)
    fov = sliderFov.get_value()
    projection_matrix = pyrr.matrix44.create_perspective_projection_matrix(fov, aspect, near_plane, far_plane)

    glUniformMatrix4fv(view_mat_loc, 1, GL_FALSE, view_matrix)
    glUniformMatrix4fv(proj_mat_loc, 1, GL_FALSE, projection_matrix)

    glUseProgram(shader)
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)

    # Refresh the display to show what's been drawn
    pg.display.flip()


# Cleanup
glDeleteVertexArrays(1, [vao])
glDeleteBuffers(1, [vbo])
glDeleteProgram(shader)

pg.quit()   # Close the graphics window
quit()      # Exit the program