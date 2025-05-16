from OpenGL.GL import *
import pygame
import math

class Piramide:
    def __init__(self, size=1.0):
        self.size = size
        self.texture = None

    def load_texture(self, surface):
        tex_data = pygame.image.tostring(surface, "RGB", True)
        w, h = surface.get_size()
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, tex_data)

    def draw(self):
        s = self.size / 2
        glBindTexture(GL_TEXTURE_2D, self.texture)
        faces = [
            ((0,math.sqrt(2)/2, math.sqrt(2)/2), [(0,s,0),(-s,-s,s),(s,-s,s)]),
            ((math.sqrt(2)/2,math.sqrt(2)/2,0), [(0,s,0),(s,-s,s),(s,-s,-s)]),
            ((0,math.sqrt(2)/2,-math.sqrt(2)/2),[(0,s,0),(s,-s,-s),(-s,-s,-s)]),
            ((-math.sqrt(2)/2,math.sqrt(2)/2,0),[(0,s,0),(-s,-s,-s),(-s,-s,s)])
        ]
        for normal, verts in faces:
            glBegin(GL_TRIANGLES)
            glNormal3f(*normal)
            for i, v in enumerate(verts):
                u = 0.5 if i==0 else (0 if v[0]<0 else 1)
                vtex = 1 if i==0 else 0
                glTexCoord2f(u, vtex)
                glVertex3f(*v)
            glEnd()
        glBegin(GL_QUADS)
        glNormal3f(0,-1,0)
        base = [(-s,-s,s),(s,-s,s),(s,-s,-s),(-s,-s,-s)]
        for i, v in enumerate(base):
            glTexCoord2f(i%2, i//2)
            glVertex3f(*v)
        glEnd()
