from random import randint, shuffle, getrandbits
from agents.agent import Agent

def neighbors(x,y):
    return [
        (x,y-1), # N
        (x+1,y), # E
        (x,y+1), # S
        (x-1,y), # W
    ]

class HuntTarget(Agent):
    def __init__(self, state, print_out=False):
        self.state = state
        self.print_out = print_out
        self.visited = set() # set of target tuples
        self.targets = set() # set of target tuples


    def next_tile(self):
        #do/while pls
        x, y = -1, -1
        while not self.state.free(x,y):
            if len(self.targets) == 0:
                x, y = self.random()
            else:
                x, y = self.targets.pop()

        return x, y

    def result(self, x, y, hit, sink):
        self.visited.add((x,y))

        if hit:
            self.state.hit(x, y)
            # Add adjacent unvisited targets
            for n in neighbors(x,y):
                if n not in self.visited:
                    self.targets.add(n)
            if self.print_out:
                print(self.state)
        else:
            self.state.miss(x, y)

    def random(self):
        return randint(0, self.state.width-1), randint(0, self.state.higth-1)

class HuntTargetParity(HuntTarget):
    # Confine the position to a checker pattern, randomise direction
    def random(self):
        x, y = super().random()
        if y % 2 + x % 2 != 1:
            delta = 1 if bool(getrandbits(1)) else -1
            if bool(getrandbits(1)):
                x += delta
            else:
                y += delta
        return x, y
