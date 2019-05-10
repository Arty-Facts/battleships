import torch

class Network(torch.nn.Module):

    def __init__(self,input_dim, hidden_dim, output_dim, load=True):
        super().__init__()
        self.model = torch.nn.Sequential(torch.nn.Linear(input_dim, hidden_dim), \
                                         torch.nn.ReLU(), \
                                         torch.nn.Linear(hidden_dim, output_dim))
        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # model = TheModelClass(*args, **kwargs)
        if load:
            self.model.load_state_dict(torch.load("./model"))
            self.model.eval() 

    def forward(self, state):
        return self.model(state)
