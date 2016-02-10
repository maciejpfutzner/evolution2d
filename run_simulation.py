import shelve
import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)


#TODO: tweak those, maybe pass them to setup
min_move = 0.1 #min move before we say, we're stuck [m]
max_stuck_time = 10 #max time being stuck before we finish [s]

#TODO: tweak setup, fix bugs, get a cleaning up function...


def setup_sim(vehicle, track):
    # --- pybox2d world setup ---
    # Create the world
    global sim_world
    sim_world = world(gravity=(0, -10), doSleep=True)

    #create the track (static ground body)
    track.build(sim_world)

    #TODO: figure out spawning position that's always just above the track
    x0, y0 = 10, 55

    #tracker - an object to ask for position
    global tracker
    tracker = vehicle.build(sim_world, x0, y0)

def run_sim(ext_func=None):
    starting_position = tracker.position[0] #just x coordinate
    stuck_time = 0

    time_step = 1./60 #60 Hz
    vel_iters, pos_iters = 6, 2 #apparently good
    while True:
        sim_world.Step(time_step, vel_iters, pos_iters)

        #check if we're moving forward
        position = tracker.position[0]
        if position - starting_position < min_move:
            stuck_time += time_step
        else:
            stuck_time = 0

        # if we're stuck for too long finish the loop
        if stuck_time > max_stuck_time:
            break

        #This is supposed to be used when debugging,
        #e.g. to draw from inside of this loop
        if ext_func:
            ext_func()

    #return final distance
    return position - starting_position


#TODO: incorporate this into the setup_sim and run_sim functions...
class StateHistory:
    pass
history = StateHistory()
history.objects = [] #FIXME: clean at setup_sim

def save_state():
    objects = []
    for body in sim_world.bodies:
        for fixture in body:
            objects.append( fixture.shape.get_params(body) )
    history.objects.append(objects)

def save_state_history(name, filename):
    #open file for storing the history
    shelf = shelve.open(filename)
    history.name = name
    shelf.setdefault('histories', [])
    hist_list = shelf['histories']
    hist_list.append(history)
    shelf['histories'] = hist_list
    shelf.close()


def get_params_polygon(polygon, body):
    vertices = [tuple(body.transform * v) for v in polygon.vertices]
    return 'polygon', vertices
polygonShape.get_params = get_params_polygon

def get_params_circle(circle, body):
    position = tuple(body.transform * circle.pos)
    radius = circle.radius
    return 'circle', (position, radius)
circleShape.get_params = get_params_circle

