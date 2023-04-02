from saper import SaperInit


def main():

    print("Input ammount of bombs, rows and columns (Example: 5 10 10): ", end="")
    b, r, c = [int(z) for z in input().split()]
    saper_plane = SaperInit(b, r, c)
    saper_plane.place_bombs()
    saper_plane.update_adjacent_bombs()
    saper_plane.print_plane()
    saper_plane.start_game()


if __name__ == "__main__":
    main()
