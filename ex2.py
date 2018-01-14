__author__ = 'sarah'

# make sure to change these to the student id's
ids = ["000000000","111111111"]

import logic
import numpy
import search
import copy
import itertools

def any_location(calibration_targets, targets, ships):
    tmp_lst = []

    for k, v in calibration_targets.items():
        tmp_lst.append(v)  # TODO: Check if the value is a list or single item

    for k, v in targets.items():
        tmp_lst.append(k)

    for k, v in ships.items():
        tmp_lst.append(v)

    return tuple(tmp_lst)



class SpaceshipController:

    @staticmethod
    def make_inst_on_ships(locations, inst_on_ships):
        tmp_lst = []

        for k, v in locations.items():
            for ship, inst in inst_on_ships.items():
                if ship == k:
                    tmp_lst.append((k, v, (None, False), inst))

        return tuple(tmp_lst)

    "This class is a controller for a spaceship problem."
    def __init__(self, problem, num_of_transmitters):
       # TODO : COMPLETE BY STUDENTS
       locations = any_location(problem[4], problem[5], problem[6])

       self.problem = (problem[0], self.make_inst_on_ships(problem[6], problem[3]), tuple(problem[4].items()),
                       tuple(problem[5].items()), locations)
       print(self.problem)
       search.Problem.__init__(self, self.problem)

    def get_next_action(self, observation):
        # TODO : COMPLETE BY STUDENTS
        # get observation for the current state and return next action to apply (and None if no action is applicable)

