from ML.evaluvate import bench
from ML.neural_tagger_trainer import load_model
from config import *

if __name__ == "__main__":
    #main()
    models = ["taghunt300k_lern100k", "taghunt300k", "taghunt200k", "taghunt200k_2seek100k", "taghunt200k_2seek100k_4seek100k"]
    print("Benshmarking with", BENCHMARK, "games")
    for model in models:
        agent = load_model(model)
        print("{:.2f} moves: {}".format(bench(agent, BENCHMARK), model))