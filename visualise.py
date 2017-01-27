"""
Simple visualisation using pygame.

TODO:
    Should initialise the pygame screen, open the saved state history of a
    single run, and draw the subsequent physics frames. Might need some
    tinkering to recreate polygon and circle objects from pure python lists of
    vertices/ circle positions that is stored in the history. The animation
    should follow the main object (tricky?)
"""

import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_RETURN)

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 10.0  # pixels per meter
TARGET_FPS = 60 #60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

bkg_color = (0,0,0,0)
obj_color = (255, 255, 255, 255)

def start_game():
    pygame.display.init()
    global screen
    # --- pygame setup ---
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Race visualisation')
    global clock
    clock = pygame.time.Clock()


def draw_polygon(vertices, shift=0):
    vertices = [[int(pos * PPM) for pos in v] for v in vertices]
    shift *= PPM
    vertices = [(v[0]+shift, SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, obj_color, vertices)


def draw_circle(position, radius, shift=0):
    position = [pos * PPM for pos in position]
    radius = int(radius*PPM)
    shift *= PPM
    position = (int(position[0]+shift), int(SCREEN_HEIGHT - position[1]))
    pygame.draw.circle(screen, obj_color, position, radius)


def draw_history(history, index):
    tracker = history.tracker_states[index]
    shift = 20 - tracker[0] # tracker's X position
    objects = history.track + history.vehicle_states[index]
    drawing_func(objects, shift)


def drawing_func(objects, shift):
    screen.fill(bkg_color)
    # now draw the rest
    for obj in objects:
        if obj[0] == 'polygon':
            draw_polygon(obj[1], shift)
        if obj[0] == 'circle':
            draw_circle(obj[1][0], obj[1][1], shift)

    # Update the screen
    pygame.display.flip()


def run(history, speed=1.):
    draw_history(history, 0)

    start = False
    while not start:
        event = pygame.event.wait()
        if event.type == KEYDOWN and event.key == K_RETURN:
            start = True
        elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            #pygame.quit()
            return

    running = True
    n_states = len(history.vehicle_states)
    istate = 0

    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # The user closed the window or pressed escape
                running = False

        istate += int(speed)
        if istate >= n_states:
            running = False
            continue

        draw_history(history, istate)
        clock.tick(TARGET_FPS)

    #pygame.quit()


def quit_game():
    pygame.display.quit()
    pygame.quit()
