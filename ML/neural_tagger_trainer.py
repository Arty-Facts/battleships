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
            if torch.cuda.is_available() and GPU:
                return torch.tensor([c], dtype=torch.long).cuda()
            else:
                return torch.tensor([c], dtype=torch.long)
    print("oj oj")

def batchify(Agent ,State , World, Ship, targets, rev_targets, n, classifier, model):
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
            if torch.cuda.is_available() and GPU:
                game_state = agent.state.get2d().cuda()
            else:
                game_state = agent.state.get2d()
            x,y = agent.get_move(SEEK)
            hit, sink = world.shot(x,y)
            bx.append(game_state)
            
            if torch.cuda.is_available() and GPU:
                world_state = world.get2d().cuda()
            else:
                world_state = world.get2d()
            by.append(world_state)
            agent.result(x, y, hit, sink)
            if len(by) >= BATCH_SIZR:
                if torch.cuda.is_available() and GPU:
                    yield test, torch.stack(bx), torch.stack(by) 
                else:
                    yield test, torch.stack(bx), torch.stack(by)
                bx = []
                by = []
                test = False

def train_neural(Agent ,State , World, Ship, model="", n=1000):
    targets, rev_targets = make_targets(WORLD_SIZE_X,WORLD_SIZE_Y)
    classifier = NeuralTagger()
    optimizer = optim.Adam(classifier.model.parameters())
    if model != "":
        checkpoint = torch.load(model)
        classifier.model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    if torch.cuda.is_available() and GPU:
        classifier.model = classifier.model.cuda()

    for test, bx, by in batchify(Agent ,State , World, Ship, targets, rev_targets, n, classifier, model):
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

    checkpoint = torch.load( model)
    classifier.model.load_state_dict(checkpoint['model_state_dict'])
    if torch.cuda.is_available() and GPU:
        classifier.model = classifier.model.cuda()
    return classifier