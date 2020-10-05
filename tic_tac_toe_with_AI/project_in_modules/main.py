import game

def play_again():
    print()
    play = ask_user_to_play()
    while play != 'n' and play != 'y':
        print()
        print("Choose 'y' to play or 'n' to exit")
        print()
        play = ask_user_to_play()
    if play == 'y':
        return True
    return False

def ask_user_to_play():
    return input("Play again? (y/n): ")

def start():
    new_game = game.Game()
    if not new_game.start_game():
        return
    while play_again():
        print()
        new_game = game.Game()
        if not new_game.start_game():
            return

start()
