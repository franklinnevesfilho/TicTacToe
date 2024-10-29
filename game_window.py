import tkinter as tk
from tkinter import messagebox
import game_logic as gl  # Import your game logic functions and variables here

def reset_buttons():
    global buttons
    for btn in buttons:
        btn.config(text="")

def player_choice(symbol):
    gl.set_player_move(symbol)
    gl.reset_game()
    reset_buttons()

    message_label.config(text=f"Playing as {symbol}")
    if symbol == "O":  # If player chooses "O", let AI make the first move
        ai_move()

def player_move(index):
    if gl.game_board[index] is None:
        gl.game_board[index] = gl.get_player_move()
        update_buttons()

        # Check for win or draw after player move
        if gl.check_win(gl.game_board) == -1:
            messagebox.showinfo("Game Over", "You win!")
            gl.reset_game()
            reset_buttons()
            update_buttons()
            return
        elif gl.check_draw(gl.game_board):
            messagebox.showinfo("Game Over", "It's a draw!")
            gl.reset_game()
            reset_buttons()
            update_buttons()
            return

        ai_move()

def ai_move():
    player = gl.get_player_move()
    ai_symbol = "O" if player == "X" else "X"

    # Step 1: Check for immediate player win and block it
    for move in gl.get_possible_moves(gl.game_board):
        temp_board = gl.make_move(move, gl.game_board, player)
        if gl.check_win(temp_board) == -1:  # If player won with this move, block it
            gl.game_board[move[0]] = ai_symbol
            update_buttons()
            if gl.check_win(gl.game_board) == 1:
                messagebox.showinfo("Game Over", "AI wins!")
                gl.reset_game()
                reset_buttons()
                update_buttons()
            elif gl.check_draw(gl.game_board):
                messagebox.showinfo("Game Over", "It's a draw!")
                gl.reset_game()
                reset_buttons()
                update_buttons()
            return

    # Step 2: Use minimax to find the best move if no immediate block is needed
    best_move = None
    best_score = gl.NEG_INF if player == "O" else gl.POS_INF
    for move in gl.get_possible_moves(gl.game_board):
        temp_board = gl.make_move(move, gl.game_board, ai_symbol)
        score = gl.minimax(temp_board, player == "X")
        if (player == "O" and score > best_score) or (player == "X" and score < best_score):
            best_score = score
            best_move = move

    if best_move:
        gl.game_board[best_move[0]] = ai_symbol
        update_buttons()
        if gl.check_win(gl.game_board) == 1:
            messagebox.showinfo("Game Over", "AI wins!")
            gl.reset_game()
            reset_buttons()
            update_buttons()
        elif gl.check_draw(gl.game_board):
            messagebox.showinfo("Game Over", "It's a draw!")
            gl.reset_game()
            reset_buttons()
            update_buttons()

def update_buttons():
    for i, button in enumerate(buttons):
        button.config(text=gl.game_board[i] if gl.game_board[i] else "")

# Reset button functionality
def reset_button():
    gl.reset_game()
    update_buttons()
    message_label.config(text="Choose X or O to start")

# Setup tkinter window
root = tk.Tk()
root.title("Tic Tac Toe")

# Message label for the current status
message_label = tk.Label(root, text="Choose X or O to start", font=("Arial", 14))
message_label.grid(row=0, column=0, columnspan=3)

# Buttons for choosing X or O
choose_x_button = tk.Button(root, text="Play as X", command=lambda: player_choice("X"))
choose_o_button = tk.Button(root, text="Play as O", command=lambda: player_choice("O"))
choose_x_button.grid(row=1, column=0, columnspan=1)
choose_o_button.grid(row=1, column=2, columnspan=1)

# Reset Game button
reset_game_button = tk.Button(root, text="Reset Game", command=reset_button)
reset_game_button.grid(row=1, column=1, columnspan=1)

# Tic Tac Toe board buttons
buttons = []
for i in range(9):
    button = tk.Button(root, text="", font=("Arial", 20), width=5, height=2, command=lambda j=i: player_move(j))
    button.grid(row=(i // 3) + 2, column=(i % 3))
    buttons.append(button)

def start():
    root.mainloop()
