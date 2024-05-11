import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time

# Replace the file paths with the paths to your PNG images
HANGMAN_PICS = [
    "Add path of image 1 here",
    "Add path of image 2 here",
    "Add path of image 3 here",
    "Add path of image 4 here",
    "Add path of image 5 here",
    "Add path of image 6 here",
    "Add path of image 7 here"
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
        self.guess_button.pack()

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_game, bg="#DC143C", fg="#E6E6FA",
                                      font=("Arial", 14))  # Set button color
        self.reset_button.pack()

        self.total_attempts = 0
        self.correct_attempts = 0
        self.incorrect_attempts = 0
        self.initialize_game()

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
        self.secret_word, self.hint =
