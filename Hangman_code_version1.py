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
    print()
    print(HANGMAN_PICS[len(missedLetters)])

    print()
    print('Missed letters: ', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')

    print()
    blanks = '_' * len(secretWord)
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    # Display the secret word with spaces between the letters:
    for letter in blanks:
        print(letter, end =' ')
    print()

def getGuess(alreadyGuessed):
    """
    Returns the letter the player entered.
    Ensures the player enters a single letter and nothing else.
    """
    while True:
        print('Please guess a letter.')
        guess = input()
        guess = guess.lower()  # Convert to lowercase
        if len(guess) != 1:
            print('Only a single letter is allowed.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a letter from the alphabet.')
        else:
            return guess

def playAgain():
    """
    Returns True if the player wants to play again, False otherwise.
    """
    print('Would you like to play again? (y)es or (n)o')
    return input().lower().startswith('y')

print('|H_A_N_G_M_A_N|')
missedLetters = ''
correctLetters = ''
secretWord, hint = getRandomCountry(countries)
gameIsDone = False

# Now for the game itself:
while True:
    displayBoard(missedLetters, correctLetters, secretWord)
    print('Hint: ' + hint)
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
            print('You guessed it!')
            print('The secret word is "' + secretWord + '"! You win!')
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess

        # Check if the player has guessed too many times and lost.
        if len(missedLetters) == len(HANGMAN_PICS) - 1:
            displayBoard(missedLetters, correctLetters, secretWord)
            print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
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
