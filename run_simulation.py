import shelve
import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)


#TODO: tweak those, maybe pass them to setup
min_move = 0.5 #min move before we say, we're stuck [m]
max_stuck_time = 2 #max time being stuck before we finish [s]

#TODO: tweak setup, fix bugs, get a cleaning up function...

class Simulation:
    def __init__(self, track, vehicle, save=False):
        self.track = track
        self.vehicle = vehicle

        # Create the world
        self.sim_world = world(gravity=(0, -10), doSleep=True)
        # Create the track (static ground body)
        self.track.build(self.sim_world)

        #TODO: figure out spawning position that's always just above the track
        # - could be part of the track class
        x0, y0 = 5, 10
        # TODO: make the tracker a property returning just the position!
        self.tracker = self.vehicle.build(self.sim_world, x0, y0)
        self.starting_position = self.tracker.worldCenter[0] #just x coordinate

        # Only init history after track was built
        self.history = StateHistory(self) if save else None

    #returns dist covered and whether it is over (bool)
    def run(self, n_iter=-1, speed=1.):
        stuck_time = 0

        #FIXME: unfortunately speed affects physics...
        time_step = speed/60. #60 Hz by default
        vel_iters, pos_iters = 6, 2 #apparently good
        i = 0
        while True:
            self.sim_world.Step(time_step, vel_iters, pos_iters)
            if self.history: self.history.save_state()

            #check if we're moving forward
            position = self.tracker.worldCenter[0]
            distance = position - self.starting_position
            if distance < min_move:
                stuck_time += time_step
            else:
                stuck_time = 0

            # if we're stuck for too long finish the loop
            if stuck_time > max_stuck_time:
                print "Stuck in one place"
                return distance, True, n_iter

            i+= 1
            if n_iter>0 and i > n_iter:
                print "Reached max time", n_iter*time_step, "s"
                return distance, False, n_iter

            if self.tracker.worldCenter[1] < 0:

                print "Fell off the cliff"
                return distance, True, n_iter

        #return final distance
        print "Normal"
        return (distance, False, n_iter)


# TODO: a single state should also be a class instead of collection of lists
class StateHistory:
    def __init__(self, simulation):
        self.sim = simulation
        self.track = self.get_objects(self.sim.track)
        self.vehicle_states = []
        self.tracker_states = []

    def save_state(self):
        objects = self.get_objects(self.sim.vehicle)
        self.vehicle_states.append(objects)
        tracker = tuple(self.sim.tracker.worldCenter)
        self.tracker_states.append(tracker)

    def write_to_file(self, name, filename):
        #open file for storing the history
        shelf = shelve.open(filename)
        self.name = name
        shelf.setdefault('histories', [])
        hist_list = shelf['histories']
        hist_list.append(history)
        shelf['histories'] = hist_list
        shelf.close()

    def get_objects(self, instance):
        objects = []
        for body in instance.bodies:
            for fixture in body:
                objects.append( fixture.shape.get_params(body) )
        return objects


# FIXME: do this more elegantly?...
def get_params_polygon(polygon, body):
    vertices = [tuple(body.transform * v) for v in polygon.vertices]
    return 'polygon', vertices
polygonShape.get_params = get_params_polygon

def get_params_circle(circle, body):
    position = tuple(body.transform * circle.pos)
    radius = circle.radius
    return 'circle', (position, radius)
circleShape.get_params = get_params_circle

