# 2D Locomotion Evolution

Simple project for evolving vehicles crossing a 2D landscape. Physics simulation using pybox2d, visualisation with pygame.

## Description of modules

### `run_simulation.py`
(TODO: finish the implementation of state history saving for later visualisation; some way to check if the track was too short)

Simple implementation of the pybox2d simulation. `setup_sim` function creates the world as well as
the vehicle and track objects (using their own constructors). `run_sim` executes the simulation until the
vehicle doesn't move for more than `min_move` metres for `max_stuck_time` seconds; then returns the total distance
traveled.


### `visualise.py`

(TODO: everything)

Simple visualisation using pygame. Should initialise the pygame screen, open the saved state history of a single
run, and draw the subsequent physics frames. Might need some tinkering to recreate polygon and circle objects
from pure python lists of vertices/ circle positions that is stored in the history. The animation should follow
the main object (tricky?)

Look for hints and inspiration in the `test.py` and `test2.py` files.


### `evolution.py`

(TODO: fill the body)

The main program and evolution loop. Should create the initial object population (choosing the appropriate class, but then
using own constructors to keep modularity), generate a track, run the simulation (calling appropriate functions from
`run_simulation.py` module) for each object, select the winners/losers, breed the winning objects (by using internal
methods) and repeat for a number of times. Should/could store state histories for some runs, but probably not all...


### `track_generator.py`

(TODO: think of an actual track generation algorithm, implement with pybox2d)

Module with functions to create a track for vehicles. Should have a generation method that can produce the same track
for a given seed (so that every vehicle from the same population races on the same one), and a function to create the
appropriate pybox2d objects when called from `run_simulation.py`


### `vehicle.py`

(TODO: review base class, implement Car, then Walker)

Actual implementation of the evolving vehicle. This module contains the base class Vehicle and all its derivatives (Car, Walker, etc.) To keep modularity of the code, all information and behaviour specific
to a certain vehicle type (car, walker, etc.) should be kept here. That means that we should be able to create initial
(random) objects, build their pybox2d representation in the simulation and breed them (create mutated offspring) only
by calling functions defined in this module.

For proper object oriented programming, should probably define a parent class (Vehicle) from which every specific
class would inherit.


## Resources

We are using [pybox2d](https://github.com/pybox2d/pybox2d) ([manual](https://github.com/pybox2d/pybox2d/wiki/manual)) as the physics engine and [pygame](http://www.pygame.org/lofi.html) for handling the I/O (display in a window etc.).

### Installation instructions

Making sure that all the modules work together seems like the biggest nightmare in this projects. Here's how I've finally managed to get pygame and pybox2d running on my macOS.
It's certainly not the only way to get it done, but it worked for me and hopefully will for you too.

1. Make sure you have pip and your default python installation is associated with it. (In my case I had to remove the version installed by MacPorts, by removing it completely: `sudo port -fp uninstall installed`)
2. Install pygame with pip: `pip install pygame`
3. Do **not** install pybox2d with pip, because it won't work. Instead let's build the `pybox2d_dev` package from source, following the instructions [here](https://github.com/pybox2d/pybox2d/blob/master/INSTALL.md#building-from-source-os-x)
