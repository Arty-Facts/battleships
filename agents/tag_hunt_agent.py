from random import randint, shuffle
class TagHunt():

    def __init__(self, state):
        self.state = state
        self.hunt = False
        self.x, self.y = -1, -1
        self.tag_x, self.tag_y = -1, -1
        self._dir = [(1,0),(-1,0),(0,1),(0,-1)]
        self.hit = False

    def next_tile(self):
        if self.hunt:
            if self.hit and self.x != self.tag_x and self.y != self.tag_y:
                if self.x == self.tag_x:
                    self.y = self.y+1 if self.y - self.tag_y > 0 else self.y -1 
                else:
                    self.x = self.x+1 if self.x - self.tag_x > 0 else self.x -1 
                return self.x, self.y
            else:
                shuffle(self._dir)
                for dir_x, dir_y in self._dir:
                    if self.state.free(self.tag_x+dir_x,self.tag_y+dir_y):
                        self.x = self.tag_x + dir_x
                        self.y = self.tag_y + dir_y
                        return self.x, self.y
                        
                # for dir_x, dir_y in self._dir:
                #     if self.state.free(self.x+dir_x,self.y+dir_y):
                #         self.x += dir_x
                #         self.y += dir_y
                #         return self.x, self.y
                self.hunt = False 

        if not self.hunt:
            self.x, self.y = self.random()
            while(not self.state.free(self.x,self.y)):
                self.x, self.y = self.random()
            return self.x, self.y


    def result(self, hit):
        self.hit = hit
        if hit:
            self.state.hit(self.x, self.y)
            if not self.hunt:
                self.tag_x = self.x
                self.tag_y = self.y
            self.hunt = True
            print(self.state)
        else:
            self.state.miss(self.x, self.y)

    def random(self):
        return randint(0, self.state.width-1), randint(0, self.state.higth-1)