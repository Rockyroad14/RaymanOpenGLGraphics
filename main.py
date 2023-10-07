# Name: Jared Reich
# ID: 4672917
# CAP 4720 Assignment 3


# Import necessary libraries
import ctypes
import pyrr
import numpy as np
import pygame as pg
from OpenGL.GL import *
import guiV2
import shaderLoaderV2
from objLoaderV4 import ObjLoader

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

shader = shaderLoaderV2.compile_shader(vs='shaders/vert.glsl', fs="shaders/frag.glsl")
glUseProgram(shader)

# Todo: Part 1: Read the 3D model
# Lets setup our scene geometry.
obj = ObjLoader("objects/raymanModel.obj")
center = obj.center
scale = 2 / obj.dia
point_light = np.array([2, 2, 2, 1])
directional_light = np.array([2, 2, 2, 0])
ambient_intensity = 0.25

scaling_matrix = pyrr.matrix44.create_from_scale([scale, scale, scale])
translate_matrix = pyrr.matrix44.create_from_translation(-obj.center)
# Definitions for Uniform Variable setup and Input Variables

aspect = 2 * width / height




# Todo: Part 2: Upload the model data to the GPU. Create a VAO and VBO for the model data.

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, size=obj.vertices.nbytes, data=obj.vertices, usage=GL_STATIC_DRAW)

vao2 = glGenVertexArrays(1)
glBindVertexArray(vao2)
vbo2 = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo2)
glBufferData(GL_ARRAY_BUFFER, size=obj.vertices.nbytes, data=obj.vertices, usage=GL_STATIC_DRAW)

vao3 = glGenVertexArrays(1)
glBindVertexArray(vao3)
vbo3 = glGenVertexArrays(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo3)
glBufferData(GL_ARRAY_BUFFER, size=obj.vertices.nbytes, data=obj.vertices, usage=GL_STATIC_DRAW)




# Todo: Part 4: Configure vertex attributes using the variables defined in Part 1

position_loc = glGetAttribLocation(shader, "position")
glVertexAttribPointer(index=position_loc, size=obj.size_position, type=GL_FLOAT, normalized=GL_FALSE, stride=obj.stride, pointer=ctypes.c_void_p(obj.offset_position))
glEnableVertexAttribArray(position_loc)
normal_loc = glGetAttribLocation(shader, "normal")
glVertexAttribPointer(index=normal_loc, size=obj.size_normal, type=GL_FLOAT, normalized=GL_FALSE, stride=obj.stride, pointer=ctypes.c_void_p(obj.offset_normal))
glEnableVertexAttribArray(normal_loc)



# Todo: Part 5: Configure uniform variables.

aspect_loc = glGetUniformLocation(shader, "aspect")
glUniform1f(aspect_loc, aspect)

model_mat_loc = glGetUniformLocation(shader, "model_matrix")


gui = guiV2.SimpleGUI("Transformations")
sliderY = gui.add_slider("RotateY", -180, 180, 0)
sliderX = gui.add_slider("RotateX", -90, 90, 0)
sliderFov = gui.add_slider("fov", 45, 120, 90)
sliderShine = gui.add_slider("shininess", 1, 128, 32, 1)
sliderK_s = gui.add_slider("K_s", 0, 1, 0.5, 0.01)
materialPicker = gui.add_color_picker("material color", )


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


    Ymatrix = pyrr.matrix44.create_from_y_rotation(np.deg2rad(sliderY.get_value()))
    Xmatrix = pyrr.matrix44.create_from_x_rotation(np.deg2rad(sliderX.get_value()))

    model_mat = pyrr.matrix44.multiply(translate_mat1, Xmatrix)
    model_mat = pyrr.matrix44.multiply(model_mat, Ymatrix)
    model_mat = pyrr.matrix44.multiply(model_mat, Zmatrix)
    model_mat = pyrr.matrix44.multiply(model_mat, scaling_mat1)

    glUniformMatrix4fv(model_mat_loc, 1, GL_FALSE, model_mat)

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