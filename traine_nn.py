from ML.neural_tagger_trainer import train_neural
from ML.nn_agent import NN_Agent
from ML.training_agent import Train
from ML.evaluvate import bench
from lib.world import World
from lib.state import State
from lib.ship import Ship
from config import *
from time import time
from random import shuffle
import torch
      
def main(model):
    start = time()
    print("Started Taining")
    network , optimizer = train_neural(Train ,State , World, Ship, n=TRAINING_ROUNDS, batch_size=BATCH_SIZR, model=model)
    print("Training Done in {:.2f} s".format((time() - start)))
    #TODO: save to file
    print(bench(network, BENCHMARK))
    if model == "":
        model = input("Name of the model:")
    torch.save({
            'model_state_dict': network.model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            }, f"ML/models/{model}")


if __name__ == "__main__":
    import sys
    print(len(sys.argv))
    if len(sys.argv) == 1:
        main("")
    else:
        main(sys.argv[1])