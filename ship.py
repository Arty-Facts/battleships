from itertools import count

class Ship():
    _ids = count(0)
    def __init__(self, hp):
        if hp < 2:
            raise "Ship has to have atleast 2 hp"
        self.hp = hp
        self.id = next(Ship._ids)

    def hitt(self):
        self.hp -= 1
    
    def sunk(self):
        return self.hp <= 0
    