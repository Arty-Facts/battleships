from random import random, randint, shuffle, getrandbits

def neighbors(x,y):
    return [
        (x,y-1), # N
        (x+1,y), # E
        (x,y+1), # S
        (x-1,y), # W
    ]

class Train():
    def __init__(self, state, print_out=False):
        self.state = state
        self.print_out = print_out
        self.visited = set() # set of target tuples
        self.targets = [] # set of target tuples
        


    def next_tile(self):
        #do/while pls
        x, y = -1, -1
        while not self.state.free(x,y):
            if len(self.targets) == 0 or random() > 0.75:
                x, y = self.random()
            else:
                shuffle(self.targets)
                x, y = self.targets[-1]
        return x, y

    def result(self, hit, x, y):
        self.visited.add((x,y))
        if (x,y) in self.targets:
            self.targets.remove((x,y))


        if hit:
            self.state.hit(x, y)
            # Add adjacent unvisited targets
            neig = neighbors(x,y)
            shuffle(neig)
            for n in neig:
                if n not in self.visited:
                    self.targets.append(n)
            if self.print_out:
                print(self.state)
        else:
            self.state.miss(x, y)
    
    def random(self):
        x, y = randint(0, self.state.width-1), randint(0, self.state.higth-1)
        if y % 2 + x % 2 != 1:
            delta = 1 if bool(getrandbits(1)) else -1
            if bool(getrandbits(1)):
                x += delta
            else:
                y += delta
        return x, y
