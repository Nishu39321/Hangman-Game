import random
import pandas as pd
from tabulate import tabulate
import sqlite3
import os

# Different hangman stages
HANGMAN_PICS = [r'''
  +---+
      |
      |
      |
     ===''',r'''
  +---+
  O   |
      |
      |
     ===''', r'''
  +---+
  O   |
  |   |
      |
     ===''', r'''
  +---+
  O   |
 /|   |
      |
     ===''', r'''
  +---+
  O   |
 /|\  |
      |
     ===''',r'''
  +---+
  O   |
 /|\  |
 /    |
     ===''', r'''
  +---+
  O   |
 /|\  |
 / \  |
     ===''', r'''
  +---+
 [O   |
 /|\  |
 / \  |
     ===''', r'''
  +---+
 [O]  |
 /|\  |
 / \  |
     ===''']

# Word lists
animal = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad turkey turtle weasel whale wolf zebra'.split()
Shapes = 'square triangle rectangle circle ellipse rhombus trapezoid parallelogram pentagon hexagon octagon trapezium cylinder sphere cube cuboid prism pyramid decagon dodecagon heptagon kite cone rhomboid nonagon octahedron hexahedron'.split()
Place = 'india london paris baghdad istanbul riyadh america delhi kolkata moscow columbo chennai dubai islamabad karachi rome tokyo kyoto seoul myanmar sydney florida mumbai monaco bangkok amsterdam osaka beijing berlin mexico miami vienna athens chicago venice singapore mecca agra jaipur jerusalem munich brussels zurich dusseldorf sanghai dhaka cairo bangalore'.split()
main_items = 'animal Shapes Place'.split()

def getRandomWord(wordList): # function to choose a random word out of a list
    return random.choice(wordList)

def displayBoard(missedLetters, correctLetters, secretWord): # function to display current status of player
    print(HANGMAN_PICS[len(missedLetters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks:
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):    # function to check for a valid input
    while True:
        print('Guess a letter.')
        guess = input().lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def playAgain():  # function to ask user confirmation to exit the game
    print('Do you want to Exit? (yes or no)')
    return input().lower().startswith('n')

def add_or_update_winner(level, winner_name, remaining_lives):
    conn = sqlite3.connect('hangman_hall_of_fame.db')
    cursor = conn.cursor()

    # Check if there's already a winner for the given level
    cursor.execute('SELECT remaining_lives FROM hall_of_fame WHERE level = ?', (level,))
    row = cursor.fetchone()

    if row:
        # If a record exists, update only if the new score is higher
        if remaining_lives > row[0]:
            cursor.execute('''
            UPDATE hall_of_fame
            SET winner_name = ?, remaining_lives = ?
            WHERE level = ?
            ''', (winner_name, remaining_lives, level))
    else:
        # If no record exists, insert a new one
        cursor.execute('''
        INSERT INTO hall_of_fame (level, winner_name, remaining_lives)
        VALUES (?, ?, ?)
        ''', (level, winner_name, remaining_lives))

    conn.commit()
    conn.close()

def display_hall_of_fame():                           # displays the name of highest scorers by fetching data from db file
    conn = sqlite3.connect('hangman_hall_of_fame.db')
    cursor = conn.cursor()
    cursor.execute('SELECT level, winner_name, remaining_lives FROM hall_of_fame')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print(tabulate(rows, headers=["Level", "Winner name", "Remaining lives"], tablefmt="grid"))
    else:
        print("No winners yet.")

def main_game(secretWord, k, level):    # the most crucial part of game which keeps the game running by asking for user input and displaying the board again and again
    missedLetters = ''
    correctLetters = ''
    gameIsDone = False

    while True:
        displayBoard(missedLetters, correctLetters, secretWord)

        # Let the player enter a letter.
        guess = getGuess(missedLetters + correctLetters)

        if guess in secretWord:
            correctLetters = correctLetters + guess

            # Check if the player has won.
            foundAllLetters = True
            for i in range(len(secretWord)):
                if secretWord[i] not in correctLetters:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                print('Yes! The secret word is "' + secretWord + '"! You have won!')
                remaining_lives = len(HANGMAN_PICS) - k - len(missedLetters)
                add_or_update_winner(level, Name, remaining_lives)
                gameIsDone = True
        else:
            missedLetters = missedLetters + guess

            # Check if player has guessed too many times and lost.
            if len(missedLetters) == len(HANGMAN_PICS) - k:
                displayBoard(missedLetters, correctLetters, secretWord)
                print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
                gameIsDone = True

        # Ask the player if they want to play again (but only if the game is done).
        if gameIsDone:
            break

def menu_2():                # the second menu table to ask users to selct among the topic they want word from
    header = ["SELECT FROM THE FOLLOWING SETS OF SECRET WORDS", "", ""]
    game_options = ["Animals 1", "Shapes 2", "Places 3"]

    table_data = [
      header,
      game_options
    ]

    df = pd.DataFrame(table_data)

    max_length = max(len(cell) for row in table_data for cell in row)
    df = df.map(lambda x: x.ljust(max_length))

    table = tabulate(df, tablefmt="grid", showindex=False, headers=[])

    print(table)

def easy_level():
    print("You selected Easy level")
    menu_2()
    get_choice = int(input("Enter your choice for words (1-3):"))
    if get_choice == 1:
        secretWord = getRandomWord(animal)
    elif get_choice == 2:
        secretWord = getRandomWord(Shapes)
    else:
        secretWord = getRandomWord(Place)
    main_game(secretWord, 1, "Easy")

def moderate_level():
    print("You selected Moderate level")
    menu_2()
    get_choice = int(input("Enter your choice for words (1-3):"))
    if get_choice == 1:
        secretWord = getRandomWord(animal)
    elif get_choice == 2:
        secretWord = getRandomWord(Shapes)
    else:
        secretWord = getRandomWord(Place)
    main_game(secretWord, 3, "Moderate")

def hard_level():
    print("You selected Hard level")
    topic = getRandomWord(main_items)  # Get a random topic name
    if topic == 'animal':
        secretWord = getRandomWord(animal)
    elif topic == 'Shapes':
        secretWord = getRandomWord(Shapes)
    elif topic == 'Place':
        secretWord = getRandomWord(Place)
    main_game(secretWord, 3, "Hard")

def hall_of_fame():
    print("You selected Hall of fame")
    display_hall_of_fame()

def about_the_game():
    print("You selected About the game")
    print("---------------------------------")
    print("|       ABOUT THE GAME          |")
    print("---------------------------------")
    print("|Easy Level : the user will be  |")
    print("|given the chance to select the |")
    print("|list from which the random word|")
    print("|will be selected (Animal,Shape,|")
    print("|Place).This will make it easier|")
    print("| to guess the secret word. Also|")
    print("|the number of trials will be   |")
    print("|increased from 6 to 8.         |")
    print("---------------------------------")
    print("|Moderate Level : Similar to    |")
    print("|Easy, the user will be given   |")
    print("|the chance to select the set   |")
    print("|from which the random word will|")
    print("|be selected (Animal, Shapes,   |")
    print("|Place), but the number of trial|")
    print("|  will be reduced to 6.        |")
    print("---------------------------------")
    print("|Hard Level : The set of words  |")
    print("|as well as the word will be    |")
    print("|random. The user will have no  |")
    print("|clue on the secret word. And,  |")
    print("| the number of trials will     |")
    print("|       reamain at 6.           |")
    print("---------------------------------")

# Switch-like dictionary to map choices to functions
switch = {
    1: easy_level,
    2: moderate_level,
    3: hard_level,
    4: hall_of_fame,
    5: about_the_game
}

def handle_choice(choice):
    action = switch.get(choice, lambda: print("Invalid choice"))
    action()

# Main program
if __name__ == "__main__":
    print("Welcome to the game. Please enter your name.")
    Name = input()

    header = [f"Hi '{Name}'", "", ""]
    sub_header = ["Welcome to HANGMAN", "", ""]
    game_levels = ["Easy level 1", "Moderate level 2", "Hard level 3"]
    additional_info = ["Hall of fame 4", "About the game 5", ""]

    table_data = [
        header,
        sub_header,
        game_levels,
        additional_info
    ]

    df = pd.DataFrame(table_data)

    table = tabulate(df, tablefmt="grid", showindex=False, headers=[])

    # Create a connection to the SQLite database
    conn = sqlite3.connect('hangman_hall_of_fame.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create the hall_of_fame table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hall_of_fame (
        id INTEGER PRIMARY KEY,
        level TEXT NOT NULL,
        winner_name TEXT NOT NULL,
        remaining_lives INTEGER NOT NULL
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    while True:
        print(table)
        user_choice = int(input("Enter your choice (1-5): "))
        handle_choice(user_choice)
        if not playAgain():
            break
