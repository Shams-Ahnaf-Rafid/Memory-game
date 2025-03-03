import tkinter as tk
from tkinter import messagebox
import random
import time

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")
        self.buttons = []
        self.first_click = None
        self.matches_found = 0
        self.can_click = True
        
        # Score tracking variables
        self.attempts = 0
        self.score = 0
        self.best_score = 0
        
        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)
        
        # Create score frame
        self.score_frame = tk.Frame(root)
        self.score_frame.pack(pady=5)
        
        # Score labels
        self.score_label = tk.Label(self.score_frame, text="Score: 0", font=("Arial", 12))
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.attempts_label = tk.Label(self.score_frame, text="Attempts: 0", font=("Arial", 12))
        self.attempts_label.pack(side=tk.LEFT, padx=10)
        
        self.best_score_label = tk.Label(self.score_frame, text="Best Score: 0", font=("Arial", 12))
        self.best_score_label.pack(side=tk.LEFT, padx=10)
        
        # Restart button
        self.restart_button = tk.Button(root, text="New Game", command=self.restart_game)
        self.restart_button.pack(pady=5)
        
        # Create numbers list (pairs of numbers from 1 to 8)
        self.numbers = [i for i in range(1, 9)] * 2
        self.setup_game()

    def setup_game(self):
        random.shuffle(self.numbers)
        
        # Create the grid of buttons
        for i in range(4):
            row = []
            for j in range(4):
                button = tk.Button(self.main_frame, text="", width=10, height=5,
                                 command=lambda x=i, y=j: self.button_click(x, y))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

    def update_score(self, matched=False):
        self.attempts += 1
        if matched:
            # Award points based on attempts (more points for fewer attempts)
            points = max(10, 50 - (self.attempts * 2))
            self.score += points
        
        # Update labels
        self.score_label.config(text=f"Score: {self.score}")
        self.attempts_label.config(text=f"Attempts: {self.attempts}")
        
        # Update best score if current score is higher
        if self.score > self.best_score:
            self.best_score = self.score
            self.best_score_label.config(text=f"Best Score: {self.best_score}")

    def button_click(self, i, j):
        if not self.can_click:
            return
        
        current_button = self.buttons[i][j]
        
        # Ignore if button is already matched or clicked
        if current_button["state"] == "disabled" or current_button["text"] != "":
            return
        
        # Show number
        current_button["text"] = self.numbers[i * 4 + j]
        
        # First click of the pair
        if self.first_click is None:
            self.first_click = (i, j)
            return
        
        # Second click of the pair
        first_i, first_j = self.first_click
        first_button = self.buttons[first_i][first_j]
        
        # Check if it's a match
        if self.numbers[first_i * 4 + first_j] == self.numbers[i * 4 + j]:
            # Match found
            first_button["state"] = "disabled"
            current_button["state"] = "disabled"
            self.matches_found += 1
            self.update_score(matched=True)
            
            # Check if game is complete
            if self.matches_found == 8:
                self.show_win_message()
        else:
            # No match - hide both buttons after a short delay
            self.can_click = False
            self.update_score(matched=False)
            self.root.after(1000, lambda: self.hide_buttons(first_i, first_j, i, j))
        
        self.first_click = None

    def hide_buttons(self, i1, j1, i2, j2):
        self.buttons[i1][j1]["text"] = ""
        self.buttons[i2][j2]["text"] = ""
        self.can_click = True

    def show_win_message(self):
        for row in self.buttons:
            for button in row:
                button["text"] = "★"
        
        message = f"Congratulations! You Won!\nFinal Score: {self.score}\nAttempts: {self.attempts}"
        messagebox.showinfo("Game Complete", message)

    def restart_game(self):
        # Clear all buttons
        for row in self.buttons:
            for button in row:
                button.destroy()
        self.buttons = []
        
        # Reset game variables
        self.first_click = None
        self.matches_found = 0
        self.can_click = True
        self.attempts = 0
        self.score = 0
        
        # Update labels
        self.score_label.config(text="Score: 0")
        self.attempts_label.config(text="Attempts: 0")
        
        # Setup new game
        self.numbers = [i for i in range(1, 9)] * 2
        self.setup_game()

def main():
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()