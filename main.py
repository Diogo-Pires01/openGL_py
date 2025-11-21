from core.window import Window
from core.shader import Shader
from core.camera import Camera
from scenes.terrain import Terrain
from OpenGL.GL import *
import glm
import glfw

def main():
    window = Window(1280, 720, "Terreno OpenGL Modular")
    camera = Camera()
    shader = Shader("assets/shaders/terrain.vert", "assets/shaders/terrain.frag")
    terreno = Terrain(width=300, depth=300, resolution=150)

    glfw.set_cursor_pos_callback(window.window, camera.mouse_callback)
    glfw.set_input_mode(window.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    while not window.should_close():
        window.poll_events()
        camera.process_input(window.window)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        shader.use()
        shader.set_int("texture1", 0)

        model = glm.mat4(1.0)
        projection = glm.perspective(glm.radians(45.0), window.width / window.height, 0.1, 100.0)
        view = camera.get_view_matrix()

        shader.set_mat4("model", model)
        shader.set_mat4("view", view)
        shader.set_mat4("projection", projection)

        terreno.render(shader)

        window.swap_buffers()

    window.terminate()

if __name__ == "__main__":
    main()
