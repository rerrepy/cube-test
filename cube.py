import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm

# Initialize glfw
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# Creating a window
window = glfw.create_window(640, 480, "PyOpenGL Interactable Cube", None, None)

# Global variables for rotation
mouse_x_pos, mouse_y_pos = 0, 0
rotation_x, rotation_y = 0, 0

def mouse_look_callback(window, xpos, ypos):
    global mouse_x_pos, mouse_y_pos, rotation_x, rotation_y
    sensitivity = 0.1
    
    if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
        x_offset = xpos - mouse_x_pos
        y_offset = mouse_y_pos - ypos  # Reversed since y-coordinates range bottom to top
        rotation_x += x_offset * sensitivity
        rotation_y += y_offset * sensitivity

    mouse_x_pos, mouse_y_pos = xpos, ypos

def get_rotation_matrix(rotation_x, rotation_y):
    model = glm.mat4(1.0)  # Create identity matrix
    model = glm.rotate(model, glm.radians(rotation_x), glm.vec3(0, 1, 0))  # Rotate around the Y axis
    model = glm.rotate(model, glm.radians(rotation_y), glm.vec3(1, 0, 0))  # Rotate around the X axis
    return model




glfw.set_cursor_pos_callback(window, mouse_look_callback)



if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_pos(window, 400, 200)
glfw.make_context_current(window)

# Define cube vertices
vertices = [
    -0.5, -0.5, -0.5, 0.0, 0.0, 0.0,  # Black color
     0.5, -0.5, -0.5, 0.0, 0.0, 0.0,  # Black color
     0.5,  0.5, -0.5, 0.0, 0.0, 0.0,  # Black color
    -0.5,  0.5, -0.5, 0.0, 0.0, 0.0,  # Black color
    -0.5, -0.5,  0.5, 0.0, 0.0, 0.0,  # Black color
     0.5, -0.5,  0.5, 0.0, 0.0, 0.0,  # Black color
     0.5,  0.5,  0.5, 0.0, 0.0, 0.0,  # Black color
    -0.5,  0.5,  0.5, 0.0, 0.0, 0.0   # Black color
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

"""
grid_lines_vertices = [
    # Vertical lines (x constant, y varies)
    -1/5, -0.5, -0.5,  1.0, 1.0, 1.0,
    -1/5,  0.5, -0.5,  1.0, 1.0, 1.0,
    1/5, -0.5, -0.5,  1.0, 1.0, 1.0,
    1/5,  0.5, -0.5,  1.0, 1.0, 1.0,
    
    # Horizontal lines (y constant, x varies)
    -0.5, -1/5, -0.5,  1.0, 1.0, 1.0,
     0.5, -1/5, -0.5,  1.0, 1.0, 1.0,
    -0.5,  1/5, -0.5,  1.0, 1.0, 1.0,
     0.5,  1/5, -0.5,  1.0, 1.0, 1.0,
]
"""

grid_lines_vertices = [
    # Vertical lines (x constant, y varies)
    -1/6, -0.5, -0.5,  1.0, 1.0, 1.0,
    -1/6,  0.5, -0.5,  1.0, 1.0, 1.0,
     1/6, -0.5, -0.5,  1.0, 1.0, 1.0,
     1/6,  0.5, -0.5,  1.0, 1.0, 1.0,
    
    # Horizontal lines (y constant, x varies)
    -0.5, -1/6, -0.5,  1.0, 1.0, 1.0,
     0.5, -1/6, -0.5,  1.0, 1.0, 1.0,
    -0.5,  1/6, -0.5,  1.0, 1.0, 1.0,
     0.5,  1/6, -0.5,  1.0, 1.0, 1.0,
]


grid_lines_vertices = np.array(grid_lines_vertices, dtype=np.float32)
vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)



# Generate and bind VAO and VBO for grid lines (similar to cube setup)
grid_VAO = glGenVertexArrays(1)
grid_VBO = glGenBuffers(1)
glBindVertexArray(grid_VAO)
glBindBuffer(GL_ARRAY_BUFFER, grid_VBO)
glBufferData(GL_ARRAY_BUFFER, grid_lines_vertices.nbytes, grid_lines_vertices, GL_STATIC_DRAW)

# Position attribute
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)
# Color attribute
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)



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
uniform mat4 model;
out vec3 ourColor;
void main()
{
   gl_Position = model * vec4(aPos, 1.0);
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

    # Clear the screen
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Generate and pass the rotation matrix to the shader
    rotation_matrix = get_rotation_matrix(rotation_x, rotation_y)
    model_loc = glGetUniformLocation(shader, "model")
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(rotation_matrix))

    # Draw the cube
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    glBindVertexArray(grid_VAO)
    glDrawArrays(GL_LINES, 0, len(grid_lines_vertices) // 6)  # Adjust count based on your vertices
    glBindVertexArray(0)
    glLineWidth(2.0)  # Set line width to 2 pixels
    glfw.swap_buffers(window)


# Terminate glfw
glfw.terminate()
