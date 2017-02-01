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

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, edgeShape, shape, vec2)

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 10.0  # pixels per meter
TARGET_FPS = 60 #60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 744

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


# Remember to pass a list, even if single vertex
def shift_scale_revert(vertices, shift):
    """
    Take vertices and shift them, scale to pixel values and revert y coordinate
    for pygame drawing. Remember to pass a list of vertices even if one element.
    Return vertices as tuples (not vec2 anymore)
    """
    for i, vert in enumerate(vertices):
        vert = vec2(vert) + shift
        vert = [int(pos*PPM) for pos in vert]
        vert[1] = SCREEN_HEIGHT - vert[1]
        vertices[i] = tuple(vert)
    return vertices


# simple drawing (from defined points)
def draw_polygon(vertices, shift=(0,0), color=obj_color, width=0):
    vertices = shift_scale_revert(vertices, shift)
    pygame.draw.polygon(screen, color, vertices, width)

def draw_circle(position, radius, shift=(0,0), color=obj_color, width=0):
    position = shift_scale_revert([position], shift)
    radius = int(radius*PPM)
    pygame.draw.circle(screen, color, position, radius, width)


# shape drawing
def draw_polygonShape(polygon, shift=(0,0), color=obj_color, width=0):
    vertices = shift_scale_revert(polygon.vertices, shift)
    pygame.draw.polygon(screen, color, vertices, width)
polygonShape.draw = draw_polygonShape

def draw_circleShape(circle, shift=(0,0), color=obj_color, width=0):
    position = shift_scale_revert([circle.pos], shift)[0]
    radius = int(circle.radius*PPM)
    pygame.draw.circle(screen, color, position, radius, width)
circleShape.draw = draw_circleShape

def draw_edgeShape(edge, shift=(0,0), color=obj_color, width=1):
    vertices = shift_scale_revert(edge.vertices, shift)
    pygame.draw.line(screen, color, vertices[0], vertices[1], width)
edgeShape.draw = draw_edgeShape


def draw_history(history, timelines, index):
    first = timelines[0]
    tracker = history.timelines[first].tracker_states[index]
    shift = vec2(20,20) - tracker
    objects = []
    objects += history.track
    for time in timelines:
        objects += history.timelines[time].vehicle_states[index]
    print len(objects)
    drawing_func(objects, shift)


def drawing_func(objects, shift):
    screen.fill(bkg_color)
    # now draw the rest
    for obj in objects:
        # if the passed object is a b2Shape, draw it shape-wise
        if isinstance(obj, shape):
            obj.draw(shift)
        # otherwise, use the simple method based on the name
        elif obj[0] == 'polygon':
            draw_polygon(obj[1], shift)
        elif obj[0] == 'circle':
            draw_circle(obj[1][0], obj[1][1], shift)

    # Update the screen
    pygame.display.flip()


def run(history, timelines, speed=1.):
    draw_history(history, timelines, 0)

    start = False
    while not start:
        event = pygame.event.wait()
        if event.type == KEYDOWN and event.key == K_RETURN:
            start = True
        elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            #pygame.quit()
            return

    running = True
    n_states = history.max_length
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

        draw_history(history, timelines, istate)
        clock.tick(TARGET_FPS)

    #pygame.quit()


def quit_game():
    pygame.display.quit()
    pygame.quit()
