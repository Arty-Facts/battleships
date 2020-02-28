from random import randint, shuffle
from config import *
import torch

class State():
    def __init__(self, width, higth):
        self.latest_result = 0
        self.ticks = width * higth
        self.width = width
        self.higth = higth
        self.map = [['.'] * higth for _ in range(width)]
        self._dir = [(1,0),(0,1)]
        self.ships_left = len(SHIPS)
        self.tiles_left = sum(SHIPS)
        self.targets = []
        for x in range(WORLD_SIZE_X):
            for y in range(WORLD_SIZE_Y):
                self.targets.append((x,y))

    def __repr__(self):
        res = ""
        for x in range(self.width):
            for y in range(self.higth):
                res += self.map[x][y] + " "
            res += "\n"
        return res
    
    def hit(self, x, y):
        self.latest_result = 1
        self.ticks -= 1
        self.map[x][y] = 'X'

    def sinc(self, x, y):
        self.latest_result = 2
        self.ticks -= 1
        self.map[x][y] = '*'
    
    def miss(self, x, y):
        self.latest_result = 0
        self.ticks -= 1
        self.map[x][y] = '~'

    def free(self,x,y):
        if x < 0 or x >= self.width or y < 0 or y >= self.higth:
            return False
        return self.map[x][y] == '.'

    def overlap(self,x,y):
        if x < 0 or x >= self.width or y < 0 or y >= self.higth:
            return False
        return self.map[x][y] == 'X'

    def blocked(self,x,y):
        if x < 0 or x >= self.width or y < 0 or y >= self.higth:
            return True
        return self.map[x][y] == '~' or self.map[x][y] == '*'

    def add(self, length):
        res = []
        shuffle(self.targets)
        for x, y in self.targets:
            shuffle(self._dir)
            for dir_x, dir_y in self._dir:
                for i in range(length):
                    if self.blocked(x+(dir_x*i),y+(dir_y*i)):
                        break
                else:
                    for i in range(length):
                        res.append((x+(dir_x*i),y+(dir_y*i)))
                    return res
        return None


    def random(self):
        return randint(0, self.width-1), randint(0, self.higth-1)

    def get_map(self):
        res = [[0] * self.higth for _ in range(self.width)]
        for x in range(self.width):
            for y in range(self.higth):
                c = self.map[x][y]
                if c == ".":
                    res[x][y] = 0
                elif c == "~":
                    res[x][y] = 1
                elif c == "X":
                    res[x][y] = 2
        return res

    def get(self):
        res = []
        for x in range(self.width):
            for y in range(self.higth):
                c = self.map[x][y]
                if c == ".":
                    res.append(0)
                elif c == "~":
                    res.append(1)
                elif c == "X":
                    res.append(2)
        return res
    def get2d(self):
        shape = self.width, self.higth
        unk = torch.zeros(shape, dtype=torch.float)
        ships = torch.zeros(shape, dtype=torch.float)
        water = torch.zeros(shape, dtype=torch.float)
        for x in range(self.width):
            for y in range(self.higth):
                c = self.map[x][y]
                if c == ".":
                    unk[x,y] = 1
                elif c == "~":
                    water[x,y] = 1
                elif c == "X":
                    ships[x,y] = 1
        return torch.stack([ships, water, unk])

    
    def get_one_hot(self):
        res = []
        for x in range(self.width):
            for y in range(self.higth):
                c = self.map[x][y]
                if c == ".":
                    res += [1,0,0]
                elif c == "~":
                    res += [0,1,0]
                else:
                    res += [0,0,1]


        return res

