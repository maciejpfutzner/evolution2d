import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

class Track:
    def __init__(self, length, roughness=0):
        self.length = length
        self.roughness = roughness
        self.generated = False
        self.generate()

    def generate(self):
        #TODO: make actual algorithm, now just a flat track with length
        self.n_segments = 1
        self.seg_lengths = [self.length]
        self.seg_angles = [0]
        self.generated = True

    def build(self, world):
        if not self.generated:
            return None

        self.bodies = []
        start = 0
        for i in xrange(self.n_segments):
            body = world.CreateStaticBody(
                    position=(start,0),
                    angle=self.seg_angles[i],
                    shapes=polygonShape(box=(self.seg_lengths[i], 1)))
            start += self.seg_lengths[i]




