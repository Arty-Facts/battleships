from random import randint, shuffle
class Agent():

    def __init__(self, state):
        self.state = state
        self.x = -1
        self.y = -1

    def next_tile(self):
        self.x, self.y = self.random()
        while(not self.state.free(self.x,self.y)):
            self.x, self.y = self.random()
        return self.x, self.y


    def result(self, hit):
        if hit:
            self.state.hit(self.x, self.y)
            print(self.state)
        else:
            self.state.miss(self.x, self.y)

    def random(self):
        return randint(0, self.state.width-1), randint(0, self.state.higth-1)