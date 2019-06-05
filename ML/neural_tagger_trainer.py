from ML.neural_tagger import NeuralTagger
from ML.evaluvate import bench
from config import *
from collections import defaultdict
import torch.nn.functional as F
import torch.optim as optim
import torch
from random import shuffle

def make_targets(size_x, size_y):
    targets = {}
    rev_targets = []
    for x in range(size_x):
        for y in range(size_y):
            targets[(x,y)] = len(targets)
            rev_targets.append((x,y))
    return targets, rev_targets

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
        
def get_best_ans(scores, state, world, targets):
    res = []
    #print(scores)
    for c,s in enumerate(scores[0]):
        #print(c)
        res.append((c,s))
    for c,s in sorted(res, key=lambda x:x[1], reverse=True):
        #print(s)
        x,y = targets[c]
        #print(x,y)
        if state.free(x,y) and world.check(x,y):
            #print(x,y, c)
            #print(state)
            return torch.tensor([c], dtype=torch.long)
    print("oj oj")

def batchify(Agent ,State , World, Ship, targets, rev_targets, n, classifier):
    bx = []
    by = []
    test = False
    for t in range(n):
        if (t+1)%(EVAL_EVERY) == 0:
            test = True

        if t%10==0:
            done = int(t/(n)*100)+1 
            left = 100-done
            #print(done)
            print("["+"+"*done + "-"*left+"]", done, "%", end="\r")
        world = World(WORLD_SIZE_X,WORLD_SIZE_Y)
        state = State(WORLD_SIZE_X,WORLD_SIZE_Y)
        agent = Agent(state, world)
        ships = [Ship(i) for i in SHIPS]
        launch(world, ships)
        counter = 0
        while(ships_left(ships)):
            counter += 1
            game_state = torch.tensor(agent.state.get(), dtype=torch.float)
            x,y = agent.get_move(1)
            hit, sink = world.shot(x,y)
            output = classifier.model.forward(torch.stack([game_state]))
            best = get_best_ans(output, state, world, rev_targets)
            agent.result(x, y, hit, sink)
            bx.append(game_state)
            by.append(best)
            #by.append(targets[(x,y)])
            if len(by) >= BATCH_SIZR:
                yield test, torch.stack(bx), torch.tensor(by, dtype=torch.long) 
                bx = []
                by = []
                test = False

def train_neural(Agent ,State , World, Ship, model="", n=1000):
    targets, rev_targets = make_targets(WORLD_SIZE_X,WORLD_SIZE_Y)
    classifier = NeuralTagger(len(targets),len(targets))
    optimizer = optim.Adam(classifier.model.parameters())
    if model != "":
        checkpoint = torch.load( f"ML/models/{model}")
        classifier.model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    for test, bx, by in batchify(Agent ,State , World, Ship, targets, rev_targets, n, classifier):
        optimizer.zero_grad()
        output = classifier.model.forward(bx)
        loss = F.cross_entropy(output, by)
        loss.backward()
        optimizer.step()
        if test and EVAL_DURING_RUNTIME:
            print()
            print(bench(classifier,EVAL_ROUNDS))
    print("["+"+"*100 +"]", 100, "%")
    return classifier, optimizer

def load_model(model):
    _, targets = make_targets(WORLD_SIZE_X,WORLD_SIZE_Y)
    classifier = NeuralTagger(len(targets),len(targets))

    checkpoint = torch.load( f"ML/models/{model}")
    classifier.model.load_state_dict(checkpoint['model_state_dict'])
    return classifier