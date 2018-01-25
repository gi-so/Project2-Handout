__author__ = 'sarah'

# make sure to change these to the student id's
ids = ["311148449", "935885178"]

import logic
import numpy
#import search
import copy
import itertools
import math


def something_blocks(pos1, pos2, state):
    block = None
    if pos1[0] == pos2[0] and pos1[1] == pos2[1]:
        block = block_on_the_line(pos1, pos1, 2, state)
    if pos1[1] == pos2[1] and pos1[2] == pos2[2]:
        block = block_on_the_line(pos1, pos2, 0, state)
    if pos1[0] == pos2[0] and pos1[2] == pos2[2]:
        block = block_on_the_line(pos1, pos2, 1, state)
    return block


def block_on_the_line(pos1, pos2, along_which_axes, state):  # x_axes=0 y=1 z=2
    for cali in state[2]:
        cal = cali
        if cali[1] != pos1 and cali[1] != pos2:
            if along_which_axes == 2:
                if cali[1][0] == pos1[0] and cali[1][1] == pos1[1]:
                    if pos1[2] < cali[1][2] < pos2[2] or pos1[2] > cali[1][2] > pos2[2]:
                        return cali[1]

            if 0 == along_which_axes:
                if cali[1][1] == pos1[1] and cali[1][2] == pos1[2]:
                    if pos1[0] < cali[1][0] < pos2[0] or pos1[0] > cali[1][0] > pos2[0]:
                        return cali[1]

            if 1 == along_which_axes:
                if cali[1][0] == pos1[0] and cali[1][2] == pos1[2]:
                    if pos1[1] < cali[1][1] < pos2[1] or pos1[1] > cali[1][1] > pos2[1]:
                        return cali[1]
    for tar in state[3]:
        if tar[0] != pos1 and tar[0] != pos2:
            if along_which_axes == 2:
                if tar[0][0] == pos1[0] and tar[0][1] == pos1[1]:
                    if pos1[2] < tar[0][2] < pos2[2] or pos1[2] > tar[0][2] > pos2[2]:
                        return tar[0]

            if 0 == along_which_axes:
                if tar[0][1] == pos1[1] and tar[0][2] == pos1[2]:
                    if pos1[0] < tar[0][0] < pos2[0] or pos1[0] > tar[0][0] > pos2[0]:
                        return tar[0]

            if 1 == along_which_axes:
                if tar[0][0] == pos1[0] and tar[0][2] == pos1[2]:
                    if pos1[1] < tar[0][1] < pos2[1] or pos1[1] > tar[0][1] > pos2[1]:
                        return cal[0]




def any_location(calibration_targets, targets, ships):
    tmp_lst = []

    for k, v in calibration_targets.items():
        tmp_lst.append(v)  # TODO: Check if the value is a list or single item

    for k, v in targets.items():
        tmp_lst.append(k)

    for k, v in ships.items():
        tmp_lst.append(v)

    return tuple(tmp_lst)

def manhattan_distance(state1, state2):
    return math.fabs(state1[0] - state2[0]) + math.fabs(state1[1] - state2[1]) + math.fabs(state1[2] - state2[2])

def modified_manhattan_distance(start, toLevelOfTarget):
    distances = [math.fabs(start[1] - toLevelOfTarget[1]) + math.fabs(start[2] - toLevelOfTarget[2]),
                 math.fabs(start[0] - toLevelOfTarget[0]) + math.fabs(start[1] - toLevelOfTarget[1]),
                 math.fabs(start[0] - toLevelOfTarget[0]) + math.fabs(start[2] - toLevelOfTarget[2])]
    position = (-1,-1,-1)
    if min(distances) == distances[0]:
        position = (start[0], toLevelOfTarget[1], toLevelOfTarget[2])
    if min(distances) == distances[1]:
        position = (toLevelOfTarget[0], toLevelOfTarget[1], start[2])
    if min(distances) == distances[2]:
        position = (toLevelOfTarget[0], start[1], toLevelOfTarget[2])

    return min(distances), position





def best_next_target(ship, problemState):
    tmp_best = ()
    for target in problemState[3]:
        authorized = False
        for weapon in ship[3]:
            if weapon in target[1]:
                authorized = True
        if authorized:
            if ship[2][0] in target[1] and ship[2][1]:
                dist = modified_manhattan_distance(ship[1], target[0])
                block = something_blocks(dist[1],target[0], problemState)
                if block is not None:
                    dist=(dist[0]+manhattan_distance(dist[1],target[0]),block[1])
                if tmp_best == ():
                    tmp_best = (dist[0], target)
                if dist[0]<tmp_best[0]:
                    tmp_best = (dist[0],target)
            else:
                cost = 1                    #for calibration
                if ship[2][1] == False:
                    cost += 1               #for activation
                for cali in problemState[2]:
                    if cali [0] in target [1] and cali[0] in ship[3]:
                        dist = modified_manhattan_distance(ship[1],cali[1])
                        cost += dist[0]
                        block = something_blocks(dist[1],cali[1],problemState)
                        if block is not None:
                            cost+=manhattan_distance(dist[1],block)             #dist to cali

                            dist = modified_manhattan_distance(block,target[0])
                        else:
                            dist = modified_manhattan_distance(dist[1],target[0])
                        cost += dist [0]    #dist from cali to target
                        block = something_blocks(dist[1],target[0],problemState)
                        if block is not None:
                            cost+=manhattan_distance(dist[1],block)
                        if tmp_best == ():
                            tmp_best = (cost, target, cali)
                        if cost<tmp_best[0]:
                            tmp_best = (cost, target, cali)
    return tmp_best

class SpaceshipController:
    "This class is a controller for a spaceship problem."
    space_kb = logic.PropKB()
    states = []
    state = ()
    move_back = None
    prev_fit = None

    def __init__(self, problem, num_of_transmitters):
        # TODO : COMPLETE BY STUDENTS
        locations = any_location(problem[4], problem[5], problem[6])
        global state
        global states
        global move_back
        global prev_fit
        global space_kb
        space_kb = logic.PropKB()
        self.state= self.problem = (problem[0], self.make_inst_on_ships(problem[6], problem[3]), tuple(problem[4].items()),
                        tuple(problem[5].items()), locations)
        print(self.problem)
        for ship in self.state[1]:
            pos_str = 'P' + str(ship[1])
            self.space_kb.tell(~logic.expr(pos_str))
            pos_str = 'P' + str((ship[1][0] + 1, ship[1][1], ship[1][2]))
            print(pos_str)
            self.space_kb.tell(~logic.expr(pos_str))
            pos_str = 'P' + str((ship[1][0] - 1, ship[1][1], ship[1][2]))
            print(pos_str)
            self.space_kb.tell(~logic.expr(pos_str))
            print(pos_str)
            pos_str = 'P' + str((ship[1][0], ship[1][1] + 1, ship[1][2]))
            print(pos_str)
            self.space_kb.tell(~logic.expr(pos_str))
            pos_str = 'P' + str((ship[1][0], ship[1][1] - 1, ship[1][2]))
            print(pos_str)
            self.space_kb.tell(~logic.expr(pos_str))
            pos_str = 'P' + str((ship[1][0], ship[1][1], ship[1][2] + 1))
            print(pos_str)
            self.space_kb.tell(~logic.expr(pos_str))
            pos_str = 'P' + str((ship[1][0], ship[1][1], ship[1][2] - 1))
            print(pos_str)
            self.space_kb.tell(~logic.expr(pos_str))

        # search.Problem.__init__(self, self.problem)


    def next_move_to_mission(self, mission, state):
        actions = self.actions(state)

        if len(mission[0]) == 3:
            tmp_min_dist = None
            for action in actions:

                if action[0] == "move" and action[1] == mission[1][0]:

                    for cali in state[2]:
                        if cali[0]==mission[1][2][0] and cali[0] == mission[0][2][0]:
                            dist=modified_manhattan_distance(action[3],cali[1])

                            if tmp_min_dist is None:
                                if self.result(state,action) not in self.states:
                                    tmp_min_dist = (dist[0],action)
                                else:
                                    tmp_min_dist = (2*(self.state[0]*self.state[0]), action)
                            if dist[0] < tmp_min_dist[0]:
                                if self.result(state,action) not in self.states:
                                    tmp_min_dist = (dist[0],action)
            return tmp_min_dist[1]

        if len(mission[0]) == 2:
            tmp_min_dist = None
            for action in actions:

                if action[0] == "move" and action[1] == mission[1][0]:

                    dist=modified_manhattan_distance(action[3],mission[0][1][0])


                    if tmp_min_dist is None:
                        if self.result(state,action) not in self.states:
                            tmp_min_dist = (dist[0],action)
                        else:tmp_min_dist = ((self.state[0]*self.state[0])*2, action)
                    else:
                        if dist[0] < tmp_min_dist[0]:
                            if self.result(state,action) not in self.states:
                                tmp_min_dist = (dist[0],action)
            #print (tmp_min_dist[0])
            return tmp_min_dist[1]


    def get_next_action(self, observation):
        # TODO : COMPLETE BY STUDENTS
        # get observation for the current state and return next action to apply (and None if no action is applicable)
        #self.space_kb.tell()
        cleared = False
        #print(self.state)
        for prev_tar in self.problem[3]:
            for tar in self.state[3]:
                if prev_tar[0] == tar[0]:
                    if len(prev_tar[1]) != len(tar[1]):
                        self.states=[]
                        self.prev_fit = None
                        cleared=True
        if cleared:
            print("CLEARED")
            self.problem=self.state
        # Take a ship and look for the closest target+calibration


        actions = self.actions(self.state)
        #print(actions)
        next_action = None

        next_target = None
        ship_missions=[]
        for ship in self.state[1]:

            for action in actions:
                if observation.get(ship[0]) != -1:
                    if observation.get(ship[0]) == 1:
                        pos_str = 'P' + str(ship[1])
                        self.space_kb.tell(~logic.expr(pos_str))

                    elif observation.get(ship[0])==0:
                        pos_str='P'+str(ship[1])
                        self.space_kb.tell(~logic.expr(pos_str))
                        pos_str='P'+str((ship[1][0]+1,ship[1][1],ship[1][2]))
                        self.space_kb.tell(~logic.expr(pos_str))
                        pos_str = 'P' + str((ship[1][0]-1, ship[1][1], ship[1][2]))
                        self.space_kb.tell(~logic.expr(pos_str))
                        pos_str = 'P' + str((ship[1][0], ship[1][1]+1, ship[1][2]))
                        self.space_kb.tell(~logic.expr(pos_str))
                        pos_str = 'P' + str((ship[1][0], ship[1][1]-1, ship[1][2]))
                        self.space_kb.tell(~logic.expr(pos_str))
                        pos_str = 'P' + str((ship[1][0], ship[1][1], ship[1][2]+1))
                        self.space_kb.tell(~logic.expr(pos_str))
                        pos_str = 'P' + str((ship[1][0], ship[1][1], ship[1][2]-1))
                        self.space_kb.tell(~logic.expr(pos_str))
                    if action[0] == "use" and action [1] == ship[0]:
                        self.state = self.result(self.state, action)
                        self.states.append(self.state)
                        return action
                    if action[0] == "calibrate" and action [1] == ship[0] and ship[2][1]==False:
                        self.state = self.result(self.state, action)
                        self.states.append(self.state)
                        return action
                    if ship[2][0] is None:
                        if action[0] == "turn_on" and action[1] == ship[0]:
                            need_for_weapon = False
                            for tar in self.state[3]:
                                if action[2] in tar[1]:
                                    need_for_weapon = True
                            if need_for_weapon:
                                self.state = self.result(self.state, action)
                                self.states.append(self.state)
                                return action

            fitness = -1
            tmp_min_fit=None
            if observation.get(ship[0]) != -1:
                ntarget = best_next_target(ship, self.state)
                if ntarget != ():
                    fitness = ntarget[0]+observation.get(ship[0])+1
                if tmp_min_fit is None:
                    tmp_min_fit = fitness
                    next_target = ntarget
                if 0 < fitness < tmp_min_fit:
                    tmp_min_fit = fitness
                    next_target = ntarget

            if next_target != ():
                ship_missions.append((next_target,ship))
        tmp_best = None
        for mission in ship_missions:
            if tmp_best is None:
                tmp_best = mission

            if 0<mission[0][0]<tmp_best[0][0]:
                tmp_best = mission
        '''if self.prev_fit is None:
            print (mission[0][0])
            self.prev_fit = mission[0][0]
        elif self.prev_fit<mission[0][0]:
            self.prev_fit=None
            self.state = self.result(self.state, self.move_back)
            return self.move_back
        else:
            self.prev_fit=mission[0][0]'''
        if mission[1][2][0] not in mission[0][1][1]:
            next_action = ("turn_on", mission[1][0], mission[0][2][0])
            self.state=self.result(self.state,next_action)

            return  next_action
        next_action = self.next_move_to_mission(mission, self.state)
        if next_action is None:
            return self.move_back
        allow=logic.dpll_satisfiable(logic.to_cnf(logic.associate('&',self.space_kb.clauses + [logic.expr('P'+str(next_action[3]))])))
        #print(allow)
        tmp_state = self.result(self.state, next_action)
        self.states.append(tmp_state)
        while allow != False:
            print('Achtung Laser')
            print(allow)
            next_action = self.next_move_to_mission(mission, self.state)
            tmp_state = self.result(self.state, next_action)
            self.states.append(tmp_state)
            if len(self.states)>6:
                self.states.clear()
            allow = logic.dpll_satisfiable(
                logic.to_cnf(logic.associate('&', self.space_kb.clauses + [logic.expr('P' + str(next_action[3]))])))
            #print(allow)
        self.state=tmp_state
        self.move_back = (next_action[0], next_action[1], next_action[3],next_action[2])
        return next_action




    @staticmethod
    def check_who_blocks(state, tmp_lst_min, tmp_lst_cali, all_occupied_pos):
        cali = []
        target = []
        tmp_block = []
        for i in range(0,6):
            tmp_block.append(())

        for pos in all_occupied_pos:
            if pos[1] == state[1] and pos[2] == state[2] and pos[0] != state[0]:
                if state[0]<pos[0]:
                    if tmp_block[0]==():
                        tmp_block[0]=pos
                    elif pos[0]<tmp_block[0][0]:
                        tmp_block[0]=pos

                if state[0]>pos[0]:
                    if tmp_block[1] == ():
                        tmp_block[1] = pos
                    elif pos[0]<tmp_block[1][0]:
                        tmp_block[1] = pos
            if pos[0] == state[0] and pos[2] == state[2] and pos[1] != state[1]:
                if state[1] < pos[1]:
                    if tmp_block[2] == ():
                        tmp_block[2] = pos
                    elif pos[1]<tmp_block[2][1]:
                        tmp_block[2] = pos
                if state[1] > pos[1]:
                    if tmp_block[3] == ():
                        tmp_block[3] = pos
                    elif pos[1]<tmp_block[3][1]:
                        tmp_block[3] = pos
            if pos[0] == state[0] and pos[1] == state[1] and pos[2] != state[2]:
                if state[2] < pos[2]:
                    if tmp_block[4] == ():
                        tmp_block[4] = pos
                    elif pos[2]<tmp_block[4][2]:
                        tmp_block[4] = pos

                if state[2] > pos[2]:
                    if tmp_block[5] == ():
                        tmp_block[5] = pos
                    elif pos[2]>tmp_block[5][2]:
                        tmp_block[5] = pos

        tmp_block_lst=tuple(tmp_block)
        for i in range(0, 6):
            if tmp_lst_cali[i] == () or tmp_lst_min[i] == ():
                if tmp_lst_min[i] == ():
                    if tmp_lst_cali[i] != ():
                        if tmp_block_lst[i] == () or tmp_block_lst[i] == tmp_lst_cali[i][1]:
                            cali.append(tmp_lst_cali[i])
                if tmp_lst_cali[i] == ():
                    if tmp_lst_min[i] != ():
                        if tmp_block_lst[i] == () or tmp_block_lst[i] == tmp_lst_min[i][0]:
                            target.append(tmp_lst_min[i])
            elif tmp_lst_cali[i] == () and tmp_lst_min[i] == ():
                pass
            else:
                tmp_res_min = math.fabs(state[0] - tmp_lst_min[i][0][0]) + math.fabs(
                    state[1] - tmp_lst_min[i][0][1]) + math.fabs(state[2] - tmp_lst_min[i][0][2])

                tmp_res_cali = math.fabs(state[0] - tmp_lst_cali[i][1][0]) + math.fabs(
                    state[1] - tmp_lst_cali[i][1][1]) + math.fabs(state[2] - tmp_lst_cali[i][1][2])

                tmp_res_block = math.fabs(state[0] - tmp_block_lst[i][0])+math.fabs(
                    state[1] - tmp_block_lst[i][1])+math.fabs(state[2] - tmp_block_lst[i][2])
                if tmp_res_min < tmp_res_cali and tmp_res_min<=tmp_res_block:
                    target.append(tmp_lst_min[i])
                elif tmp_res_cali<tmp_res_min and tmp_res_cali<=tmp_res_block:
                    cali.append(tmp_lst_cali[i])

        return target, cali

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a tuple, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        dim = state[0]
        allowed_lst = []

        # Move section
        for ship in state[1]:
            if ship[1][0] != dim - 1 and (int(ship[1][0]) + 1, ship[1][1], ship[1][2]) not in state[4]:
                allowed_lst.append(("move", ship[0], ship[1], (int(ship[1][0]) + 1, ship[1][1], ship[1][2])))

            if ship[1][1] != dim - 1 and (ship[1][0], int(ship[1][1]) + 1, ship[1][2]) not in state[4]:
                allowed_lst.append(("move", ship[0], ship[1], (ship[1][0], int(ship[1][1]) + 1, ship[1][2])))

            if ship[1][2] != dim - 1 and (ship[1][0], ship[1][1], int(ship[1][2]) + 1) not in state[4]:
                allowed_lst.append(("move", ship[0], ship[1], (ship[1][0], ship[1][1], int(ship[1][2]) + 1)))

            if ship[1][0] != 0 and (int(ship[1][0]) - 1, ship[1][1], ship[1][2]) not in state[4]:
                allowed_lst.append(("move", ship[0], ship[1], (int(ship[1][0]) - 1, ship[1][1], ship[1][2])))

            if ship[1][1] != 0 and (ship[1][0], int(ship[1][1]) - 1, ship[1][2]) not in state[4]:
                allowed_lst.append(("move", ship[0], ship[1], (ship[1][0], int(ship[1][1]) - 1, ship[1][2])))

            if ship[1][2] != 0 and (ship[1][0], ship[1][1], int(ship[1][2]) - 1) not in state[4]:
                allowed_lst.append(("move", ship[0], ship[1], (ship[1][0], ship[1][1], int(ship[1][2]) - 1)))

        # Turn on

        for ship in state[1]:
            for inst in ship[3]:
                if inst != ship[2][0]:
                    allowed_lst.append(("turn_on", ship[0], inst))

        # Use & Cali

        for ship in state[1]:
            tmp_lst_min = []
            tmp_lst_cal = []

            # Maximum values

            for i in range(0, 6):
                tmp_lst_min.append(())
                tmp_lst_cal.append(())

            # if ship[2][1]:  # Check if calibrated
            for target in state[3]:
                # Check for every target if  closer to the state
                self.check_for_use(1, 2, 0, 0, 1, ship[1], target, tmp_lst_min)
                self.check_for_use(0, 2, 1, 2, 3, ship[1], target, tmp_lst_min)
                self.check_for_use(1, 0, 2, 4, 5, ship[1], target, tmp_lst_min)

            for cali in state[2]:
                self.check_for_cali(1, 2, 0, 0, 1, ship[1], cali, tmp_lst_cal)
                self.check_for_cali(0, 2, 1, 2, 3, ship[1], cali, tmp_lst_cal)
                self.check_for_cali(1, 0, 2, 4, 5, ship[1], cali, tmp_lst_cal)

            target, cali = self.check_who_blocks(ship[1], tmp_lst_min, tmp_lst_cal, state[4])

            if ship[2][1]:  # If the weapon is calibrated
                for item in target:
                    if ship[2][0] in item[1] and ship[2][1]:
                        allowed_lst.append(("use", ship[0], ship[2][0], item[0]))
            else:
                for item in cali:
                    if ship[2][0] == item[0]:
                        allowed_lst.append(("calibrate", ship[0], ship[2][0], item[1]))

        return tuple(allowed_lst)


    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        if action[0] == "move":
            all_ships = []
            for ship in state[1]:
                if ship[1] == action[2]:
                    new_ship = (ship[0], action[3], ship[2], ship[3])
                    all_ships.append(new_ship)
                else:
                    all_ships.append(ship)

            tmp = list(state[4])
            tmp.remove(action[2])
            tmp.append(action[3])

            state = (state[0], tuple(all_ships), state[2], state[3], tuple(tmp))

            return state

        elif action[0] == "turn_on":
            all_ships = []
            for ship in state[1]:
                if ship[0] == action[1]:
                    new_ship = (ship[0], ship[1], (action[2], False), ship[3])
                    all_ships.append(new_ship)
                else:
                    all_ships.append(ship)

            state = (state[0], tuple(all_ships), state[2], state[3], state[4])
            return state

        elif action[0] == "use":
            all_targets = []
            for target in state[3]:
                if target[0] == action[3]:
                    tmp = list(target[1])
                    tmp.remove(action[2])
                    modified_target = (target[0], tuple(tmp))

                    all_targets.append(modified_target)

                else:
                    all_targets.append(target)

            state = (state[0], state[1], state[2], tuple(all_targets), state[4])
            return state

        elif action[0] == "calibrate":
            all_ships = []
            for ship in state[1]:
                if ship[0] == action[1]:
                    current_instrument = ship[2][0]
                    new_ship = (ship[0], ship[1], (current_instrument, True), ship[3])
                    all_ships.append(new_ship)
                else:
                    all_ships.append(ship)

            state = (state[0], tuple(all_ships), state[2], state[3], state[4])
            return state







    @staticmethod
    def make_inst_on_ships(locations, inst_on_ships):
        tmp_lst = []

        for k, v in locations.items():
            for ship, inst in inst_on_ships.items():
                if ship == k:
                    tmp_lst.append((k, v, (None, False), inst))

        return tuple(tmp_lst)



    @staticmethod
    def check_for_use(a, b, c, d, e, state, target, tmp_lst_min):
        if state[a] == target[0][a] and state[b] == target[0][b]:
            if state[c] < target[0][c]:
                if tmp_lst_min[d] == ():
                    tmp_lst_min[d] = target
                elif tmp_lst_min[d][0][c] < target[0][c]:
                    tmp_lst_min[d] = target
            elif state[c] > target[0][c]:
                if tmp_lst_min[e] == ():
                    tmp_lst_min[e] = target
                elif tmp_lst_min[e][0][c] > target[0][c]:
                    tmp_lst_min[e] = target


                    # TODO: Check if < and > are set correct

    @staticmethod
    def check_for_cali(fixed_axis, second_fixed_axis, on_line_of_this_axis, first_dir, second_dir, state, cali,
                       tmp_lst_cal):
        if state[fixed_axis] == cali[1][fixed_axis] and state[second_fixed_axis] == cali[1][second_fixed_axis]:
            if state[on_line_of_this_axis] < cali[1][on_line_of_this_axis]:
                if tmp_lst_cal[first_dir] == ():
                    tmp_lst_cal[first_dir] = cali
                elif tmp_lst_cal[first_dir][1][on_line_of_this_axis] < cali[1][on_line_of_this_axis]:
                    tmp_lst_cal[first_dir] = cali
            elif state[on_line_of_this_axis] > cali[1][on_line_of_this_axis]:
                if tmp_lst_cal[second_dir] == ():
                    tmp_lst_cal[second_dir] = cali
                elif tmp_lst_cal[second_dir][1][on_line_of_this_axis] > cali[1][on_line_of_this_axis]:
                    tmp_lst_cal[second_dir] = cali