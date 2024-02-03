import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

# Initialize glfw
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# Creating a window
window = glfw.create_window(640, 480, "PyOpenGL Interactable Cube", None, None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_pos(window, 400, 200)
glfw.make_context_current(window)

# Define cube vertices
vertices = [
    -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
     0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
     0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
    -0.5,  0.5, -0.5, 1.0, 1.0, 0.0,
    -0.5, -0.5,  0.5, 1.0, 0.0, 1.0,
     0.5, -0.5,  0.5, 0.0, 1.0, 1.0,
     0.5,  0.5,  0.5, 1.0, 1.0, 1.0,
    -0.5,  0.5,  0.5, 0.0, 0.0, 0.0
]

# Define cube indices
indices = [
    0, 1, 2, 2, 3, 0,
    4, 5, 6, 6, 7, 4,
    4, 5, 1, 1, 0, 4,
    6, 7, 3, 3, 2, 6,
    5, 6, 2, 2, 1, 5,
    7, 4, 0, 0, 3, 7
]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

# Vertex Buffer Object and Vertex Array Object
VBO = glGenBuffers(1)
VAO = glGenVertexArrays(1)
EBO = glGenBuffers(1)
glBindVertexArray(VAO)

glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

# Position attribute
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
# Color attribute
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

# Shader sources
vertex_src = """
# version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
out vec3 ourColor;
void main()
{
   gl_Position = vec4(aPos, 1.0);
   ourColor = aColor;
}
"""
fragment_src = """
# version 330 core
out vec4 FragColor;
in vec3 ourColor;
void main()
{
   FragColor = vec4(ourColor, 1.0);
}
"""

# Compile shaders
shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_src, GL_VERTEX_SHADER),
                                          OpenGL.GL.shaders.compileShader(fragment_src, GL_FRAGMENT_SHADER))

glUseProgram(shader)

# Main loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    glBindVertexArray(0)

    glfw.swap_buffers(window)

# Terminate glfw
glfw.terminate()
