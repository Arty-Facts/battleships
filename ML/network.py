import torch

class Network(torch.nn.Module):

    def __init__(self, hidden_dim, dim):
        super().__init__()
        self.model = torch.nn.Sequential(torch.nn.Linear(dim, hidden_dim), \
                                         torch.nn.ReLU(), \
                                         torch.nn.Linear(hidden_dim, dim))
        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.model.to(self.device) # without this there is no error, but it runs in CPU (instead of GPU). 
        # self.model.eval() # declaring to the system that we're only doing 'forward' calculations 

    def forward(self, state):
        return self.model(state)
