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

import run_simulation as sim
import track_generator
import vehicle
#import test
import visualise

VehicleClass = vehicle.Car # or vehicle.Car

n_generations = 10
fleet_size = 100
n_winners = 20

def main():
    fleet = []
    for i in xrange(fleet_size):
        car = VehicleClass()
        car.random_genome()
        fleet.append(car)

    track = track_generator.Track(100, 1)

    for gen in xrange(n_generations):
        max_score = 0
        for car in fleet:
            #play(car, track)
            sim.setup_sim(car, track)
            distance, bb, time = sim.run_sim(1e4, save=True)
            car.score = distance #if distance < 20 else distance/time*100
            car.history = copy.copy(sim.history) # FIXME: huge amounts of memory???
            #if distance > max_score:
            #    max_score = distance

        fleet.sort(key=lambda car:car.score, reverse=True) 
        winners = fleet[0:n_winners]
        scores = [car.score for car in fleet]

        print "Scoreboard:"
        print scores[0:n_winners]

        fleet = []
        #print "Winners:"
        for winner in winners:
            #print winner.score
            #print "\nNext winner reproduces"
            for j in xrange(fleet_size/n_winners):
                #print ""
                fleet.append(winner.get_child())

        #print ""
        #play(winners[0], track)
        visualise.start_game()
        visualise.run(winners[0].history, speed=3)


def play(car, track):
    test.start_game(car, track)
    test.run(1)


if __name__ == '__main__':
    main()
