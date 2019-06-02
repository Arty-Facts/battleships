from ML.tagger import Tagger
from ML.network import Network
import torch

class NeuralTagger(Tagger):

    def __init__(self,input_dim, target_dim, hidden_dim=300,):
        self.model = Network(input_dim,hidden_dim, target_dim)

    def predict(self, state, targets):
        inp = torch.tensor(state.get(), dtype=torch.float)
        scores = self.model.forward(inp)
        #TODO: pick the best and valid 
        res = []
        for c,s in enumerate(scores):
            res.append((c,s))
        for c,s in sorted(res, key=lambda x:x[1], reverse=True):
            x,y = targets[c]
            if state.free(x,y):
                return x,y

        raise("No moves left")