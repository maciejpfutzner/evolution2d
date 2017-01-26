import shelve
import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)


#TODO: tweak those, maybe pass them to setup
min_move = 0.5 #min move before we say, we're stuck [m]
max_stuck_time = 2 #max time being stuck before we finish [s]

#TODO: tweak setup, fix bugs, get a cleaning up function...


def setup_sim(vehicle, track):
    # --- pybox2d world setup ---
    # Create the world
    global sim_world
    sim_world = world(gravity=(0, -10), doSleep=True)

    #create the track (static ground body)
    global length
    length = track.build(sim_world)

    #TODO: figure out spawning position that's always just above the track
    # - could be part of the track class
    x0, y0 = 5, 10

    #tracker - an object to ask for position
    global tracker
    tracker = vehicle.build(sim_world, x0, y0)
    global starting_position
    starting_position = tracker.worldCenter[0] #just x coordinate

    history.objects = [] # zero the state history


#returns dist covered and whether it is over (bool)
def run_sim(n_iter=-1, speed=1., save=False):
    stuck_time = 0

    #FIXME: unfortunately speed affects physics...
    time_step = speed/60. #60 Hz by default
    vel_iters, pos_iters = 6, 2 #apparently good
    i = 0
    while True:
        sim_world.Step(time_step, vel_iters, pos_iters)
        if save: save_state()

        #check if we're moving forward
        position = tracker.worldCenter[0]
        distance = position - starting_position
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

        if tracker.worldCenter[1] < 0:
            print "Fell off the cliff"
            return distance, True, n_iter

    #return final distance
    print "Normal"
    return (distance, False, n_iter)


#TODO: Rewrite this whole thing! Use classes instead of tuples with the name as
#       first element!!!
#   Also, we can't really store the whole state for each iteration, at least keep the track separately
class StateHistory:
    pass
history = StateHistory()
history.objects = [] #FIXME: clean at setup_sim

def save_state():
    objects = []
    for body in sim_world.bodies:
        for fixture in body:
            objects.append( fixture.shape.get_params(body) )
    objects.append( ('tracker', list(tracker.worldCenter)) )
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

