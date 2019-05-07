class State():
    def __init__(self, width, higth):
        self.width = width
        self.higth = higth
        self.map = [['.'] * higth for _ in range(width)]

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

