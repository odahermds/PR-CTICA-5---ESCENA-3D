import sys
import os
import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from cubo import Cubo
from piramide import Piramide
from esfera import Esfera
from cilindro import Cilindro
from superelipsoide import Superelipsoide
from utilidades import init_lighting, rotate_arbitrary_axis, draw_shadow

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Práctica 5 - Escena 3D Realista")

    glClearColor(0.1, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    init_lighting()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    tex_path = os.path.join(script_dir, 'textura.jpg')
    if not os.path.exists(tex_path):
        print(f"Error: 'textura.jpg' no encontrado en {script_dir}")
        sys.exit(1)
    tex_surf = pygame.image.load(tex_path)

    shapes = [Cubo(), Piramide(), Esfera(), Cilindro(), Superelipsoide()]
    for s in shapes:
        if hasattr(s, 'load_texture'):
            s.load_texture(tex_surf)

    projection = 'perspective'
    selected = None
    transforms = {
        'rot': [0, 0],
        'trans': [0, 0, 0],
        'scale': 1.0,
        'arb_rot': {'angle': 0, 'axis': [1, 1, 1]},
        'rotation_mode': 'global'
    }
    lighting = True
    textured = True
    show_shadow = False
    light_pos = [4.0, 4.0, 6.0, 1.0]

    menu = [
        "MENÚ", "", "1) Mostrar Cubo", "", "2) Mostrar Pirámide", "",  "3) Mostrar Esfera",
        "", "4) Mostrar Cilindro", "", "5) Mostrar Superelipsoide", "", "6) Salir"
    ]
    font = pygame.font.SysFont('Times New Roman', 30)

    def set_projection():
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if projection == 'perspective':
            gluPerspective(45, display[0]/display[1], 0.1, 50)
        else:
            glOrtho(-5, 5, -5, 5, -50, 50)
        glMatrixMode(GL_MODELVIEW)

    set_projection()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_1: selected = 0
                elif event.key == K_2: selected = 1
                elif event.key == K_3: selected = 2
                elif event.key == K_4: selected = 3
                elif event.key == K_5: selected = 4
                elif event.key == K_6:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_r:
                    transforms = {
                        'rot': [0, 0],
                        'trans': [0, 0, 0],
                        'scale': 1.0,
                        'arb_rot': {'angle': 0, 'axis': [1, 1, 1]},
                        'rotation_mode': transforms['rotation_mode']
                    }
                elif event.key == K_p:
                    projection = 'perspective' if projection == 'ortho' else 'ortho'
                    set_projection()
                elif event.key == K_i:
                    lighting = not lighting
                    if lighting:
                        glEnable(GL_LIGHTING)
                        glEnable(GL_LIGHT0)
                        glEnable(GL_LIGHT1)
                    else:
                        glDisable(GL_LIGHTING)
                elif event.key == K_t:
                    textured = not textured
                    if textured:
                        glEnable(GL_TEXTURE_2D)
                    else:
                        glDisable(GL_TEXTURE_2D)
                elif event.key == K_h:
                    show_shadow = not show_shadow
                elif event.key == K_m:
                    transforms['rotation_mode'] = 'local' if transforms['rotation_mode'] == 'global' else 'global'
                elif event.unicode == '+':
                    transforms['scale'] *= 1.05
                elif event.unicode == '-':
                    transforms['scale'] /= 1.05
                elif event.key == K_7:
                    transforms['arb_rot']['axis'] = [1, 0, 0]
                    transforms['arb_rot']['angle'] += 5
                elif event.key == K_8:
                    transforms['arb_rot']['axis'] = [0, 1, 0]
                    transforms['arb_rot']['angle'] += 5
                elif event.key == K_9:
                    transforms['arb_rot']['axis'] = [0, 0, 1]
                    transforms['arb_rot']['angle'] += 5
                elif event.key == K_ESCAPE:
                    selected = None
                    transforms = {
                        'rot': [0, 0],
                        'trans': [0, 0, 0],
                        'scale': 1.0,
                        'arb_rot': {'angle': 0, 'axis': [1, 1, 1]},
                        'rotation_mode': 'global'
                    }

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]: transforms['rot'][1] -= 1
        if keys[K_RIGHT]: transforms['rot'][1] += 1
        if keys[K_UP]: transforms['rot'][0] -= 1
        if keys[K_DOWN]: transforms['rot'][0] += 1
        if keys[K_w]: transforms['trans'][1] += 0.1
        if keys[K_s]: transforms['trans'][1] -= 0.1
        if keys[K_a]: transforms['trans'][0] -= 0.1
        if keys[K_d]: transforms['trans'][0] += 0.1
        if keys[K_q]: transforms['trans'][2] -= 0.1
        if keys[K_e]: transforms['trans'][2] += 0.1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

        if selected is None:
            glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
            glOrtho(0, display[0], 0, display[1], -1, 1)
            glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
            glDisable(GL_TEXTURE_2D)
            for i, line in enumerate(menu):
                if not line: continue
                surf = font.render(line, True, (255, 255, 255)).convert_alpha()
                x = (display[0] - surf.get_width()) // 2
                y = display[1] - 110 - i * 35
                glRasterPos2f(x, y)
                data = pygame.image.tostring(surf, "RGBA", True)
                glDrawPixels(surf.get_width(), surf.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, data)
            glPopMatrix()
            glMatrixMode(GL_PROJECTION); glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glEnable(GL_TEXTURE_2D)
        else:
            glTranslatef(*transforms['trans'])
            glScalef(transforms['scale'], transforms['scale'], transforms['scale'])

            if transforms['rotation_mode'] == 'global':
                glRotatef(transforms['rot'][0], 1, 0, 0)
                glRotatef(transforms['rot'][1], 0, 1, 0)
                rotate_arbitrary_axis(
                    transforms['arb_rot']['angle'],
                    *transforms['arb_rot']['axis']
                )
            else:
                rotate_arbitrary_axis(
                    transforms['arb_rot']['angle'],
                    *transforms['arb_rot']['axis']
                )
                glRotatef(transforms['rot'][1], 0, 1, 0)
                glRotatef(transforms['rot'][0], 1, 0, 0)

            if show_shadow:
                draw_shadow(shapes[selected], light_pos)

            shapes[selected].draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
