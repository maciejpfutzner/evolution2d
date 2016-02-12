#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An attempt at some simple, self-contained pygame-based examples.

Example 01

In short:
One static body: a big polygon to represent the ground
One dynamic body: a rotated big polygon
And some drawing code to get you going.

kne
"""
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE, K_RETURN)

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

import run_simulation as sim
import track_generator
import vehicle

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 10.0  # pixels per meter
TARGET_FPS = 60 #60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


def start_game(car=None, track=None):
    global screen
    # --- pygame setup ---
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Simple pygame example')
    global clock
    clock = pygame.time.Clock()

    if not car:
        car = vehicle.Car()
        car.random_genome()
    if not track:
        track = track_generator.Track(200) #200 m length
    sim.setup_sim(car, track)


colors = {
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255),
}

def my_draw_polygon(polygon, body, fixture, shift=0):
    shift *= PPM
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0]+shift, SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)
polygonShape.draw = my_draw_polygon


def my_draw_circle(circle, body, fixture, shift=0):
    shift *= PPM
    position = (body.transform * circle.pos) * PPM
    position = (position[0]+shift, SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[body.type], [int(
        x) for x in position], int(circle.radius * PPM))
circleShape.draw = my_draw_circle

# --- main game loop ---


def drawing_func(shift=0):
    world = sim.sim_world

    screen.fill((0, 0, 0, 0))
    # Draw the world
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture, shift)

    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()


def run(speed=1.):
    drawing_func()

    start = False
    while not start:
        event = pygame.event.wait()
        if event.type == KEYDOWN and event.key == K_RETURN:
            start = True
        elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            return


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # The user closed the window or pressed escape
                running = False

        dist, is_over, ii= sim.run_sim(1)
        print dist, is_over
        drawing_func(-dist+20)
        clock.tick(int(TARGET_FPS/float(speed)))
        if is_over:
            running = False

    pygame.quit()

