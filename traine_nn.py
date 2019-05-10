from ML.neural_tagger_trainer import train_neural
from agents.nn_agent import NN_Agent
from agents.training_agent import Train
from src.evaluvate import bench
from lib.world import World
from lib.state import State
from lib.ship import Ship
from lib.constents import *
from time import time
from random import shuffle
import torch
      
def main():
    start = time()
    print("Started Taining")
    network = train_neural(Train ,State , World, Ship, n=TRAINING_ROUNDS, batch_size=BATCH_SIZR)
    print("Training Done in {:.2f} s".format((time() - start)))
    #TODO: save to file
    print(bench(network, EVAL_FINAL))

if __name__ == "__main__":
    main()