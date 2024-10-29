NEG_INF, POS_INF = float('-inf'), float('inf')

_player_move = "X"  # Player's symbol
visited = set()
game_board = [None] * 9

def set_player_move(move: str):
    global _player_move
    _player_move = move

def get_player_move() -> str:
    return _player_move


def get_current_state() -> list:
    return game_board

def reset_game():
    global game_board, visited
    game_board = [None] * 9
    visited = set()

def is_terminal(board: list) -> bool:
    # Check for a win or a draw
    return check_win(board) or check_draw(board)

def check_draw(board: list) -> bool:
    # A draw occurs when there are no None values left and no winner
    return all(cell is not None for cell in board) and not check_win(board)

def get_possible_moves(board: list) -> [tuple]:
    # Return a list of possible moves (indices where the board is None)
    return [(i,) for i in range(9) if board[i] is None]

def make_move(move: tuple, board: list, player: str) -> list:
    new_board = board[:]
    new_board[move[0]] = player
    return new_board

def evaluate(board: list) -> int:
    """
    Evaluate the board and return a score based on win/loss.
    :param board: current board state
    :return: 1 if AI wins, -1 if player wins, 0 otherwise
    """
    return check_win(board)  # Directly use check_win’s output

def minimax(board: list, isMax: bool, alpha: float = NEG_INF, beta: float = POS_INF) -> int:
    """
    Minimax algorithm with alpha-beta pruning to calculate the best score for AI.
    :param board: current board state
    :param isMax: True if AI's move, False if player's
    :param alpha: Alpha for pruning
    :param beta: Beta for pruning
    :return: score of the board state
    """
    score = evaluate(board)
    if score == 1 or score == -1 or check_draw(board):
        return score

    visited.add(tuple(board))  # Track visited states to avoid redundant calculations

    if isMax:
        best_score = NEG_INF
        for move in get_possible_moves(board):
            new_board = make_move(move, board, "X")
            score = minimax(new_board, False, alpha, beta)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = POS_INF
        for move in get_possible_moves(board):
            new_board = make_move(move, board, "O")
            score = minimax(new_board, True, alpha, beta)
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score

def check_win(board: list) -> int:
    """
    Returns 1 if AI has won, -1 if player has won, or 0 if no winner.
    :param board: current board state
    :return: POS_INF, NEG_INF, or 0
    """
    # Define winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]  # Diagonal
    ]

    player = get_player_move()  # Get the player's symbol
    ai_symbol = "O" if player == "X" else "X"  # Determine AI's symbol

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]]:
            if board[combo[0]] == ai_symbol:
                return 1  # AI wins
            elif board[combo[0]] == player:
                return -1  # Player wins

    return 0  # No winner
