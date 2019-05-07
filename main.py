from world import World
from ship import Ship



def launch(world, ships):
    ships.sort(key=lambda s:s.hp, reverse=True)
    for s in ships:
        world.add(s)
        
def main():
    world = World(10,10)
    ships = [Ship(i) for i in range(2,6)]
    ships.append(Ship(3))
    launch(world, ships)
    print(world)

    # for _ in range(3):
    #     for s in ships:
    #         s.hitt()

    #         s.hitt()
    #     print(world)

    
    pass



if __name__ == "__main__":
    main()