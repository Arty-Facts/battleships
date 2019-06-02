from ML.evaluvate import bench
from ML.neural_tagger_trainer import load_model
from config import *

if __name__ == "__main__":
    #main()
    models = ["taghunt", "taghunt200k", "taghunt500k"]
    print("Benshmarking with", BENCHMARK, "games")
    for model in models:
        agent = load_model(model)
        print("{:.2f} moves: {}".format(bench(agent, BENCHMARK), model))