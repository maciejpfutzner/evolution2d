"""
Top level module running the main game function. Creates the
initial fleet of vehicles and a track, calls the simulation to
perform individual races, evaluates and breeds the winners. Loop is
repeated a set number of times, with visual displays of the best
organisms.

Usage: Currently just run the main function (automatic if run as a script),
it will perform 10 iterations of 100 races and show the winner (press Enter
to start, Esc to end), while printing some debug messages. The visualisation
uses a test module and basically reruns the race simulation.

TODO: 
    Make an interactive game menu allowing to choose options for vehicles,
    tracks, and other parameters. If possible, allow to visualise any chosen
    race.
"""
import copy

import run_simulation as run_sim
import track_generator
import vehicle
#import test
import visualise
import state_history as sh

VehicleClass = vehicle.Car

n_generations = 10
fleet_size = 75
n_winners = 15
display_winners = 3

def main():
    fleet = []
    for i in xrange(fleet_size):
        car = VehicleClass()
        car.random_genome()
        car.name = 'car_%d'%i
        fleet.append(car)

    for gen in xrange(n_generations):
        track = track_generator.Track(400, 5)

        hist = sh.StateHistory()

        max_score = 0
        for car in fleet:
            sim = run_sim.Simulation(track, car, save=True)

            # XXX: Apparently the track has to be built
            # before the history can be set up
            if not hist.track:
                hist.set_track(track)

            distance, bb, time = sim.run(1e4)
            car.score = distance #if distance < 20 else distance/time*100

            # FIXME: Huge amounts of memory? Nicer if possible
            hist.timelines[car.name] = sim.history.timelines['timeline']
            #if distance > max_score:
            #    max_score = distance

        fleet.sort(key=lambda car:car.score, reverse=True) 
        winners = fleet[0:n_winners]
        #scores = [car.score for car in fleet]

        print "Scoreboard:"
        #print scores[0:n_winners]

        fleet = []
        for winner in winners:
            print "%s: %g" %(winner.name, winner.score)
            for j in xrange(fleet_size/n_winners):
                child = winner.get_child()
                child.name = winner.name + '_%d'%j
                fleet.append(child)

        # for now only visualise the winners timeline
        timelines = [w.name for w in winners[:display_winners]]
        visualise.start_game()
        visualise.run(hist, timelines, speed=3)


def play(car, track):
    test.start_game(car, track)
    test.run(1)


if __name__ == '__main__':
    main()
