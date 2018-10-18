import random


class Dice:
    def __init__(self):
        self.top = random.randint(1, 6)

    def __repr__(self):
        face = str(self.top)
        return face

    def __eq__(self, other):
        return self.top == other

    def __add__(self, other):
        return self.top + other

    def __radd__(self, other):
        return self.top + other

class YatzeeUpper:
    def __init__(self):
        self.Aces = 0
        self.Twos = 0
        self.Threes = 0
        self.Fours = 0
        self.Fives = 0
        self.Sixes = 0
        self.total_upper = (self.Aces +
                       self.Twos +
                       self.Threes +
                       self.Fours +
                       self.Fives +
                       self.Sixes)

        self.bonus = 35 if self.total_upper > 63 else 0

        self.total = self.total_upper + self.bonus

    def __str__(self):
        card = ["Aces total:" + str(self.Aces), "Twos total:" + str(self.Twos), "Threes total:" + str(self.Threes),
                "Fours total:" + str(self.Fours), "Fives total:" + str(self.Fives), "Sixes total:" + str(self.Sixes)]
        return str(card)

    def sum(self):
        return self.total

    def has_bonus(self):
        if self.bonus > 0:
            return True
        return False

    def pre_bonus(self):
        return self.total_upper

    def add_Aces(self, dice):
        if self.Aces != 0:
            print("You've already assigned a value to Aces.  That value is", self.Aces)
            return False
        else:
            for die in dice:
                if die == 1:
                    self.Aces += die
            return True


    def add_Twos(self, dice):
        if self.Twos != 0:
            print("You've already assigned a value to Twos.  That value is", self.Twos)
            return False
        else:
            for die in dice:
                if die == 2:
                    self.Twos += die
            return True

    def add_Threes(self, dice):
        if self.Threes != 0:
            print("You've already assigned a value to Threes.  That value is", self.Threes)
            return False
        else:
            for die in dice:
                if die == 3:
                    self.Threes += die
            return True

    def add_Fours(self, dice):
        if self.Fours != 0:
            print("You've already assigned a value to Fours.  That value is", self.Fours)
            return False
        else:
            for die in dice:
                if die == 4:
                    self.Fours += die
            return True

    def add_Fives(self, dice):
        if self.Fives != 0:
            print("You've already assigned a value to Fives.  That value is", self.Fives)
            return False
        else:
            for die in dice:
                if die == 5:
                    self.Fives += die
            return True

    def add_Sixes(self, dice):
        if self.Sixes != 0:
            print("You've already assigned a value to Sixes.  That value is", self.Sixes)
            return False
        else:
            for die in dice:
                if die == 6:
                    self.Sixes += die
            return True

    def check_value(self, die):
        if ((die == 1 and self.Aces == 0)
             or (die == 2 and self.Twos == 0)
             or (die == 3 and self.Threes == 0)
             or (die == 4 and self.Fours == 0)
             or (die == 5 and self.Fives == 0)
             or (die == 6 and self.Sixes == 0)):
                return True
        return False


class YatzeeLower:
    def __init__(self):
        self.threekind = 0
        self.fourkind = 0
        self.fullhouse = 0
        self.smstrt = 0
        self.lgstrt = 0
        self.yatzee = 0
        self.chance = 0
        self.yatzeebonus = 0
        self.total_lower = (self.threekind +
                            self.fourkind +
                            self.fullhouse +
                            self.smstrt +
                            self.lgstrt +
                            self.yatzee +
                            self.change +
                            self.yatzeebonus)

def die_roll():
    dice = []
    for die in range(7):
        dice.append(Dice())
    print(dice)
    return dice


def main():
    gamecard = YatzeeUpper()
    while True:
        option = []
        cnt1 = 0
        cnt2 = 0
        cnt3 = 0
        cnt4 = 0
        cnt5 = 0
        cnt6 = 0
        input("roll dice?")
        gameroll = die_roll()
        for die in gameroll:
            if die == 1 and gamecard.check_value(die):
                if "Aces" not in option:
                    option.append("Aces")
                cnt1 += 1
            elif die == 2 and gamecard.check_value(die):
                if "Twos" not in option:
                    option.append("Twos")
                cnt2 += 1
            elif die == 3 and gamecard.check_value(die):
                if "Threes" not in option:
                    option.append("Threes")
                cnt3 += 1
            elif die == 4 and gamecard.check_value(die):
                if "Fours" not in option:
                    option.append("Fours")
                cnt4 +=1
            elif die == 5 and gamecard.check_value(die):
                if "Fives" not in option:
                    option.append("Fives")
                cnt5 += 1
            elif die == 6 and gamecard.check_value(die):
                if "Sixes" not in option:
                    option.append("Sixes")
                cnt6 += 1
        choices = ""
        for i in option:
            choices += i
            choices += "\n"

        choice = input(choices)
        if choice == "Aces":
            gamecard.add_Aces(gameroll)
        elif choice == "Twos":
            gamecard.add_Twos(gameroll)
        elif choice == "Threes":
            gamecard.add_Threes(gameroll)
        elif choice == "Fours":
            gamecard.add_Fours(gameroll)
        elif choice == "Fives":
            gamecard.add_Fives(gameroll)
        elif choice == "Sixes":
            gamecard.add_Sixes(gameroll)

        print(gamecard)


main()