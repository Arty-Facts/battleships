from world import World
from state import State
from agent import Agent
from ship import Ship

def ships_left(ships):
    for s in ships:
        if not s.sunk():
            return True
    return False

def launch(world, ships):
    ships.sort(key=lambda s:s.hp, reverse=False)
    for s in ships:
        world.add(s)
        
def main():
    world = World(100,100)
    ships = [Ship(i) for i in range(2,40)]
    ships.append(Ship(3))
    launch(world, ships)
    print(world)
    state = State(100,100)
    agent = Agent(state)
    counter = 0
    while(ships_left(ships)):
        counter += 1
        x,y = agent.next_tile()
        hit = world.shot(x,y)
        agent.result(hit)
        
    print("Done in", counter, "moves")




if __name__ == "__main__":
    main()