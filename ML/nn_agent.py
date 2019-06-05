import torch
class NN_Agent():

    def __init__(self, state, network, targets ,print_out=False ):
        self.state = state
        self.network = network
        self.print_out = print_out
        self.targets = targets

    def next_tile(self):
        x, y = self.network.predict(self.state, self.targets)
        return x, y


    def result(self,x, y, hit, sink):
        if hit:
            self.state.hit(x, y)
            if self.print_out:
                print(self.state)
        else:
            self.state.miss(x, y)
