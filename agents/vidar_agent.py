from random import randint, shuffle, getrandbits

def neighbors(x,y):
    return [
        (x,y-1), # N
        (x+1,y), # E
        (x,y+1), # S
        (x-1,y), # W
    ]

class VidarAgent():
    def __init__(self, state, print_out=False):
        self.state = state
        self.print_out = print_out
        self.visited = set() # set of target tuples
        self.targets = set() # set of target tuples


    # Confine the position to a checker pattern, randomise direction
    def checkers(self, pos):
        x, y = pos
        if y % 2 + x % 2 != 1:
            delta = 1 if bool(getrandbits(1)) else -1
            if bool(getrandbits(1)):
                x += delta
            else:
                y += delta
        return x, y

    def next_tile(self):
        if len(self.targets) == 0:
            x, y = self.checkers(self.random())
        else:
            x, y = self.targets.pop()
        
        self.last = (x, y)
        # Just retry if bad, hopefully can't get stuck in endless recursion
        if not self.state.free(x,y):
            return self.next_tile()

        return x, y

    def result(self, hit):
        x, y = self.last
        self.visited.add(self.last)

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