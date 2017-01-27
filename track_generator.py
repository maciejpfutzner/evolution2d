"""
Module for creating the racing tracks each of which is an instance of class Track.
Allows to create a flat block, series of slopes or a continuous track with
parametrised roughness. Class method build the track as a series of box2d polygons.

TODO:
    Write class docstrings!
    Review and delete commented code
    Parametrise roughness
"""

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)
import random
from datetime import datetime
import math

class Track:
    def __init__(self, length, roughness=0, seed=None):
        self.length = length
        self.roughness = roughness
        self.seed = seed
        self.generated = False
        self.generate()

    def generate(self):
        if self.seed:
            random.seed(seed)
        else:
            random.seed(datetime.now())

        if self.roughness == 0:
            self.gen_flat()
        elif self.roughness == 1:
            self.gen_slopes()
        else:
            self.gen_rough()

    def build(self, world):
        if not self.generated:
            return None

        start = 0
        self.bodies = []
        for i in xrange(self.n_segments):
            body = world.CreateStaticBody(
                    position=self.seg_positions[i],
                    angle=self.seg_angles[i],
                    shapes=polygonShape(
                        box=(self.seg_lengths[i]/2., 1)))
            start += self.seg_lengths[i]
            self.bodies.append(body)

        return self.length


    def gen_flat(self):
        self.n_segments = 1
        self.seg_lengths = [self.length]
        self.seg_angles = [0]
        self.seg_positions = [(0,3)]
        self.generated = True

    def gen_slopes(self):
        seg_len = 30
        nn = self.length/seg_len
        self.n_segments = nn
        self.seg_lengths = [seg_len for x in xrange(nn)]
        self.seg_angles = [0.15 for x in xrange(nn)]
        self.seg_positions = [(0.9*seg_len*x,3) for x in xrange(nn)]
        self.generated = True

    #TODO: roughness
    def gen_rough(self):
        nn = self.length/15
        self.n_segments = nn
        self.seg_lengths = [0]*nn
        self.seg_angles = [0]*nn
        self.seg_positions = [0]*nn
        for i in xrange(nn):
            self.seg_lengths[i] = 15
            angle = random.uniform(-0.2, 0.2)
            self.seg_angles[i] = angle
            px = i*15 + 15*math.cos(angle)
            py = 5 + 15*math.sin(angle)
            self.seg_positions[i] = (px, py)
        self.generated = True


#l = 10;
#h = 1;
#angle = 0.4;
#px = 10;
#py = 10;
#angle = 0;
#for i in range(0,10):
#   body = world.CreateStaticBody(
#           position=(px, py),
#           angle=angle,
#           shapes=polygonShape(box=(l, h)),
#           )
#   angle = random.uniform(-0.2,0.2);
#   # l = l + random.uniform(-5,5)
#   px = px + l + l*math.cos(angle);
#   py = py + h + l*math.sin(angle);
