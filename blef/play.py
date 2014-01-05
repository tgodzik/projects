# create own scenario and try to get the best possible strategy
import random
import math


class Strategy:

    def __init__(self):
        pass

    delta_base = 0.0
    delta_period = 0.05

    @staticmethod
    def one_better(value):
        """
        The next correct setting.
        """
        dice_list = [s for s in value]
        for i in range(1, 6):
            if dice_list.count(str(i)) > 0:
                dice_list.append(str(i + 1))
                dice_list.remove(str(i))
                break
        dice_list.sort()
        return "".join(dice_list)

    @staticmethod
    def better(value, num):
        """
        The next correct setting.
        """
        ret = value
        for i in range(0,num):
            ret = Strategy.one_better(ret)
        return ret

    @staticmethod
    def is_possible(mine, current):
        """
        Returns a tuple - (can the setting exist, with what probability should we check)
        """
        to_check = [s for s in current][0:len(mine)]
        checkit = zip(mine, to_check)
        for my, other in checkit:
            if int(my) < int(other):
                return False, 1.0

        # add a random delta to add some unpredictability, now it provokes more cheating checking
        delta = Strategy.delta_base + random.random()/(100.0 / Strategy.delta_period)
        to_check = [s for s in current]

        minecp = mine[:]
        minecp.reverse()
        for i in minecp:
            ren = range(1, int(i)+1)
            ren.reverse()
            for j in ren:
                if to_check.count(str(j)) > 0:
                    to_check.remove(str(j))
                    break
        mx = math.pow(6, len(to_check))
        acc = 1.0
        for i in to_check:
            acc *= float(i)
        pos = (acc - 1.0) / mx
        if pos > 0:
            pos += delta
        return True, pos


class Player:
    def __init__(self):
        self.name = None
        self.dices = None
        self.my_points = 0

    def setName(self, i):
        """
        We do not count our moves into the trustworthiness
        """
        self.name = str(i)

    def start(self, dice):
        self.dices = dice
        self.dices.sort()

    def play(self, history):
        res = Strategy.is_possible(self.dices, history[0][1])
        if not res[0]:
            return "CHECK"
        else:
            if res[1] < random.random():
                return "CHECK"
            else:
                return Strategy.one_better(history[0][1])

    def result(self, points, dices):
        """
        Influence on delta (Strategy.delta_base / delta_period):
        1. The higher the points the more we can risk and the other way?
        2. Check the trustworthiness of previous player to determine the next delta.
        3. Maybe influence the leap.
        """
        self.my_points += points[self.name]


#p1 = Player()
#p1.setName("1")
#p1.start([3, 4])
#
#print p1.play([(4,"3444")])