import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
# Global variables
TIMER_DURATION = 30  # Duration of the timer in seconds
# Replace the file paths with the paths to your PNG images
HANGMAN_PICS = [
    "add path of image 1 here",
    "add path of image 2 here",
    "add path of image 3 here",
    "add path of image 4 here",
    "add path of image 5 here",
    "add path of image 6 here",
    "add path of image 7 here"
]

countries = [
    ("usa", "The land of the free"),
    ("uk", "Home of Big Ben"),
    ("france", "Eiffel Tower stands tall here"),
    ("china", "The Great Wall"),
    ("brazil", "Famous for the Amazon Rainforest"),
    ("russia", "Largest country by land area"),
    ("india", "Taj Mahal resides here"),
    ("australia", "Known as the Land Down Under"),
    ("germany", "Famous for its beer and sausages"),
    ("japan", "Land of the rising sun"),
    ("canada", "Second largest country in the world"),
    ("italy", "Home to the Colosseum"),
    ("spain", "Famous for its siestas and fiestas"),
    ("mexico", "Birthplace of tacos and tequila"),
    ("argentina", "Famous for Tango and Maradona"),
    ("egypt", "Home to the Pyramids and Sphinx"),
    ("southafrica", "Known for its diverse wildlife"),
    ("southkorea", "Home of K-pop and kimchi"),
    ("greece", "Birthplace of democracy and the Olympics"),
    ("thailand", "Land of smiles and tropical beaches")
]

class InstructionPage:
    def _init_(self, master, callback):
        self.master = master
        self.master.title("Instructions")
        self.master.configure(bg="#F0F0F0")  # Set background color

        # Create a frame to hold the content
        self.content_frame = tk.Frame(self.master, bg="#F0F0F0")
        self.content_frame.pack(padx=20, pady=20)

        # Create a label for the title
        title_label = tk.Label(self.content_frame, text="Hangman Game Instructions", bg="#F0F0F0",
                               fg="#8B0000", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Create a label for the instructions text
        instructions_text = "Welcome to Hangman Game!\n\n" \
                            "The objective of the game is to guess the secret word by suggesting letters.\n" \
                            "You can make up to 6 incorrect guesses before the game ends.\n\n" \
                            "the game also has a timer of 30 seconds.\n\n"\
                            "on clicking restart, you wont be having timer rule but the word would change.\n"\
                            "Click 'Start' to begin the game.\n" \
                            "Good luck!"

        instructions_label = tk.Label(self.content_frame, text=instructions_text, bg="#F0F0F0",
                                      fg="#333333", font=("Arial", 12), justify="left")
        instructions_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Create a button to start the game
        start_button = ttk.Button(self.content_frame, text="Start", command=callback, style="Start.TButton")
        start_button.grid(row=2, column=0, columnspan=2)


class StartPage:
    def _init_(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.configure(bg="#E6E6FA")  # Set lavender background color

        self.label = tk.Label(self.master, text="Enter your name:", bg="#E6E6FA", fg="#8B0000",
                              font=("Arial", 14))
        self.label.pack()

        self.name_entry = tk.Entry(self.master, font=("Arial", 14))
        self.name_entry.pack()

        self.start_button = tk.Button(self.master, text="Start", command=self.start_game, bg="#DC143C", fg="#E6E6FA",
                                       font=("Arial", 14))  # Set button color
        self.start_button.pack()

    def start_game(self):
        name = self.name_entry.get()
        if name.strip() == "":
            messagebox.showerror("Error", "Please enter your name.")
        else:
            instruction_window = tk.Toplevel(self.master)
            instructions = InstructionPage(instruction_window, lambda: self.start_actual_game(name))
            self.master.withdraw()

    def start_actual_game(self, name):
        game_window = tk.Toplevel(self.master)
        hangman_game = HangmanGame(game_window, name)
        self.master.withdraw()


class HangmanGame:
    def _init_(self, master, name):
        self.master = master
        self.master.title("Hangman Game")
        self.master.configure(bg="#E6E6FA")  # Set lavender background color

        self.canvas = tk.Canvas(self.master, width=400, height=500, bg="#E6E6FA")  # Set lavender background color
        self.canvas.pack()

        self.name = name
        # Add a label for the timer display
        self.timer_label = tk.Label(self.master, text="", bg="#E6E6FA", fg="#8B0000", font=("Arial", 14))
        self.timer_label.pack()

        # Initialize the timer
        self.timer_remaining = TIMER_DURATION
        self.update_timer()
        

        self.missed_letters_label = tk.Label(self.master, text="Missed Letters:", bg="#E6E6FA", fg="#8B0000",
                                             font=("Arial", 14))
        self.missed_letters_label.pack()

        self.missed_letters_var = tk.StringVar()
        self.missed_letters_display = tk.Label(self.master, textvariable=self.missed_letters_var, bg="#E6E6FA",
                                               fg="#8B0000", font=("Arial", 14))
        self.missed_letters_display.pack()

        self.secret_word_label = tk.Label(self.master, text="Secret Word:", bg="#E6E6FA", fg="#8B0000",
                                          font=("Arial", 14))
        self.secret_word_label.pack()

        self.secret_word_var = tk.StringVar()
        self.secret_word_display = tk.Label(self.master, textvariable=self.secret_word_var, bg="#E6E6FA", fg="#8B0000",
                                            font=("Arial", 14))
        self.secret_word_display.pack()

        self.hint_label = tk.Label(self.master, text="Hint:", bg="#E6E6FA", fg="#8B0000", font=("Arial", 14))
        self.hint_label.pack()

        self.hint_var = tk.StringVar()
        self.hint_display = tk.Label(self.master, textvariable=self.hint_var, bg="#E6E6FA", fg="#8B0000",
                                     font=("Arial", 14))
        self.hint_display.pack()

        self.guess_label = tk.Label(self.master, text="Enter a Letter:", bg="#E6E6FA", fg="#8B0000", font=("Arial", 14))
        self.guess_label.pack()

        self.guess_entry = tk.Entry(self.master, font=("Arial", 14))
        self.guess_entry.pack()

        self.guess_button = tk.Button(self.master, text="Guess", command=self.make_guess, bg="#DC143C", fg="#E6E6FA",
                                      font=("Arial", 14))  # Set button color
        self.guess_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_game, bg="#DC143C", fg="#E6E6FA",
                                      font=("Arial", 14))  # Set button color
        self.reset_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        


        self.total_attempts = 0
        self.correct_attempts = 0
        self.incorrect_attempts = 0
        self.initialize_game()
    def update_timer(self):
        # Update the timer label with the remaining time
        self.timer_label.config(text=f"Time left: {self.timer_remaining} seconds")

        # Decrement the remaining time
        self.timer_remaining -= 1

        # Check if the timer has reached 0
        if self.timer_remaining < 0:
            self.timer_label.config(text="Time's up!")
            self.game_over(time_up=True)

        else:
            # Schedule the update_timer function to run after 1 second
            self.master.after(1000, self.update_timer)
        
        
    def game_over(self, time_up=False):
        if time_up:
            
            # Display the result box indicating time's up
            messagebox.showinfo("Time's Up!",f"You ran out of time!The secret word is '{self.secret_word}'.\n\nTotal Attempts: {self.total_attempts}\nCorrect Attempts: {self.correct_attempts}\nIncorrect Attempts: {self.incorrect_attempts}")
        else:
            # Display the result box indicating successful guess
            messagebox.showinfo("Congratulations",
                            f"{self.name}, you guessed it!\nThe secret word is '{self.secret_word}'. You win!\n\nTotal Attempts: {self.total_attempts}\nCorrect Attempts: {self.correct_attempts}\nIncorrect Attempts: {self.incorrect_attempts}")

        


    def animate_correct_guess(self):
        self.secret_word_display.config(fg="green")  # Change the color of the correct letters
        # Add a short delay to the animation
        self.master.update()
        time.sleep(0.5)  # Adjust the delay time as needed

        # Reset the color back to the original color
        self.secret_word_display.config(fg="#8B0000")  # Original color of the letters

    def animate_hangman(self, missed):
        for i in range(missed + 1):
            img_path = HANGMAN_PICS[i]
            img = Image.open(img_path)
            img = img.resize((200, 200), Image.ANTIALIAS)  # Resize the image if needed
            photo = ImageTk.PhotoImage(img)
            self.canvas.image = photo  # Keep a reference to prevent garbage collection
            self.canvas.create_image(200, 200, image=photo, anchor=tk.CENTER)

            # Add a short delay between each frame of the animation
            self.master.update()
            time.sleep(0.5)  # Adjust the delay time as needed
        self.canvas.delete("hangman")

    def initialize_game(self):
        self.missed_letters = ''
        self.correct_letters = ''
        self.secret_word, self.hint = getRandomCountry(countries)
        self.update_display()
        

    def update_display(self):
        self.missed_letters_var.set(self.missed_letters)

        blanks = ''
        for letter in self.secret_word:
            if letter in self.correct_letters:
                blanks += letter + ' '
            else:
                blanks += '_ '
        self.secret_word_var.set(blanks)

        self.hint_var.set(self.hint)

        self.draw_hangman(len(self.missed_letters))
        if self.check_win():
            self.game_over(time_up=False)

    def make_guess(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        self.total_attempts += 1

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Invalid Guess", "Please enter a single letter.")
            return

        if guess in self.correct_letters or guess in self.missed_letters:
            messagebox.showwarning("Duplicate Guess", "You have already guessed that letter. Choose again.")
            return

        if guess in self.secret_word:
            self.correct_letters += guess
            self.correct_attempts += 1
            self.animate_correct_guess()
            self.update_display()  # Update display after correct guess
            if self.check_win():
                messagebox.showinfo("Congratulations",
                                    f"{self.name}, you guessed it!\nThe secret word is '{self.secret_word}'. You win!\n\nTotal Attempts: {self.total_attempts}\nCorrect Attempts: {self.correct_attempts}\nIncorrect Attempts: {self.incorrect_attempts}")
                self.initialize_game()
        else:
            self.missed_letters += guess
            self.incorrect_attempts += 1
            if len(self.missed_letters) == len(HANGMAN_PICS) - 1:
                self.update_display()
                messagebox.showinfo("Game Over",
                                    f"{self.name}, you have run out of guesses!\nAfter {len(self.missed_letters)} missed guesses and {len(self.correct_letters)} correct guesses, the word was '{self.secret_word}'.\n\nTotal Attempts: {self.total_attempts}\nCorrect Attempts: {self.correct_attempts}\nIncorrect Attempts: {self.incorrect_attempts}")
                self.initialize_game()
            else:
                self.animate_hangman(len(self.missed_letters))
                self.update_display()

    def check_win(self):
        for letter in self.secret_word:
            if letter not in self.correct_letters:
                return False
        return True

    def draw_hangman(self, missed):
        self.canvas.delete("hangman")

        # Load the image based on the number of missed guesses
        img_path = HANGMAN_PICS[missed]
        img = Image.open(img_path)
        img = img.resize((200, 200), Image.ANTIALIAS)  # Resize the image if needed
        photo = ImageTk.PhotoImage(img)

        # Create a label to display the image
        self.canvas.image = photo  # Keep a reference to prevent garbage collection
        self.canvas.create_image(200, 200, image=photo, anchor=tk.CENTER, tags="hangman")

    def reset_game(self):
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset the game?"):
            self.total_attempts = 0
            self.correct_attempts = 0
            self.incorrect_attempts = 0
            self.initialize_game()
            
            
    
    



def getRandomCountry(countriesList):
    return random.choice(countriesList)


def main():
    root = tk.Tk()
    start_page = StartPage(root)
    root.mainloop()


if _name_ == "_main_":
    main()
