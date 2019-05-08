from random import randint
class RandomAgent():

    def __init__(self, state, print_out=False ):
        self.state = state
        self.print_out = print_out
        self.print_out
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
            if self.print_out:
                print(self.state)
        else:
            self.state.miss(self.x, self.y)

    def random(self):
        return randint(0, self.state.width-1), randint(0, self.state.higth-1)