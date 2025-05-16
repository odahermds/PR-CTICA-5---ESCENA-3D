from OpenGL.GL import *

def init_lighting():
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (4.0,4.0,6.0,1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.2,0.2,0.2,1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (0.7,0.7,0.7,1))
    glMaterialfv(GL_FRONT,GL_SPECULAR,(1,1,1,1))
    glMaterialfv(GL_FRONT,GL_SHININESS,50)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, (-4.0, 4.0, 6.0, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  (0.5, 0.5, 0.8, 1))
    glLightfv(GL_LIGHT1, GL_AMBIENT,  (0.1, 0.1, 0.1, 1))

def rotate_arbitrary_axis(angle, axis_x, axis_y, axis_z):
    glRotatef(angle, axis_x, axis_y, axis_z)

def draw_shadow(shape, light_pos, ground_level=-3.0):
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glColor4f(0.1, 0.1, 0.1, 0.5)

    shadow_mat = [0]*16
    dot = light_pos[1]  # y * 1

    for i in range(4):
        for j in range(4):
            if i == j:
                shadow_mat[i*4+j] = dot - light_pos[j] if i == 1 else dot
            else:
                shadow_mat[i*4+j] = -light_pos[j] if i == 1 else 0

    glPushMatrix()
    glTranslatef(0, ground_level, 0)
    glMultMatrixf(shadow_mat)

    shape.draw()

    glPopMatrix()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glColor4f(1, 1, 1, 1)
