"""
History of simulation states

Objects of class StateHistory keep the shapes (in correct positions) of all the
simulated bodies at each time step, so it can be saved and visualised
separately. See documentation of StateHistory.
Additional helper functions serve to extract the transformed shapes from body
attributes.

TODO:
    Many named timelines, of different lengths
    Proper saving to files
    Store in a cleverer way, ideally just base shapes and transforms
"""

import shelve
import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, edgeShape, vec2)


# TODO: a single state should also be a class instead of collection of lists
class StateHistory:
    """
    History of simulation states - stores shapes for each time step

    To save memory, all static bodies are stored once for all history, an
    object with a collection of those in the .bodies attribute should be passed
    to the constructor. Dynamic bodies can be saved at each timestep via the
    save_state method, which can be called for many named timelines.
    """
    def __init__(self, track=None, name="history"):
        """
        Create state history

        Arguments:
            name:   identifier for finding in save files
            track:  object with a list of static bodies in track.bodies
        """
        self.name = name
        self.track = self.get_shapes(track)
        self.vehicle_states = []
        self.tracker_states = []

    def save_state(self, vehicle, timeline='timeline'):
        """
        Save current state of bodies in vehicle

        Arguments:
            vehicle:    object with list of dynamic bodies in vehicle.bodies
            timeline:   NOT IMPLEMENTED!!! name of timeline
        """
        shapes = self.get_shapes(vehicle)
        self.vehicle_states.append(shapes)
        tracker = vec2(vehicle.tracker)
        self.tracker_states.append(tracker)

    def get_shapes(self, instance):
        shapes = []
        for body in instance.bodies:
            for fixture in body:
                shapes.append( fixture.shape.get_transformed_shape(body) )
        return shapes

    def write_to_file(self, filename):
        """
        NOT IMPLEMENTED! Store history in a file
        """
        #open file for storing the history
        shelf = shelve.open(filename)
        # TODO: use self.name?
        shelf.setdefault('histories', [])
        hist_list = shelf['histories']
        hist_list.append(history)
        shelf['histories'] = hist_list
        shelf.close()

    def read_from_file(self, filename):
        """
        NOT IMPLEMENTED! Load history from a file
        """
        pass


# Helper functions to extract shapes in their correct positions
#   Add them as methods to the shape classes for 'polymorphic' calls
def get_transformed_edge(edge, body):
    new_vertices = [tuple(body.transform * v) for v in edge.vertices]
    return edgeShape(vertices=new_vertices)
edgeShape.get_transformed_shape = get_transformed_edge

def get_transformed_polygon(polygon, body):
    new_vertices = [tuple(body.transform * v) for v in polygon.vertices]
    return polygonShape(vertices=new_vertices)
polygonShape.get_transformed_shape = get_transformed_polygon

def get_transformed_circle(circle, body):
    new_pos = tuple(body.transform * circle.pos)
    return circleShape(pos=new_pos, radius=circle.radius)
circleShape.get_transformed_shape = get_transformed_circle


# Old version, keep for debugging
def get_params_polygon(polygon, body):
    vertices = [tuple(body.transform * v) for v in polygon.vertices]
    return 'polygon', vertices
polygonShape.get_params = get_params_polygon

def get_params_circle(circle, body):
    position = tuple(body.transform * circle.pos)
    radius = circle.radius
    return 'circle', (position, radius)
circleShape.get_params = get_params_circle

