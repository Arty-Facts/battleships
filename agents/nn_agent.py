import torch
class NN_Agent():

    def __init__(self, state, network, targets,print_out=False ):
        self.state = state
        self.network = network
        self.print_out = print_out
        self.targets = targets

    def next_tile(self):
        self.x, self.y = self.network.predict(self.state, self.targets)
        return self.x, self.y


    def result(self, hit):
        if hit:
            self.state.hit(self.x, self.y)
            if self.print_out:
                print(self.state)
        else:
            self.state.miss(self.x, self.y)
