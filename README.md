# The Hangman Game
Introduction

Welcome to the Hangman Game! This game allows you to enjoy the classic game of Hangman with varying levels of difficulty, different sets of secret words, and a Hall of Fame to keep track of the highest scorers.

Setup

Prerequisites:

Python 3.x installed on your system.
Required Python packages: random, pandas, tabulate, sqlite3, os.
Install Required Packages:
Run the following command to install the required packages:
Copy code
pip install pandas tabulate
Database Setup:
The game uses an SQLite database to store Hall of Fame records. The database file hangman_hall_of_fame.db will be created automatically when you run the game for the first time.


How to Play
Run the Game:
Execute the Python script to start the game:
Copy code
python hangman.py

Enter Your Name:
The game will prompt you to enter your name. This will be used to track your score in the Hall of Fame.

Select an Option:
You will be presented with a menu to choose the game level or view additional information. Enter the corresponding number to make your choice.

Game Levels

Easy Level:
Choose a set of words (Animals, Shapes, Places).
You have 8 lives to guess the word.

Moderate Level:
Choose a set of words (Animals, Shapes, Places).
You have 6 lives to guess the word.

Hard Level:
The set of words and the word itself are randomly chosen.
You have 6 lives to guess the word.

Hall of Fame
The Hall of Fame displays the highest scorers for each level. The score is determined by the number of remaining lives when the game is won. The highest score for each level is stored in the SQLite database.

About the Game
This section provides detailed information about the game rules for each level.

Database
The SQLite database hangman_hall_of_fame.db is used to store the highest scorers. The table structure is as follows:

id: Primary key (integer)

level: The game level (text)

winner_name: The name of the winner (text)

remaining_lives: The number of remaining lives when the game was won (integer)

The database is created and updated automatically by the game.
