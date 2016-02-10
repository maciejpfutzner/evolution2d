import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)
import random

#TODO: actual seed
random.seed(22)

class Vehicle:
    def __init__(self, type_name):
        self.type_name = type_name
        self.genome = {}

    def random_genome(self):
        pass

    def build(self, world):
        pass

    def get_child(self, mutation_rate, mutation_range):
        child = Vehicle(self.type_name)
        child.genome = self.genome
        for key in child.genome:
            prob = random.random()
            #mutate if lucky
            if prob < mutation_rate:
                #change is from -100% to +100% of the gene's value
                change = 2.*random.random()-1.
                gene = child.genome[key]
                gene += change*gene
                child.genome[key] = gene

        return child



