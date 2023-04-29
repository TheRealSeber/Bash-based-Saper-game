import random
from block import Block


class SaperInit:
    def __init__(self, bombs_num, rows_num, columns_num):
        self.game_status = 1  # 0 - lost, 1 - on going, 2 - won,
        self.bombs_to_place = bombs_num
        self.columns = columns_num
        self.rows = rows_num
        self.plane = [[Block() for c in range(columns_num)] for r in range(rows_num)]
        self.column_names = [chr(ord("A") + i) for i in range(columns_num)]
        self.possible_neighbour_coordinates = [
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, 0),
            (1, -1),
        ]

    #  arbitraly placing the bombs on the plane
    def place_bombs(self):
        while self.bombs_to_place > 0:
            rows = random.randint(0, self.rows - 1)
            columns = random.randint(0, self.columns - 1)
            if not self.plane[rows][columns].is_bomb:
                self.plane[rows][columns].is_bomb = True
                self.bombs_to_place -= 1

    #  this function updates ammount of neighbours bombs
    #  for the block after placing the bombs on the plane
    def update_adjacent_bombs(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.plane[r][c].is_bomb:
                    pass
                else:
                    for crd in self.possible_neighbour_coordinates:
                        try:
                            if (
                                self.plane[r + crd[0]][c + crd[1]].is_bomb
                                and r + crd[0] != -1
                                and c + crd[1] != -1
                            ):
                                self.plane[r][c].neighbour_bombs += 1
                        except IndexError:
                            pass

    def print_plane(self):
        print(f"{'  |': >{len(str(self.rows))+2}}", *self.column_names)
        print(
            f"{'- X': >{len(str(self.rows))+2}}",
            "".join(["-" for i in range(self.columns * 2 - 1)]),
        )
        for r in range(self.rows):
            print(
                f"{r+1: >{len(str(self.rows))}} |",
                end=" ",
            )
            for c in range(self.columns):
                if self.game_status in [0, 2]:
                    self.plane[r][c].game_in_progress = False
                print(self.plane[r][c], end=" ")
            print()

    #  checks whether ammount of
    #  neighbour marked bombs is
    #  equal to real ammout of
    #  neighbour bombs of the block
    def check_neighbours(self, r, c):
        marked_bombs = 0
        for crd in self.possible_neighbour_coordinates:
            try:
                if (
                    self.plane[r + crd[0]][c + crd[1]].player_guess
                    == 2  # checks if it is marked as a bomb
                    and r + crd[0] != -1
                    and c + crd[1] != -1
                ):
                    marked_bombs += 1
            except IndexError:
                pass
        return self.plane[r][c].neighbour_bombs == marked_bombs

    #  shows neighbours under
    #  certain condition
    def show_neighbours(self, r, c):
        #  was_checked is used, to suppress
        #  the function from getting into
        #  infinit recurency
        self.plane[r][c].was_checked = True
        for crd in self.possible_neighbour_coordinates:
            try:
                if (
                    not self.plane[r + crd[0]][c + crd[1]].player_guess
                    == 2  # checks if its marked as bomb
                    and r + crd[0] != -1
                    and c + crd[1] != -1
                ):
                    self.plane[r + crd[0]][
                        c + crd[1]
                    ].player_guess = 1  # exposing neighbours
                    if not self.plane[r + crd[0]][
                        c + crd[1]
                    ].was_checked and self.check_neighbours(r + crd[0], c + crd[1]):
                        self.show_neighbours(r + crd[0], c + crd[1])
            except IndexError:
                pass

    def player_guess(self, r, c, action):
        if action == 1:  # click
            self.plane[r][c].player_guess = 1
            if self.plane[r][c].is_bomb:
                self.game_status = 0
            elif self.plane[r][c].neighbour_bombs == 0 or self.check_neighbours(r, c):
                self.show_neighbours(r, c)

        elif action == 2:  # mark as a bomb
            self.plane[r][c].player_guess = 2
        else:  # unmark the bomb
            if self.plane[r][c].player_guess == 2:
                self.plane[r][c].player_guess = 0

    #  there should be also one more condition whether the last guess was correct
    def check_if_ended(self):
        return (
            sum([1 for row in self.plane for block in row if block.player_guess != 0])
            == self.columns * self.rows
        )

    def start_game(self):
        while self.game_status == 1:
            if self.game_status == 1:
                try:
                    column_guess = ord(input("Choose column: ")[0].upper()) - 65
                    if column_guess > self.columns or column_guess < 0:
                        print("Wrong column!")
                        continue
                    row_guess = int(input("Choose row: "))
                    if row_guess > self.rows or row_guess < 1:
                        print("Wrong row!")
                        continue
                    action = input(
                        "What do you want to do?\n1. Click\n2. Mark as a bomb\n3. Unmark the bomb \nYour choice is to: "
                    )[0]
                    if action not in "123":
                        print("Wrong action chosen!")
                        continue
                except:
                    print("Wrong input!")
                    continue
                self.player_guess(row_guess - 1, column_guess, int(action))

            if self.check_if_ended():
                self.game_status = 2

            if self.game_status == 0:
                print("\nYou've Lost!\n")
            if self.game_status == 2:
                print("\nYov've Won!\n")
            self.print_plane()
