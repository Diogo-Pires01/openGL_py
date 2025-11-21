import glfw
from OpenGL.GL import *

class Window:
    def __init__(self, width=1280, height=720, title="A3 OpenGL + Python"):
        if not glfw.init():
            raise Exception("Erro ao inicializar GLFW")

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Erro ao criar a janela")

        glfw.make_context_current(self.window)

        glfw.set_key_callback(self.window, self.key_callback)
        
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.2, 0.3, 0.4, 1.0)

        self.width = width
        self.height = height

    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def poll_events(self):
        glfw.poll_events()

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

    def terminate(self):
        glfw.terminate()

