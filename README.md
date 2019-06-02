# Agents playing batlleships 
Agents are inspired by http://www.datagenetics.com/blog/december32011/
and the montecarlo implematation uses DataSnaek implementation from https://github.com/DataSnaek/battleships_ai as a base

## Interface
Agent have an internarepresentaion of the gamestate.

When calling **next_tile()** the agent will supply the next target to fire upon.

The agent updates its internal state when reciving **result(x, y, hit, sink)**


## run

```
python3 eval_bots.py
```

## Configure configure 

All configuration are in config.py in root folder

## latest run
```
Benshmarking with 100 games

95.60 moves: RandomAgent
63.87 moves: HuntTarget
60.24 moves: HuntTargetParity
58.06 moves: MonteCarlo
52.29 moves: MonteCarloSinc 
```
