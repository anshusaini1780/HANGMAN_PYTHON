import random

HANGMAN_PICS = ['''
    +---+
         |
         |
         |
        ===''', '''
    +---+
    O   |
        |
        |
       ===''', '''
    +---+
    O   |
    |   |
        |
       ===''', '''
    +---+
    O   |
   /|   |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
   /    |
       ===''', '''
    +---+
    O   |
   /|\  |
   / \  |
       ===''']

# Define colors
COLORS = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

countries = [
    ("usa", "The land of the free"),
    ("uk", "Home of Big Ben"),
    ("france", "Eiffel Tower stands tall here"),
    ("china", "The Great Wall"),
    ("brazil", "Famous for the Amazon Rainforest"),
    ("russia", "Largest country by land area"),
    ("india", "Taj Mahal resides here"),
    ("australia", "Known as the Land Down Under")
]

def getRandomCountry(countriesList):
    """
    Returns a random country tuple from the passed list of country tuples.
    """
    return random.choice(countriesList)

def displayBoard(missedLetters, correctLetters, secretWord):
    print(COLORS['HEADER'] + HANGMAN_PICS[len(missedLetters)] + COLORS['ENDC'])

    print()
    print(COLORS['OKBLUE'] + 'Missed letters:' + COLORS['ENDC'], end=' ')
    for letter in missedLetters:
        print(COLORS['FAIL'] + letter + COLORS['ENDC'], end=' ')

    print()
    blanks = '_' * len(secretWord)
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    # Display the secret word with spaces between the letters:
    for letter in blanks:
        print(COLORS['OKGREEN'] + letter + COLORS['ENDC'], end =' ')
    print()

def getGuess(alreadyGuessed):
    """
    Returns the letter the player entered.
    Ensures the player enters a single letter and nothing else.
    """
    while True:
        print(COLORS['WARNING'] + 'Please guess a letter.' + COLORS['ENDC'])
        guess = input()
        guess = guess.lower()  # Convert to lowercase
        if len(guess) != 1:
            print(COLORS['FAIL'] + 'Only a single letter is allowed.' + COLORS['ENDC'])
        elif guess in alreadyGuessed:
            print(COLORS['FAIL'] + 'You have already guessed that letter. Choose again.' + COLORS['ENDC'])
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print(COLORS['FAIL'] + 'Please enter a letter from the alphabet.' + COLORS['ENDC'])
        else:
            return guess

def playAgain():
    """
    Returns True if the player wants to play again, False otherwise.
    """
    print(COLORS['OKBLUE'] + 'Would you like to play again? (y)es or (n)o' + COLORS['ENDC'])
    return input().lower().startswith('y')

print(COLORS['BOLD'] + '|H_A_N_G_M_A_N|' + COLORS['ENDC'])
missedLetters = ''
correctLetters = ''
secretWord, hint = getRandomCountry(countries)
gameIsDone = False

# Now for the game itself:
while True:
    displayBoard(missedLetters, correctLetters, secretWord)
    print(COLORS['OKBLUE'] + 'Hint: ' + hint + COLORS['ENDC'])
    # Let the player enter a letter:
    guess = getGuess(missedLetters + correctLetters)

    if guess in secretWord:  
        correctLetters = correctLetters + guess
        # Check to see if the player has won:
        foundAllLetters = True
        for letter in secretWord:
            if letter not in correctLetters:  
                foundAllLetters = False
                break
        if foundAllLetters:
            print(COLORS['OKGREEN'] + 'You guessed it!' + COLORS['ENDC'])
            print('The secret word is "' + secretWord + '"! ' + COLORS['OKGREEN'] + 'You win!' + COLORS['ENDC'])
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess

        # Check if the player has guessed too many times and lost.
        if len(missedLetters) == len(HANGMAN_PICS) - 1:
            displayBoard(missedLetters, correctLetters, secretWord)
            print(COLORS['FAIL'] + 'You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"' + COLORS['ENDC'])
            gameIsDone = True
    # If the game is done, ask the player to try again.
    if gameIsDone:
        if playAgain():
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False
            secretWord, hint = getRandomCountry(countries)
        else:
            break
