from lib.world import World
from lib.state import State
from lib.ship import Ship
from agents.random_agent import RandomAgent

_size = 100
_ships = 40

def ships_left(ships):
    for s in ships:
        if not s.sunk():
            return True
    return False

def launch(world, ships):
    ships.sort(key=lambda s:s.hp, reverse=False)
    for s in ships:
        world.add(s)

def run(world, agent):
    ships = [Ship(i) for i in range(2,_ships)]
    ships.append(Ship(3))
    launch(world, ships)
    counter = 0
    while(ships_left(ships)):
        counter += 1
        x,y = agent.next_tile()
        hit = world.shot(x,y)
        agent.result(hit)
    return counter
        
def main():
    world = World(_size,_size)
    print(world)
    state = State(_size,_size)
    agent = RandomAgent(state)

    counter = run(world, agent)
        
    print("Done in", counter, "moves")




if __name__ == "__main__":
    main()