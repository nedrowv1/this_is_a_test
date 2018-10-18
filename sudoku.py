from numpy.random import randint
from random import sample

def updates(row, column1, column2, column3, temp_index, num, row_dex1, row_dex2, row_dex3, col_dex):
    if temp_index == 0 or temp_index == 3 or temp_index == 6:
        row.add(row_dex1, num)
        column1.add(col_dex, num)
    elif temp_index == 1 or temp_index == 4 or temp_index == 7:
        row.add(row_dex2, num)
        column2.add(col_dex, num)
    elif temp_index == 2 or temp_index == 5 or temp_index == 8:
        row.add(row_dex3, num)
        column3.add(col_dex, num)


def New_Game(puzzle):
    seed_list = randint(0, 10, randint(15, 20))
    A = ["_"] * 9
    A[randint(0, 10)] = sample(seed_list)
    print(A)

def bottom(cell1, cell2, cell3):
    line = "|_" + str(cell1) + "_|_" + str(cell2) + "_|_" + str(cell3) + "_|"
    return line


def cell(cell_value):
    up = " ___ "
    down = "|_" + str(cell_value) + "_|"
    print(up)
    print(down)


def tops():
    print(" ___________ ", end="")


def row(box_row):
    print(bottom(box_row[0], box_row[1], box_row[2]), end="")


def column(col_list):
    for i in range(9):
        cell(col_list[i])


class sudoku_box():
    def __init__(self, box_list):
        self.box = []
        for i in range(9):
            self.box.append(box_list[i])

    def add(self, index, value):
        self.box[index] = value

    def check_eq(self):
        found = [False] * 10
        for i in self.box:
            if i == "_":
                return False
            for k in range(1, 11):
                if i == k:
                    if not found[k]:
                        found[k] = True
                    else:
                        return False
        for k in range(len(found)):
            if not k and k != 0:
                return False
        return True

    def __str__(self):
        tops()
        print()
        row(self.box[0, 3])
        print()
        row(self.box[3, 6])
        print()
        row(self.box[6, 9])
        return " "

    def disp_row(self, row_index):
        if row_index == 0:
            return self.box[0:3]
        elif row_index == 1:
            return self.box[3:6]
        elif row_index == 2:
            return self.box[6:9]

    def disp_column(self, col_index):
        if col_index == 0:
            return [self.box[0], self.box[3], self.box[6]]
        elif col_index == 1:
            return [self.box[1], self.box[4], self.box[7]]
        elif col_index == 2:
            return [self.box[2], self.box[5], self.box[8]]


class sudoku_column():
    def __init__(self, list1, list2, list3):
        self.column = [list1[0], list1[1], list1[2], list2[0], list2[1], list2[2], list3[0], list3[1], list3[2]]

    def add(self, index, value):
        self.column[index] = value

    def check_eq(self):
        found = [False] * 10
        for i in self.column:
            if i == "_":
                return False
            for k in range(1, 11):
                if i == k:
                    if not found[k]:
                        found[k] = True
                        break
                    else:
                        return False
        for k in range(len(found)):
            if not k and k != 0:
                return False
        return True

    def __str__(self):
        column(self.column)
        return " "


class sudoku_row():
    def __init__(self, list1, list2, list3):
        self.row = [list1[0], list1[1], list1[2], list2[0], list2[1], list2[2], list3[0], list3[1], list3[2]]

    def add(self, index, value):
        self.row[index] = value

    def check_eq(self):

        found = [False] * 10
        for i in self.row:
            if i == "_":
                return False
            for k in range(1, 11):
                if i == k:
                    if not found[k]:
                        found[k] = True
                    else:
                        return False
        for k in range(len(found)):
            if not found[k] and k != 0:
                return False
        return True

    def __str__(self):
        row(self.row[0:3])
        row(self.row[3:6])
        row(self.row[6:9])
        return ""


class sudoku:
    def __init__(self):
        TL = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        ML = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        BL = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        TM = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        M = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        BM = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        TR = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        MR = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        BR = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        self.TopLeft = sudoku_box(TL)
        self.MidLeft = sudoku_box(ML)
        self.BottomLeft = sudoku_box(BL)
        self.TopMid = sudoku_box(TM)
        self.Mid = sudoku_box(M)
        self.BottomMid = sudoku_box(BM)
        self.TopRight = sudoku_box(TR)
        self.MidRight = sudoku_box(MR)
        self.BottomRight = sudoku_box(BR)
        self.row1 = sudoku_row(self.TopLeft.disp_row(0), self.TopMid.disp_row(0), self.TopRight.disp_row(0))
        self.row2 = sudoku_row(self.TopLeft.disp_row(1), self.TopMid.disp_row(1), self.TopRight.disp_row(1))
        self.row3 = sudoku_row(self.TopLeft.disp_row(2), self.TopMid.disp_row(2), self.TopRight.disp_row(2))
        self.row4 = sudoku_row(self.MidLeft.disp_row(0), self.Mid.disp_row(0), self.MidRight.disp_row(0))
        self.row5 = sudoku_row(self.MidLeft.disp_row(1), self.Mid.disp_row(1), self.MidRight.disp_row(1))
        self.row6 = sudoku_row(self.MidLeft.disp_row(2), self.Mid.disp_row(2), self.MidRight.disp_row(2))
        self.row7 = sudoku_row(self.BottomLeft.disp_row(0), self.BottomMid.disp_row(0), self.BottomRight.disp_row(0))
        self.row8 = sudoku_row(self.BottomLeft.disp_row(1), self.BottomMid.disp_row(1), self.BottomRight.disp_row(1))
        self.row9 = sudoku_row(self.BottomLeft.disp_row(2), self.BottomMid.disp_row(2), self.BottomRight.disp_row(2))
        self.col1 = sudoku_column(self.TopLeft.disp_column(0), self.MidLeft.disp_column(0),
                                  self.BottomLeft.disp_column(0))
        self.col2 = sudoku_column(self.TopLeft.disp_column(1), self.MidLeft.disp_column(1),
                                  self.BottomLeft.disp_column(1))
        self.col3 = sudoku_column(self.TopLeft.disp_column(2), self.MidLeft.disp_column(2),
                                  self.BottomLeft.disp_column(2))
        self.col4 = sudoku_column(self.TopMid.disp_column(0), self.Mid.disp_column(0), self.BottomMid.disp_column(0))
        self.col5 = sudoku_column(self.TopMid.disp_column(1), self.Mid.disp_column(1), self.BottomMid.disp_column(1))
        self.col6 = sudoku_column(self.TopMid.disp_column(2), self.Mid.disp_column(2), self.BottomMid.disp_column(2))
        self.col7 = sudoku_column(self.TopRight.disp_column(0), self.MidRight.disp_column(0),
                                  self.BottomRight.disp_column(0))
        self.col8 = sudoku_column(self.TopRight.disp_column(1), self.MidRight.disp_column(1),
                                  self.BottomRight.disp_column(1))
        self.col9 = sudoku_column(self.TopRight.disp_column(2), self.MidRight.disp_column(2),
                                  self.BottomRight.disp_column(2))

    def __str__(self):
        i = 0
        while i < 3:
            tops()
            i += 1
        print()
        print(self.row1)
        print(self.row2)
        print(self.row3)
        i = 0
        while i < 3:
            tops()
            i += 1
        print()
        print(self.row4)
        print(self.row5)
        print(self.row6)
        i = 0
        while i < 3:
            tops()
            i += 1
        print()
        print(self.row7)
        print(self.row8)
        print(self.row9)
        return ""

    def update_region(self, region_let, cell_num, value, flag=None):
        regiondict = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9}
        region = regiondict[region_let]
        index = cell_num - 1
        if region < 4:
            if region == 1:
                self.TopLeft.add(index, value)
                if index < 3:
                    updates(self.row1, self.col1, self.col2, self.col3, index, value, 0, 1, 2, 0)
                elif index < 6:
                    updates(self.row2, self.col1, self.col2, self.col3, index, value, 0, 1, 2, 1)
                else:
                    updates(self.row3, self.col1, self.col2, self.col3, index, value, 0, 1, 2, 2)
            elif region == 2:
                self.TopMid.add(index, value)
                if index < 3:
                    updates(self.row1, self.col4, self.col5, self.col6, index, value, 3, 4, 5, 0)
                elif index < 6:
                    updates(self.row2, self.col4, self.col5, self.col6, index, value, 3, 4, 5, 1)
                else:
                    updates(self.row3, self.col4, self.col5, self.col6, index, value, 3, 4, 5, 2)
            elif region == 3:
                self.TopRight.add(index, value)
                if index < 3:
                    updates(self.row1, self.col7, self.col8, self.col9, index, value, 6, 7, 8, 0)
                elif index < 6:
                    updates(self.row2, self.col7, self.col8, self.col9, index, value, 6, 7, 8, 1)
                else:
                    updates(self.row3, self.col7, self.col8, self.col9, index, value, 6, 7, 8, 2)
        elif region < 7:
            if region == 4:
                self.MidLeft.add(index, value)
                if index < 3:
                    updates(self.row4, self.col1, self.col2, self.col3, index, value, 0, 1, 2, 3)
                elif index < 6:
                    updates(self.row5, self.col1, self.col2, self.col3, index, value, 0, 1, 2, 4)
                else:
                    updates(self.row6, self.col1, self.col2, self.col3, index, value, 0, 1, 2, 5)

            elif region == 5:
                self.Mid.add(index, value)
                if index < 3:
                    updates(self.row4, self.col4, self.col5, self.col6, index, value, 3, 4, 5, 3)
                elif index < 6:
                    updates(self.row5, self.col4, self.col5, self.col6, index, value, 3, 4, 5, 4)
                else:
                    updates(self.row6, self.col4, self.col5, self.col6, index, value, 3, 4, 5, 5)
            elif region == 6:
                self.MidRight.add(index, value)
                if index < 3:
                    updates(self.row4, self.col7, self.col8, self.col9, index, value, 6, 7, 8, 3)
                elif index < 6:
                    updates(self.row5, self.col7, self.col8, self.col9, index, value, 6, 7, 8, 4)
                else:
                    updates(self.row6, self.col7, self.col8, self.col9, index, value, 6, 7, 8, 5)
        else:
            if region == 7:
                self.BottomLeft.add(index, value)
                if index < 3:
                    updates(self.row7, self.col1, self.col2, self.col3, index, value, 0, 1, 2, 6)
                elif index < 6:
                    updates(self.row8, self.col1, self.col2, self.col3, index, value, 0, 1, 2, 7)
                else:
                    updates(self.row9, self.col1, self.col2, self.col3, index, value, 0, 1, 2, 8)
            elif region == 8:
                self.BottomMid.add(index, value)
                if index < 3:
                    updates(self.row7, self.col4, self.col5, self.col6, index, value, 3, 4, 5, 6)
                elif index < 6:
                    updates(self.row8, self.col4, self.col5, self.col6, index, value, 3, 4, 5, 7)
                else:
                    updates(self.row9, self.col4, self.col5, self.col6, index, value, 3, 4, 5, 8)
            elif region == 9:
                self.BottomRight.add(index, value)
                if index < 3:
                    updates(self.row7, self.col7, self.col8, self.col9, index, value, 6, 7, 8, 6)
                elif index < 6:
                    updates(self.row8, self.col7, self.col8, self.col9, index, value, 6, 7, 8, 7)
                else:
                    updates(self.row9, self.col7, self.col8, self.col9, index, value, 6, 7, 8, 8)

        if flag:
            print(self)

    def check(self):

        if (
                self.TopLeft.check_eq()
                and self.MidLeft.check_eq()
                and self.BottomLeft.check_eq()
                and self.TopMid.check_eq()
                and self.Mid.check_eq()
                and self.BottomMid.check_eq()
                and self.TopRight.check_eq()
                and self.MidRight.check_eq()
                and self.BottomRight.check_eq()
                and self.row1.check_eq()
                and self.row2.check_eq()
                and self.row3.check_eq()
                and self.row4.check_eq()
                and self.row5.check_eq()
                and self.row6.check_eq()
                and self.row7.check_eq()
                and self.row8.check_eq()
                and self.row9.check_eq()
                and self.col1.check_eq()
                and self.col2.check_eq()
                and self.col3.check_eq()
                and self.col4.check_eq()
                and self.col5.check_eq()
                and self.col6.check_eq()
                and self.col7.check_eq()
                and self.col8.check_eq()
                and self.col9.check_eq()
        ):
            return True
        return False

def main(Game1):
    Solved = False
    Regions = sudoku()
    for i in "ABCDEFGHI":
        Regions.update_region(i, 5, i)

    Cells = sudoku_box([1, 2, 3, 4, 5, 6, 7, 8, 9])
    while not Solved:
        print("MENU")
        print("1 = Show Region Names")
        print("2 = Show Cell Index Numbers")
        print("3 = Update a Cell")
        print("4 = Check if Box Correct")
        print("5 = Check if Column Correct")
        print("6 = Check if Row Correct")
        print("7 - Help")
        selection = input("Selection: ")
        if selection == "3":
            print(Game1)
            UPDATES = True
            while UPDATES:
                region, cell, value = input("Enter which cell to update, Region Cell Value eg: A19.  Enter "
                                            "000 to exit.")
                if region == "0" and cell == "0" and value == "0":
                    break
                if region in "ABCDEFGHI" and int(cell) in range(1, 10) and int(value) in range(1, 10):
                    Game1.update_region(region, int(cell), int(value), flag=True)
                else:
                    print("invalid position array.  Would you like to see the region and cell keys?")
                    regioncell = input()
                    if regioncell[0].lower == "y":
                        print(Regions)
                        print(Cells)
                if Game1.check():
                    Solved = True
                    UPDATES = False

        elif selection == "1":
            print(Regions)
        elif selection == "2":
            print(Cells)
        elif selection == "4":
            box2check = input("Which region would you like check?")
            region_dict = {"A": Game1.TopLeft.check_eq(), "B": Game1.TopMid.check_eq(), "C": Game1.TopRight.check_eq(),
                           "D": Game1.MidLeft.check_eq(), "E": Game1.Mid.check_eq(), "F": Game1.MidRight.check_eq(),
                           "G": Game1.BottomLeft.check_eq(), "H": Game1.BottomMid.check_eq(),
                           "I": Game1.BottomRight.check_eq()}
            if region_dict[box2check]:
                print("Region " + box2check + " looks good!")
            else:
                print("Region " + box2check + " is a little off!")
        elif selection == "5":
            column2check = input("Which column would you like check.  Choose a column, as if numbered left to right.")
            column_dict = {"1": Game1.col1.check_eq(), "2": Game1.col2.check_eq(), "3": Game1.col3.check_eq(),
                           "4": Game1.col4.check_eq(), "5": Game1.col5.check_eq(), "6": Game1.col6.check_eq(),
                           "7": Game1.col7.check_eq(), "8": Game1.col8.check_eq(), "9": Game1.col9.check_eq()}
            if column_dict[column2check]:
                print("Column " + column2check + " looks good!")
            else:
                print("Column " + column2check + " is a little off!")
        elif selection == "6":
            row2check = input("Which row would you like check.  Choose a row as if numbered top to bottom.")
            row_dict = {"1": Game1.row1.check_eq(), "2": Game1.row2.check_eq(), "3": Game1.row3.check_eq(),
                        "4": Game1.row4.check_eq(), "5": Game1.row5.check_eq(), "6": Game1.row6.check_eq(),
                        "7": Game1.row7.check_eq(), "8": Game1.row8.check_eq(), "9": Game1.row9.check_eq()}
            if row_dict[row2check]:
                print("Row " + row2check + " looks good!")
            else:
                print("Row " + row2check + " is a little off!")
        elif selection == "Exit":
            Solved = True


GAME = New_Game()
print("MENU")
print("1 = New Game\n2 = Directions\n3 = Credits")
GAME_CHOICE = input(">>>")
if GAME_CHOICE == "1":
    main(GAME)
elif GAME_CHOICE == "2":
    print("To play, enter the two digit coordinates and the value.  For example, to put a 5 in the "
          "center cell of the center square, play 'A55")
elif GAME_CHOICE == "3":
    print("Copyright 2018; Vanessa Nedrow.\n Created using PyCharm for Mac")

    # print(Game1.check())

# print(Game1.row1.check_eq())

