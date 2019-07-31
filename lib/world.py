from random import randint, shuffle, seed

class World():
    def __init__(self, width, higth):
        self.width = width
        self.higth = higth
        self.map = [[None] * higth for _ in range(width)]
        self.ships = {}
        self._dir = [(1,0),(-1,0),(0,1),(0,-1)]

    def __repr__(self):
        res = ""
        for x in range(self.width):
            for y in range(self.higth):
                if self.free(x,y):
                    res += "~ "
                elif self.map[x][y].sunk():
                    res += "X "
                else: 
                    res += str(self.map[x][y].id) + " "
            res += "\n"
        return res

    def free(self,x,y):
        if x < 0 or x >= self.width or y < 0 or y >= self.higth:
            return False
        return self.map[x][y] == None

    def shot(self, x, y):
        if self.map[x][y] != None:
            self.map[x][y].hit()
            sunk = self.map[x][y].sunk()
            self.map[x][y] = None
            return True , sunk
        return False, False

    def check(self, x, y):
        if self.map[x][y] != None:
            return True
        return False
    
    def add(self, ship):
        #seed(1337)
        while(not self.present(ship.id)):
            x, y = self.random()
            shuffle(self._dir)
            for dir_x, dir_y in self._dir:
                for i in range(ship.hp):
                    if not self.free(x+(dir_x*i),y+(dir_y*i)):
                        break
                else:
                    for i in range(ship.hp):
                        self.map[x+(dir_x*i)][y+(dir_y*i)] = ship
                    self.ships[ship.id] = ship
                    return

    def present(self, id):
        return id in self.ships

    def random(self):
        return randint(0, self.width-1), randint(0, self.higth-1)

