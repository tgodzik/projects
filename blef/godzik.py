# create own scenario and try to get the best possible strategy
import random
import math


class Strategy:
    """
    Additional methods adding in choosing the right strategy
    """

    def __init__(self):
        """
        Constructor - unused
        """
        pass

    # deviation of current behavior ( - more risky, + less risky)
    delta_base = 0.0
    # period of the deviation
    delta_period = 0.05

    @staticmethod
    def cautious():
        """
        Increases cautioness level
        """
        Strategy.delta_base += 0.1

    @staticmethod
    def risky():
        """
        Makes more risky
        """
        Strategy.delta_base -= 0.1

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
        The next correct setting by num.
        """
        ret = value
        for i in range(0,num):
            ret = Strategy.one_better(ret)
        return ret

    @staticmethod
    def is_possible(mine, current, use_delta=True):
        """
        Returns a tuple - (can the setting exist, with what probability should we check)
        """
        to_check = [s for s in current][0:len(mine)]
        checkit = zip(mine, to_check)
        for my, other in checkit:
            if int(my) < int(other):
                return False, 1.0

        # add a random delta to add some unpredictability, now it provokes more cheating checking
        if use_delta:
            delta = Strategy.delta_base + random.random()/(100.0 / Strategy.delta_period)
        else:
            delta = 0.0

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
    """
    The player class
    """
    def __init__(self):
        """
        Sst all the important parameters
        """
        self.name = None
        self.dices = None
        self.my_points = 0
        self.turn = 0
        self.last = "1111"
        self.checked = False

    def setName(self, i):
        """
        That's not my name.
        """
        self.name = i

    def start(self, dice):
        """
        Start new game and setup parameters
        """
        self.dices = dice
        self.dices.sort()
        self.checked = False

    def play(self, history):
        """
        One turn
        """
        if len(history) == 0:
            return "1"*(self.turn+4)
        res = Strategy.is_possible(self.dices, history[0][1])
        self.last = history[0]
        if not res[0]:
            self.checked = True
            return "CHECK"
        else:
            if res[1] > random.random():
                self.checked = True
                return "CHECK"
            else:
                return Strategy.one_better(history[0][1])

    def result(self, points, dices, history):
        """
        Check how the game went.
        """
        # update values

        self.turn += 1
        self.my_points += points[self.name-1]

        # check previous player
        prev_player = self.last[0]-1
        prev_turn = self.last[1]
        prev_prob = Strategy.is_possible(dices[prev_player], prev_turn, use_delta=False)

        # we lost with the previous, is he a risk taker and we did not check?
        if points[self.name-1] == -1 and points[prev_player] == 1 and prev_prob[1] > 0.4 and not self.checked:
            # check more often
            Strategy.cautious()

        # we lost with the previous, is he very careful?
        if points[self.name-1] == -1 and points[prev_player] == 1 and prev_prob[1] < 0.1 and self.checked:
            # check less often
            Strategy.risky()

        # check next player
        next_player = self.name % 4
        next_turn = Strategy.one_better(prev_turn)
        next_prob = Strategy.is_possible(dices[next_player], next_turn, use_delta=False)

        # we lost with the next, is he more cautious?
        if points[next_player] == 1 and points[self.name-1] == -1 and next_prob[1] < 0.1:
            # risk less
            Strategy.cautious()
