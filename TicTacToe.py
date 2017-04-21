# https://gist.github.com/fheisler/430e70fa249ba30e707f

board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] # Initial empty board

def gameplay:
    noWin = true
    player_x_turn = true
    while noWin:
        char = 'X' if player_x_turn == true else 'O'
        # llamar player move mandando BOARD

        # Actualizar board con la posicioin retornada por oplayermove

        #Validate if win and add reward to winner and loser and exit while

        #Validar si board is full after knowing there is no winner to add reward reward to both players TIE! exit while
        player_x_turn = false

def available_moves(board):
    available_spots = []
    for i in range(0,9):
        if board[i] == ' ':
            available_spots << i + 1

def q_learning_move(board):
    last_board = tuple(board)
