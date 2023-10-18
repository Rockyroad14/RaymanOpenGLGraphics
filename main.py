# Name: Jared Reich
# ID: 4672917
# CAP 4720 Assignment 3


# Import necessary libraries
import pyrr
import numpy as np
import pygame as pg
from OpenGL.GL import *
import guiV1
import shaderLoader
from objLoaderV2 import ObjLoader

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
obj = ObjLoader("objects/raymanModel.obj")
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
translate_mat1 = pyrr.matrix44.create_from_translation(-center)
scaling_mat1 = pyrr.matrix44.create_from_scale([scale, scale, scale])



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

aspect_loc = glGetUniformLocation(shader, "aspect")
glUniform1f(aspect_loc, aspect)

model_mat_loc = glGetUniformLocation(shader, "model_matrix")


gui = guiV1.SimpleGUI("Transformations")
sliderZ = gui.add_slider("RotateZ", -90, 90, 0)
sliderY = gui.add_slider("RotateY", -180, 180, 0)
sliderX = gui.add_slider("RotateX", -90, 90, 0)



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

    Zmatrix = pyrr.matrix44.create_from_z_rotation(np.deg2rad(sliderZ.get_value()))
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