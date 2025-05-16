from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

class Esfera:
    def __init__(self, radius=1.0):
        self.radius = radius
        self.texture = None
        self.quad = gluNewQuadric()
        gluQuadricTexture(self.quad, GL_TRUE)

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
        gluSphere(self.quad, self.radius, 32, 32)
