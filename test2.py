#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An attempt at some simple, self-contained pygame-based examples.
Example 02

In short:
One static body:
    + One fixture: big polygon to represent the ground
Two dynamic bodies:
    + One fixture: a polygon
    + One fixture: a circle
And some drawing code that extends the shape classes.

kne
"""
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 4.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0, -10), doSleep=True)

# And a static body to hold the ground shape
ground_body = world.CreateStaticBody(
    position=(0, 50),
    angle=-0.0,
    shapes=polygonShape(box=(150, 1)),
)

width = 10
height = 3
radius1 = 3.3
radius2 = 3.4
wheel_friction = 0.5

x0, y0 = 10, 55

# Create a couple dynamic bodies
carriage = world.CreateDynamicBody(position=(x0, y0))
box = carriage.CreatePolygonFixture(box=(width, height), density=1, friction=0.3)

wheel1 = world.CreateDynamicBody(position=(x0-width*0.95, y0-height*0.45))
circle = wheel1.CreateCircleFixture(radius=radius1, density=1, friction=wheel_friction)
joint1 = world.CreateRevoluteJoint(bodyA=carriage, bodyB=wheel1, anchor = wheel1.worldCenter)

wheel2 = world.CreateDynamicBody(position=(x0+width*0.95, y0-height*0.45))
circle = wheel2.CreateCircleFixture(radius=radius2, density=1, friction=wheel_friction)
joint2 = world.CreateRevoluteJoint(bodyA=carriage, bodyB=wheel2, anchor = wheel2.worldCenter,
        maxMotorTorque = 1550.0, motorSpeed = -50.0, enableMotor = True)

#body1 = world.CreateDynamicBody(position=(15, 45))
#box = body1.CreatePolygonFixture(box=(3, 1), density=1, friction=0.3)
#body2 = world.CreateDynamicBody(position=(12, 45), angle=-15)
#box = body2.CreatePolygonFixture(box=(3, 1), density=1, friction=0.3)
#joint = world.CreateRevoluteJoint(bodyA=body1, bodyB=body2, anchor=(12,45))


colors = {
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255),
}

# Let's play with extending the shape classes to draw for us.


def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)
polygonShape.draw = my_draw_polygon


def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[body.type], [int(
        x) for x in position], int(circle.radius * PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.
circleShape.draw = my_draw_circle

# --- main game loop ---

running = True
while running:
    # Check the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            running = False

    screen.fill((0, 0, 0, 0))
    # Draw the world
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)

    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)

    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

    #print carriage.position

pygame.quit()
print('Done!')
