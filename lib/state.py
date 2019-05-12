from random import randint, shuffle
class State():
    def __init__(self, width, higth):
        self.width = width
        self.higth = higth
        self.map = [['.'] * higth for _ in range(width)]
        self.ships = None
        self._dir = [(1,0),(-1,0),(0,1),(0,-1)]

    def __repr__(self):
        res = ""
        for x in range(self.width):
            for y in range(self.higth):
                res += self.map[x][y] + " "
            res += "\n"
        return res
    
    def hit(self, x, y):
        self.map[x][y] = 'X'
    
    def miss(self, x, y):
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
        return self.map[x][y] == '~'

    def add(self, length):
        res = []
        for i in range(10000):
            x, y = self.random()
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
                else:
                    res.append(3)
        return res
    
    def get_one_hot(self):
        res = []
        for x in range(self.width):
            for y in range(self.higth):
                c = self.map[x][y]
                if c == ".":
                    res += [1,0,0]
                elif c == "~":
                    res += [0,1,0]
                elif c == "X":
                    res += [0,0,1]
                else:
                    raise "cant create one_hot"

        return res

