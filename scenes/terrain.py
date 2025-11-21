from OpenGL.GL import *
import numpy as np
import glm
from PIL import Image

class Terrain:
    def __init__(self, width, depth, resolution):
        self.vertices = self.generate(width, depth, resolution)
        self.vertex_count = len(self.vertices)

        self.texture = self.load_texture("assets/textures/grass.png")

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        stride = 5 * 4

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

    def generate(self, width, depth, res):
        x = np.linspace(-width/2, width/2, res)
        z = np.linspace(-depth/2, depth/2, res)
        verts = []

        for i in range(res - 1):
            for j in range(res - 1):
                x0, z0 = x[i], z[j]
                x1, z1 = x[i+1], z[j+1]

                u0, v0 = i / res * 10, j / res * 10
                u1, v1 = (i+1) / res * 10, (j+1) / res * 10

                verts.extend([
                    [x0, 0, z0, u0, v0],
                    [x1, 0, z0, u1, v0],
                    [x1, 0, z1, u1, v1],

                    [x0, 0, z0, u0, v0],
                    [x1, 0, z1, u1, v1],
                    [x0, 0, z1, u0, v1],
                ])

        return np.array(verts, dtype=np.float32)

    def load_texture(self, path):
        img = Image.open(path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

        img_data = img.convert("RGBA").tobytes()

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                     img.width, img.height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        return texture

    def render(self, shader):
        glBindVertexArray(self.vao)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        shader.set_int("texture1", 0)

        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
