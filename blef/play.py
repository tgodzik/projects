# create own scenario and try to get the best possible strategy


class Player:

    def __init__(self):
        self.name = None
        self.dices = None
        self.my_points = 0

    def setName(self, i):
        self.name = i

    def start(self, dice):
        self.dices = dice

    def play(self, history):
        return "CHECK"

    def result(self, points):
        self.my_points += points[self.name]