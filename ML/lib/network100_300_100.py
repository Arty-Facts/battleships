import torch

class Network100_300_100(torch.nn.Module):

    def __init__(self,input_dim, hidden_dim, output_dim):
        super().__init__()
        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # model = TheModelClass(*args, **kwargs)
        self.model = torch.nn.Sequential(torch.nn.Linear(input_dim, hidden_dim), \
                                        torch.nn.ReLU(), \
                                        torch.nn.Linear(hidden_dim, output_dim))
        

    def forward(self, state):
        return self.model(state)
