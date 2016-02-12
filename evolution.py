import run_simulation as sim
import track_generator
import vehicle
import test

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
            distance, bb, time = sim.run_sim(1e4)
            car.score = distance #if distance < 20 else distance/time*100
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
        play(winners[0], track)


def play(car, track):
    test.start_game(car, track)
    test.run(1)

