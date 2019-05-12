from random import randint
from agents.agent import Agent
class QlergningAgent(Agent):

    def __init__(self, state, print_out=False ):
        self.state = state
        self.print_out = print_out
        self.Qtable = {}
        
    def next_tile(self):
        x, y = self.random()
        while(not self.state.free(x,y)):
            x, y = self.random()
        return x, y


    def result(self, x, y, hit, sinc):
        if hit:
            self.state.hit(x, y)
            if self.print_out:
                print(self.state)
        else:
            self.state.miss(x, y)

    def random(self):
        return randint(0, self.state.width-1), randint(0, self.state.higth-1)