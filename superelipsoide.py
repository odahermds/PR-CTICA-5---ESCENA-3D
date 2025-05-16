from OpenGL.GL import *
import math
import pygame

class Superelipsoide:
    def __init__(self, a=1, b=1, c=1, n1=0.5, n2=1.0):
        self.a, self.b, self.c = a, b, c
        self.n1, self.n2 = n1, n2
        self.texture = None

    def sign(self, v): return math.copysign(1, v)
    def fexp(self, base, exp): return self.sign(base) * (abs(base)**exp)

    def load_texture(self, surface):
        tex_data = pygame.image.tostring(surface, "RGB", True)
        w, h = surface.get_size()
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, tex_data)

    def draw(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        stacks, slices = 32, 32
        for i in range(stacks):
            phi0 = math.pi * (i / stacks - 0.5)
            phi1 = math.pi * ((i + 1) / stacks - 0.5)
            glBegin(GL_TRIANGLE_STRIP)
            for j in range(slices + 1):
                theta = 2 * math.pi * j / slices
                for phi, t in zip((phi0, phi1), (i / stacks, (i + 1) / stacks)):
                    x = self.a * self.fexp(math.cos(phi), self.n1) * self.fexp(math.cos(theta), self.n2)
                    y = self.b * self.fexp(math.cos(phi), self.n1) * self.fexp(math.sin(theta), self.n2)
                    z = self.c * self.fexp(math.sin(phi), self.n1)
                    u = j / slices
                    v = t
                    glTexCoord2f(u, v)
                    glVertex3f(x, y, z)
            glEnd()
