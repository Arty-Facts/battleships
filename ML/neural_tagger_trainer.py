from ML.neural_tagger import NeuralTagger
from src.evaluvate import bench
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

def batchify(Agent ,State , World, Ship, targets,_size, _ships, n, batch_size):
    bx = []
    by = []
    test = False
    for t in range(n):
        if t%(10*batch_size) == 0:
            test = True

        if t%100==0:
            done = int(t/(n)*100)+1 
            left = 100-done
            #print(done)
            print("["+"+"*done + "-"*left+"]", done, "%", end="\r")
        world = World(_size,_size)
        state = State(_size,_size)
        agent = Agent(state)
        ships = [Ship(i) for i in range(2,_ships)]
        ships.append(Ship(3))
        launch(world, ships)
        counter = 0
        while(ships_left(ships)):
            counter += 1
            bx.append(torch.tensor(agent.state.get(), dtype=torch.float))
            x,y = agent.next_tile()
            hit = world.shot(x,y)
            agent.result(hit)
            by.append(targets[(x,y)])
            if len(by) >= batch_size:
                ans_bx = torch.stack(bx)
                ans_by = torch.tensor(by, dtype=torch.long)
                bx = []
                by = []
                yield test, ans_bx, ans_by
                test = False
        


def train_neural(Agent ,State , World, Ship ,_size, _ships, n=1000, batch_size=100):
    targets = make_targets(_size)
    classifier = NeuralTagger(targets)
    optimizer = optim.Adam(classifier.model.parameters())
    for test, bx, by in batchify(Agent ,State , World, Ship, targets, _size, _ships,n, batch_size):
        optimizer.zero_grad()
        output = classifier.model.forward(bx)
        loss = F.cross_entropy(output, by)
        loss.backward()
        optimizer.step()
        if test:
            print()
            print(bench(classifier,100))
    print()
    return classifier