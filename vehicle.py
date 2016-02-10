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


class Car(Vehicle):
    def __init__(self):
        Vehicle.__init__(self, 'Car')
        self.genome = { 'wheel1_r' : 0,
                        'wheel2_r' : 0,
                        'body_length' : 0,
                        'body_width' : 0 }

    def random_genome(self):
        for key in self.genome:
            gene = self.genome[key]
            x = random.random()
            gene = 2*x # sizes from 0 to 2 metres
            if key == 'body_width':
                # body length is from 2 to 6 m
                gene +=1
                gene *= 2 
            self.genome[key] = gene

    def build(self, world, x0, y0):
        width = self.genome['body_length']
        height = self.genome['body_width']
        radius1 = self.genome['wheel1_r']
        radius2 = self.genome['wheel2_r']

        wheel_friction = 0.5
        max_torque = 1e3
        speed = -100

        # Create a couple dynamic bodies
        carriage = world.CreateDynamicBody(position=(x0, y0))
        carriage.CreatePolygonFixture(box=(width, height), density=1, friction=0.3)

        wheel1 = world.CreateDynamicBody(position=(x0-width*0.95, y0-height*0.85))
        wheel1.CreateCircleFixture(radius=radius1, density=1, friction=wheel_friction)
        world.CreateRevoluteJoint(bodyA=carriage, bodyB=wheel1,
                anchor = wheel1.worldCenter,
                maxMotorTorque = max_torque, motorSpeed = speed,
                enableMotor = True)

        wheel2 = world.CreateDynamicBody(position=(x0+width*0.95, y0-height*0.85))
        wheel2.CreateCircleFixture(radius=radius2, density=1, friction=wheel_friction)
        world.CreateRevoluteJoint(bodyA=carriage, bodyB=wheel2,
                anchor = wheel2.worldCenter,
                maxMotorTorque = max_torque, motorSpeed = speed,
                enableMotor = True)

        # return the body object for tracking position
        return carriage




