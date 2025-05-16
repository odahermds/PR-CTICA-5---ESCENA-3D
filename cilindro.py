from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

class Cilindro:
    def __init__(self, base=1.0, top=1.0, height=2.0):
        self.base = base
        self.top = top
        self.height = height
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
        glPushMatrix()
        glRotatef(-90,1,0,0)
        gluCylinder(self.quad, self.base, self.top, self.height, 32, 16)
        gluDisk(self.quad, 0, self.base, 32, 1)
        glTranslatef(0,0,self.height)
        gluDisk(self.quad, 0, self.top, 32, 1)
        glPopMatrix()
