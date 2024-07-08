import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid action")
    new_board = [row.copy() for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(all(cell is not EMPTY for cell in row) for row in board)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        value, move = max_value(board)
    else:
        value, move = min_value(board)
    
    return move

def max_value(board):
    if terminal(board):
        return utility(board), None

    v = -math.inf
    best_action = None

    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > v:
            v = min_val
            best_action = action

    return v, best_action

def min_value(board):
    if terminal(board):
        return utility(board), None

    v = math.inf
    best_action = None

    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v = max_val
            best_action = action

    return v, best_action

def print_board(board):
    """
    Prints the board to the console.
    """
    for row in board:
        print([" " if cell is None else cell for cell in row])
    print()

def play_game():
    """
    Runs a game of Tic-Tac-Toe between a human player and the AI.
    """
    board = initial_state()
    print("Initial board:")
    print_board(board)

    while not terminal(board):
        if player(board) == X:
            print("Player X's turn:")
            action = minimax(board)
        else:
            print("Player O's turn:")
            action = None
            while action not in actions(board):
                try:
                    i = int(input("Enter the row (0, 1, or 2): "))
                    j = int(input("Enter the column (0, 1, or 2): "))
                    action = (i, j)
                except ValueError:
                    print("Invalid input. Please enter numbers between 0 and 2.")
            if action not in actions(board):
                print("Invalid move. Try again.")
                continue
        
        board = result(board, action)
        print_board(board)

    win = winner(board)
    if win is not None:
        print(f"Player {win} wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()
