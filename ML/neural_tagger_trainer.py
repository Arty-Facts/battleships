from ML.neural_tagger import NeuralTagger
from ML.evaluvate import bench
from config import *
from collections import defaultdict
import torch.nn.functional as F
import torch.optim as optim
import torch
from random import shuffle

def make_targets(size):
    targets = {}
    for x in range(size):
        for y in range(size):
            targets[(x,y)] = len(targets)
    return targets

def ships_left(ships):
    for s in ships:
        if not s.sunk():
            return True
    return False

def launch(world, ships):
    shuffle(ships)
    #ships.sort(key=lambda s:s.hp, reverse=False)
    for s in ships:
        world.add(s)

def get_move(agent, world):
    x, y = 0, 0
    for _ in range(4):
        x,y = agent.next_tile()
        if world.check(x,y):
            return x,y
    return x,y


def batchify(Agent ,State , World, Ship, targets, n, batch_size):
    bx = []
    by = []
    test = False
    for t in range(n):
        if (t+1)%(EVAL_EVERY) == 0:
            test = True

        if t%100==0:
            done = int(t/(n)*100)+1 
            left = 100-done
            #print(done)
            print("["+"+"*done + "-"*left+"]", done, "%", end="\r")
        world = World(WORLD_SIZE,WORLD_SIZE)
        state = State(WORLD_SIZE,WORLD_SIZE)
        agent = Agent(state, world)
        ships = [Ship(i) for i in SHIPS]
        launch(world, ships)
        counter = 0
        while(ships_left(ships)):
            counter += 1
            bx.append(torch.tensor(agent.state.get_one_hot(), dtype=torch.float))
            x,y = agent.get_move()
            hit = world.shot(x,y)
            agent.result(hit, x, y)
            by.append(targets[(x,y)])
            if len(by) >= batch_size:
                ans_bx = torch.stack(bx)
                ans_by = torch.tensor(by, dtype=torch.long)
                bx = []
                by = []
                yield test, ans_bx, ans_by
                test = False
        


def train_neural(Agent ,State , World, Ship, model="", n=1000, batch_size=100):
    targets = make_targets(WORLD_SIZE)
    classifier = NeuralTagger(len(targets)*3,len(targets))
    optimizer = optim.Adam(classifier.model.parameters())
    if model != "":
        checkpoint = torch.load( f"ML/models/{model}")
        classifier.model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    for test, bx, by in batchify(Agent ,State , World, Ship, targets, n, batch_size):
        optimizer.zero_grad()
        output = classifier.model.forward(bx)
        loss = F.cross_entropy(output, by)
        loss.backward()
        optimizer.step()
        if test and EVAL:
            print()
            print(bench(classifier,EVAL_FOR))
    print()
    return classifier, optimizer

def load_model(model):
    targets = make_targets(WORLD_SIZE)
    classifier = NeuralTagger(len(targets)*3,len(targets))

    checkpoint = torch.load( f"ML/models/{model}")
    classifier.model.load_state_dict(checkpoint['model_state_dict'])
    return classifier