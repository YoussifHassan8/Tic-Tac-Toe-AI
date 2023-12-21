import tkinter as tk
import tkinter.messagebox as messagebox

def check_winner():
    winning_positions = [
        [(i, 0), (i, 1), (i, 2)] for i in range(3)
        ] + [
        [(0, i), (1, i), (2, i)] for i in range(3)
        ] + [
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for positions in winning_positions:
        symbols = [board[row][col] for row, col in positions]
        if symbols.count('X') == 3:
            highlight_winner(positions, 'X')
            return True
        elif symbols.count('O') == 3:
            highlight_winner(positions, 'O')
            return True
    return False

def highlight_winner(positions, symbol):
    for row, col in positions:
        buttons[row][col].config(bg="Green" if symbol == 'X' else 'red', fg="white" if symbol == 'X' else 'black')

def button_click(row, col):
    global UserScore, PcScore

    if board[row][col] == " ":
        board[row][col] = "X"
        buttons[row][col].config(text="X")
        if check_winner():
            UserScore += 1
            update_scores("You")
            end_game("You win!")
        elif all(board[i][j] != " " for i in range(3) for j in range(3)):
            end_game("It's a draw!")
        else:
            computer_move()

def evaluate(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == 'X':
                return -10
            elif board[i][0] == 'O':
                return 10

        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == 'X':
                return -10
            elif board[0][i] == 'O':
                return 10

    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == 'X':
            return -10
        elif board[0][0] == 'O':
            return 10

    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == 'X':
            return -10
        elif board[0][2] == 'O':
            return 10

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                return None

    return 0

def minimax(board, depth, is_maximizing):
    score = evaluate(board)

    if score is not None:
        return score

    if is_maximizing:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = max(best, minimax(board, depth + 1, not is_maximizing))
                    board[i][j] = ' '
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = min(best, minimax(board, depth + 1, not is_maximizing))
                    board[i][j] = ' '
        return best

def best_move():
    best_val = -1000
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_val = minimax(board, 0, False)
                board[i][j] = ' '

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

def computer_move():
    global PcScore
    row, col = best_move()

    if row != -1 and col != -1:
        board[row][col] = 'O'
        buttons[row][col].config(text='O')

        if check_winner():
            PcScore += 1
            update_scores("PC")
            end_game("Computer wins!")
        elif all(board[i][j] != ' ' for i in range(3) for j in range(3)):
            end_game("It's a draw!")

def reset_board():
    global board
    board = [[" " for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", bg="white", fg="black")

def create_grid():
    global buttons
    grid_frame = tk.Frame(window)
    grid_frame.pack()

    buttons = [
        [tk.Button(grid_frame, text=" ", width=20, height=10, command=lambda row=i, col=j: button_click(row, col), font=100) for j in range(3)]
        for i in range(3)
    ]

    for i, row in enumerate(buttons):
        for j, button in enumerate(row):
            button.grid(row=i, column=j)

def update_scores(winner):
    if winner == "You":
        global UserScore
        UserScore += 1
    elif winner == "PC":
        global PcScore
        PcScore += 1
    Scoreboard.config(text=f"You: {UserScore}       PC: {PcScore}")

def end_game(message):
    messagebox.showinfo("Tic Tac Toe", message)
    reset_board()

window = tk.Tk()
window.title("Tic Tac Toe")

board = [[" " for _ in range(3)] for _ in range(3)]
UserScore = 0
PcScore = 0
Scoreboard = tk.Label(text=f"You: {UserScore}       PC: {PcScore}", font=100)
Scoreboard.pack()

restart_button = tk.Button(text="Restart", command=reset_board, font=100)
restart_button.pack()

create_grid()

window.mainloop()
