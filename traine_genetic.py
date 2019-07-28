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
from pathlib import Path
import torch
PATH
def train(model):
    start = time()
    name_gen = Path(model).name.split(".")
    gen = 1
    if len(name_gen) == 1:
        name = name_gen[0]
    else:
        name, gen = name_gen
    print("Started Taining")
    print("Models start at:", name, "Genaration", gen)
    network , optimizer = train_neural(Train ,State , World, Ship, n=TRAINING_ROUNDS, model=model)
    print("Training Done in {:.2f} s".format((time() - start)))
    score = bench(network, BENCHMARK)
    print("Resulting score:", score)
    torch.save({
            'model_state_dict': network.model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            }, f"{PATH}/{int(score)}.{int(gen)+1}")

    
def main():
    while True:
        path = Path(PATH)
        models = [str(x.name).split('.') + [x] for x in path.iterdir() if x.is_file()]
        models = sorted(models)
        for m in models:
            print(m)
        if len(models) == 0:
            train("")
        else:
            for s,g, m in models:
                train(m)
        models = sorted([str(x.name).split('.') + [x] for x in path.iterdir() if x.is_file()])
        removed = 0
        if len(models) > GENARATIONS*1.5:
            for i in range(1, len(models)):
                if models[i-1][0] == models[i][0]:
                    models[i-1][2].unlink() 
                    removed += 1
                if not (len(models) - removed > GENARATIONS*1.5):
                    break 

        if len(models) > GENARATIONS:
            for s, g , m in models[GENARATIONS+1:]:
                m.unlink() 



if __name__ == "__main__":
    import sys
    main()