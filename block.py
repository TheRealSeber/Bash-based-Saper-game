class Block:
    def __init__(self):
        self.game_in_progress = True
        self.is_bomb = False
        self.neighbour_bombs = 0
        self.was_checked = False
        self.player_guess = (
            0  # player_guess = 0, means no guess, 1 means "clicked", 2 "marked as bomb"
        )

    def __str__(self):
        if self.player_guess == 0 and self.game_in_progress:
            return chr(9608)  # white square
        elif self.player_guess == 1 and not self.is_bomb:
            return f"{self.neighbour_bombs}"
        elif self.player_guess == 2 and self.game_in_progress:
            return "\033[0;36m@\033[0m"  # "cyan_color '@' default_color"
            # return "\U0001F3F3"

        # if's when game is over.
        elif (
            self.player_guess == 2 and not self.game_in_progress
        ):  # checks whether marking was correct
            if self.is_bomb:
                return "\033[0;92m@\033[0m"  # "color_green '@' default_color"
            return "\033[0;91m@\033[0m"  # "color_red '@' default_color"
        elif self.is_bomb and self.player_guess == 1 and not self.game_in_progress:
            return "\033[0;91m*\033[0m"  # "color_red '*' default_color"
        elif self.is_bomb and not self.game_in_progress:
            return "\033[0;92m*\033[0m"  # "color_green '*' default_color"
        return f"{self.neighbour_bombs}"
