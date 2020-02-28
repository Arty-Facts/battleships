from random import randint
from agents.agent import Agent
from Qlerning.QlerningControler import QlerningControler
from Qlerning.StateAndReward import StateAndReward
class QlergningAgent(Agent):

    def __init__(self, state, print_out=False ):
        self.controler = QlerningControler(state)
        self.state_and_reward = StateAndReward()
        self.state = state
        self.print_out = print_out
        
    def next_tile(self):
        return self.controler.tick(self.state, self.state_and_reward)

    def save(self):
        self.controler.save()

    def result(self, x, y, hit, sinc):
        if hit:
            self.state.hit(x, y)
            if self.print_out:
                print(self.state)
        else:
            self.state.miss(x, y)

    def random(self):
        return randint(0, self.state.width-1), randint(0, self.state.higth-1)