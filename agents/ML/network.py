import torch

class Network(torch.nn.Module):

    def __init__(self,input_dim=100, hidden_dim=100, output_dim=100):
        super().__init__()
        self.model = torch.nn.Sequential(torch.nn.Linear(input_dim, hidden_dim), \
                                         torch.nn.ReLU(), \
                                         torch.nn.Linear(hidden_dim, output_dim))

    def forward(self, features):
        input_data = torch.tensor(features)
        return self.model(input_data)
