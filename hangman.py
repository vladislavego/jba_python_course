from random import choice

correct_symbols = set("qwertyuiopasdfghjklzxcvbnm")
word_list = 'python', 'java', 'kotlin', 'javascript'
print("H A N G M A N")
while True:
    play_or_exit = input('Type "play" to play the game, "exit" to quit:').strip()
    if play_or_exit == "exit":
        break
    elif play_or_exit != "play":
        continue
    guessed_word = choice(word_list)
    guessed_word_length = len(guessed_word)
    current_word = "-" * guessed_word_length
    attempts = 8
    used_letters = set()
    while True:
        if attempts == 0:
            print("You are hanged!")
            break
        print(f"\n{current_word}")
        letter = input("Input a letter:")
        if len(letter) != 1:
            print("You should input a single letter")
            continue
        if letter not in correct_symbols:
            print("It is not an ASCII lowercase letter")
            continue
        if letter in used_letters:
            print("You already typed this letter")
            continue
        if letter not in guessed_word:
            print("No such letter in the word")
            attempts -= 1
        for i in range(guessed_word_length):
            if guessed_word[i] == letter:
                current_word = current_word[:i] + letter + current_word[i+1:]
        if '-' not in current_word:
            print("You guessed the word!")
            print("You survived!")
            break
        used_letters.add(letter)

