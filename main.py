# Name: Jared Reich
# ID: 4672917
# CAP 4720 Assignment 3

# Import necessary libraries
import numpy
import pyrr
import numpy as np
import pygame as pg
from OpenGL.GL import *
import guiV1
import shaderLoader
from objLoaderV4 import ObjLoader

# Initialize pygame
pg.init()

# Set up OpenGL context version
pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)


# Create a window for graphics using OpenGL
width = 640
height = 480
pg.display.set_mode((width * 2, height), pg.OPENGL | pg.DOUBLEBUF)


glClearColor(0.3, 0.4, 0.5, 1.0)
# Todo: Enable depth testing here using glEnable()
glEnable(GL_DEPTH_TEST)
glEnable(GL_SCISSOR_TEST)

# Todo: Part 3: Write shaders (vertex and fragment shaders) and compile them here

dragon_shader = shaderLoader.compile_shader(vs='shaders/vert.glsl', fs="shaders/frag.glsl")
glUseProgram(dragon_shader)
raymon_shader = shaderLoader.compile_shader(vs='shaders/vert.glsl', fs='shaders/frag2.glsl')
glUseProgram(raymon_shader)

# Todo: Part 1: Read the 3D model
# Lets setup our scene geometry.
dragon_obj = ObjLoader("objects/dragon.obj")
rayman_obj = ObjLoader("objects/raymanModel.obj")
raymon_vertices = np.array(rayman_obj.vertices, dtype="float32")
dragon_vertices = np.array(dragon_obj.vertices, dtype="float32")


# Definitions for Uniform Variable setup and Input Variables

rayman_scale = 2 / rayman_obj.dia
dragon_scale = 2 / dragon_obj.dia
aspect = width / height
identity_matrix = pyrr.matrix44.create_identity()
rayman_translate_matrix = pyrr.matrix44.create_from_translation(-rayman_obj.center)
dragon_translate_matrix = pyrr.matrix44.create_from_translation(-dragon_obj.center)
rayman_scale_matrix = pyrr.matrix44.create_from_scale([rayman_scale, rayman_scale, rayman_scale])
dragon_scale_matrix = pyrr.matrix44.create_from_scale([dragon_scale, dragon_scale, dragon_scale])
rayman_model_matrix = pyrr.matrix44.multiply(identity_matrix, rayman_translate_matrix)
rayman_model_matrix = pyrr.matrix44.multiply(rayman_model_matrix, rayman_scale_matrix)
dragon_model_matrix = pyrr.matrix44.multiply(identity_matrix, dragon_translate_matrix)
dragon_model_matrix = pyrr.matrix44.multiply(dragon_model_matrix, dragon_scale_matrix)
up_vector = np.array([0, 1, 0])
near_plane = 0.1
far_plane = 1000
eye = np.array([0, 0, 2])
look_at = np.array([0, 0, 0])


# Todo: Part 2: Upload the model data to the GPU. Create a VAO and VBO for the model data.
# Dragon Object----------------------------------------------------------
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, size=dragon_obj.vertices.nbytes, data=dragon_obj.vertices, usage=GL_STATIC_DRAW)

# Dragon object and how to format the arrays
dragon_pos_loc = glGetAttribLocation(dragon_shader, "position")
glVertexAttribPointer(index=dragon_pos_loc, size=dragon_obj.size_position, type=GL_FLOAT, normalized=GL_FALSE, stride=dragon_obj.stride, pointer=ctypes.c_void_p(dragon_obj.offset_position))
glEnableVertexAttribArray(dragon_pos_loc)
dragon_normal_loc = glGetAttribLocation(dragon_shader, "normal")
glVertexAttribPointer(index=dragon_normal_loc, size=dragon_obj.size_normal, type=GL_FLOAT, normalized=GL_FALSE, stride=dragon_obj.stride, pointer=ctypes.c_void_p(dragon_obj.offset_normal))
glEnableVertexAttribArray(dragon_normal_loc)
# -------------------------------------------------------------------------
# Rayman Object------------------------------------------------------------
vao2 = glGenVertexArrays(1)
glBindVertexArray(vao)

vbo2 = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo2)
glBufferData(GL_ARRAY_BUFFER, size=rayman_obj.vertices.nbytes, data=rayman_obj.vertices, usage=GL_STATIC_DRAW)
# Rayman Object Formatting
rayman_pos_loc = glGetAttribLocation(raymon_shader, "position")
glVertexAttribPointer(index=rayman_pos_loc, size=rayman_obj.size_position, type=GL_FLOAT, normalized=GL_FALSE, stride=rayman_obj.stride, pointer=ctypes.c_void_p(rayman_obj.offset_position))
glEnableVertexAttribArray(rayman_pos_loc)
rayman_normal_loc = glGetAttribLocation(raymon_shader, "normal")
glVertexAttribPointer(index=rayman_normal_loc, size=rayman_obj.size_normal, type=GL_FLOAT, normalized=GL_FALSE, stride=rayman_obj.stride, pointer=ctypes.c_void_p(rayman_obj.offset_normal))
glEnableVertexAttribArray(rayman_normal_loc)
#-------------------------------------------------------------------------------
# Todo: Part 5: Configure uniform variables.


dragon_model_mat_loc = glGetUniformLocation(dragon_shader, "model_matrix")
glUniformMatrix4fv(dragon_model_mat_loc, 1, GL_FALSE, dragon_model_matrix)
rayman_model_mat_loc = glGetUniformLocation(raymon_shader, "model_matrix")
glUniformMatrix4fv(rayman_model_mat_loc, 1, GL_FALSE, rayman_model_matrix)
dragon_view_mat_loc = glGetUniformLocation(dragon_shader, "view_matrix")
dragon_proj_mat_loc = glGetUniformLocation(dragon_shader, "projection_matrix")
rayman_view_mat_loc = glGetUniformLocation(raymon_shader, "view_matrix")
rayman_proj_mat_loc = glGetUniformLocation(raymon_shader, "projection_matrix")



gui = guiV1.SimpleGUI("Transformations")
sliderY = gui.add_slider("RotateY", -180, 180, 0)
sliderX = gui.add_slider("RotateX", -90, 90, 0)
sliderFov = gui.add_slider("fov", 25, 120, 45)


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

    rotation_y_matrix = pyrr.matrix44.create_from_y_rotation(np.deg2rad(sliderY.get_value()))
    rotation_x_matrix = pyrr.matrix44.create_from_x_rotation(np.deg2rad(sliderX.get_value()))
    rotation_eye_matrix = pyrr.matrix44.multiply(rotation_y_matrix, rotation_x_matrix)
    rotated_eye = pyrr.matrix44.apply_to_vector(rotation_eye_matrix, eye)
    view_matrix = pyrr.matrix44.create_look_at(rotated_eye, look_at, up_vector)
    projection_matrix = pyrr.matrix44.create_perspective_projection_matrix(sliderFov.get_value(), aspect, near_plane, far_plane)

    glViewport(0, 0, width, height)
    glScissor(0, 0, width, height)
    glClearColor(0.3, 0.4, 0.5, 1.0)

    glUseProgram(dragon_shader)
    glUniformMatrix4fv()




    glUseProgram(dragon_shader)
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, dragon_obj.n_vertices)

    # Refresh the display to show what's been drawn
    pg.display.flip()


# Cleanup
glDeleteVertexArrays(1, [vao, vao2])
glDeleteBuffers(1, [vbo, vbo2])
glDeleteProgram([dragon_shader, raymon_shader])

pg.quit()   # Close the graphics window
quit()      # Exit the program