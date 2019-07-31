from collections import defaultdict
from random import random, randint
import pickle
from config import*
class QlerningControler:

    # PARAMETERS OF THE LEARNING ALGORITHM - THESE MAY BE TUNED BUT THE DEFAULT VALUES OFTEN WORK REASONABLY WELL 
    GAMMA_DISCOUNT_FACTOR = 0.95; # Must be < 1, small values make it very greedy
    LEARNING_RATE_CONSTANT = 10; # See alpha(), lower values are good for quick results in large and deterministic state spaces
    explore_chance = EXPLORE_CHANSE; # The exploration chance during the exploration phase
    REPEAT_ACTION_MAX = 30; # Repeat selected action at most this many times trying reach a new state, without a max it could loop forever if the action cannot lead to a new state

    def __init__(self, state):
        self.QTable = {}
        self.NTable = {}
        self.iteration = 0
        self.action_counter = 0
        self.previous_state = tuple(state.get())
        self.previous_action = (-1, -1)
        self.load()

    def __del__(self):
        self.save()

    def save(self, name="table"):
        with open(f'Qlerning/tables/Q{name}_{WORLD_SIZE_X}x{WORLD_SIZE_Y}.pickle', 'wb') as handle:
            pickle.dump(self.QTable, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(f'Qlerning/tables/N{name}_{WORLD_SIZE_X}x{WORLD_SIZE_Y}.pickle', 'wb') as handle:
            pickle.dump(self.NTable, handle, protocol=pickle.HIGHEST_PROTOCOL)


    def load(self, name="table"):
        try:
            with open(f'Qlerning/tables/Q{name}_{WORLD_SIZE_X}x{WORLD_SIZE_Y}.pickle', 'rb') as handle:
                self.QTable = pickle.load(handle)
            with open(f'Qlerning/tables/N{name}_{WORLD_SIZE_X}x{WORLD_SIZE_Y}.pickle', 'rb') as handle:
                self.NTable = pickle.load(handle)
        except:
            print("unable to lockate erlier tables")

    # Main decision loop
    def tick(self, state, state_reward):
        self.iteration += 1
        new_state = state_reward.state(state)
        previous_reward = state_reward.reward(state)
        self.action_counter = 0

        if self.previous_state != None:
            # Create state-action key
            prev_state_action = self.previous_state + self.previous_action
            # Increment state-action counter
            if prev_state_action in self.NTable:
                self.NTable[prev_state_action] += 1
            else:
                self.NTable[prev_state_action] = 1

            if prev_state_action not in self.QTable:
                self.QTable[prev_state_action] = 0


            # Update Q value
            # Q(s, a) ← Q(s, a) + α(R(s) + γ max aQ('s, 'a) − Q(s, a))
            r = previous_reward
            y = QlerningControler.GAMMA_DISCOUNT_FACTOR
            thisQvalue = self.QTable[prev_state_action]
            Qvalue = thisQvalue + self.alpha(self.NTable[prev_state_action]) * (r +  y * self.getMaxActionQValue(state) - thisQvalue)

            self.QTable[prev_state_action] = Qvalue
            action = self.selectAction(state)
            self.previous_state = new_state
            self.previous_action = action
            return action 




    # Finds the highest Qvalue of any action in the given state 
    def getMaxActionQValue(self, state):
        maxQval = -float("inf")
        for x in range(state.higth):
            for y in range(state.width):
                if tuple(state.get()) + (x,y) not in self.QTable:
                    continue
                Qval = self.QTable[tuple(state.get()) + (x,y)]
                if Qval > maxQval:
                    maxQval = Qval
        if maxQval == -float("inf"):
            return 0
        return maxQval

    # Selects an action in a state based on the registered Q-values and the exploration chance
    def selectAction(self, state):
        x,y = self.random(state)
        while not state.free(x,y):
            x,y = self.random(state)
        action = (x,y)
        # Taking random exploration action
        if random() < QlerningControler.explore_chance:
            return action
        maxQval = -float("inf")
        for x in range(state.higth):
            for y in range(state.width):
                if state.free(x,y):
                    test = tuple(state.get()) + (x,y)
                    if test in self.QTable:
                        Qval = self.QTable[test]
                        if Qval > maxQval:
                            maxQval = Qval
                            action = (x,y)
        return action
	# Computes the learning rate parameter alpha based on the number of times the state-action combination has been tested
    def alpha(self, num_tested):
        # Lower learning rate constants means that alpha will become small faster and therefore make the agent behavior converge to 
        # to a solution faster, but if the state space is not properly explored at that point the resulting behavior may be poor.
        # If your state-space is really huge you may need to increase it. 
        alpha = (QlerningControler.LEARNING_RATE_CONSTANT/(QlerningControler.LEARNING_RATE_CONSTANT + num_tested))
        return alpha
    
    def random(self, state):
        return randint(0, state.width-1), randint(0, state.higth-1)


