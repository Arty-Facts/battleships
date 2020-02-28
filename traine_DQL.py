from lib.world import World
from lib.state import State
from lib.ship import Ship
from agents.DQL_agent import Agent
from random import shuffle
from util.evaluvate import launch, plotLearning
from config import *
import numpy as np

def make_targets(size_x, size_y):
    targets = {}
    rev_targets = []
    for x in range(size_x):
        for y in range(size_y):
            targets[(x,y)] = len(targets)
            rev_targets.append((x,y))
    return targets, rev_targets

def get_best_ans(scores, state, world, targets):
    res = []
    #print(scores)
    for c,s in enumerate(scores):
        #print(c)
        res.append((c,s))
    for c,s in sorted(res, key=lambda x:x[1], reverse=True):
        #print(s)
        x,y = targets[c]
        #print(x,y)
        if state.free(x,y):# and world.check(x,y):
            #print(x,y, c)
            #print(state)
            return c
    print("oj oj")

def main():
    size = WORLD_SIZE_X * WORLD_SIZE_Y
    _ , targets = make_targets(WORLD_SIZE_X,WORLD_SIZE_Y)

    gamma=0.99
    alpha=5e-5
    eps_dec=0.99998
    scores = []
    eps_history = []
    num_games = 100_000
    score = 0
    load_checkpoint = False

    agent = Agent(gamma=gamma, epsilon=1.0, alpha=alpha,
                  input_dims=[size], n_actions=size, mem_size=10_000_000, eps_min=0.01,
                  batch_size=64, eps_dec=eps_dec, replace=100)

    if load_checkpoint:
        agent.load_models()

    for i in range(num_games):
        if i % 10 == 0 and i > 0:
            avg_score = np.mean(scores[max(0, i-10):(i+1)])
            print('episode: ', i,'score: ', score,
                 ' average score %.3f' % avg_score,
                'epsilon %.3f' % agent.epsilon)
        else:
            print('episode: ', i,'score: ', score)
        eps_history.append(agent.epsilon)
        done = False
        state = State(WORLD_SIZE_X,WORLD_SIZE_Y)
        world = World(WORLD_SIZE_X,WORLD_SIZE_Y)
        ships = [Ship(i) for i in SHIPS]
        launch(world, ships)

        score = 0
        while not done:
            curr_state = state.get()
            #print(state)
            action = agent.choose_action(curr_state, state, targets)
            #action = get_best_ans(actions, state, world, targets)
            x, y = targets[action]
            hit, _ = world.shot(x, y)
            if hit:
                state.hit(x,y)
            else:
                state.miss(x,y)
            reward = state.reward()
            #print(world.ships_left)
            if state.ticks <= 0 or world.ships_left == 0:
                done = True
            score += 1
            agent.store_transition(curr_state, action, reward, state.get(),
                                  done)
            agent.learn()
            # if done:
            #     print(state)



        scores.append(score)
        if i%100 == 0:
            x = [j+1 for j in range(i+1)]
            filename = 'Curr_Games' + 'Gamma' + str(gamma) + \
                        'Alpha' + str(alpha) +'Dec' + str(eps_dec) +'.png'
            plotLearning(x, scores, eps_history, filename)

    x = [i+1 for i in range(num_games)]
    filename = str(num_games) + 'Games' + 'Gamma' + str(gamma) + \
                'Alpha' + str(alpha) +'Dec' + str(eps_dec) +'.png'
    plotLearning(x, scores, eps_history, filename)


if __name__ == "__main__":
    main()

