from ML.tagger import Tagger
from ML.network import Network
import torch

class NeuralTagger(Tagger):

    def __init__(self, targets, hidden_dim=100):
        self.targets = targets
        self.dim = len(targets)
        self.model = Network(hidden_dim, self.dim)

    def predict(self, state):
        scores = self.model.forward(state)
        #TODO: pick the best and valid 
        pred_target = scores.argmax()
        return pred_target