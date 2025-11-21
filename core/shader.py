from OpenGL.GL import *
import glm

class Shader:
    def __init__(self, vertex_path, fragment_path):       
        with open(vertex_path, 'r') as f:
            vertex_src = f.read()
        with open(fragment_path, 'r') as f:
            fragment_src = f.read()

        self.program = glCreateProgram()

        vertex_shader = self._compile_shader(vertex_src, GL_VERTEX_SHADER)
        fragment_shader = self._compile_shader(fragment_src, GL_FRAGMENT_SHADER)

        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)

        if glGetProgramiv(self.program, GL_LINK_STATUS) != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(self.program))

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    def _compile_shader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            error = glGetShaderInfoLog(shader)
            raise RuntimeError(f"Erro ao compilar shader: {error}")

        return shader

    def use(self):
        glUseProgram(self.program)

    def set_int(self, name, value):
        loc = glGetUniformLocation(self.program, name)
        glUniform1i(loc, value)

    def set_float(self, name, value):
        loc = glGetUniformLocation(self.program, name)
        glUniform1f(loc, value)

    def set_vec3(self, name, vec):
        loc = glGetUniformLocation(self.program, name)
        glUniform3f(loc, vec[0], vec[1], vec[2])

    def set_mat4(self, name, mat):
        loc = glGetUniformLocation(self.program, name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, glm.value_ptr(mat))
