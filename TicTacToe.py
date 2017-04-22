# https://gist.github.com/fheisler/430e70fa249ba30e707f
import random

policy = 0.5
learning_rate = 0.3
discount_factor = 0.9
q = {}

def available_moves(current_board):
    available_spots = []
    for i in range(0,9):
        if current_board[i] == ' ':
            available_spots << i + 1
def getQ(board, action):
    return q.get((board, action))

def calculate_Qs(current_board, actions):
    qs = []
    for action in actions:
        if q.get((current_board, action)) is None:
            q[(current_board, action)] = 1.0
        qs.append(q)
    return qs


def q_learning_move(last_move, current_board):
    last_board = tuple(current_board)
    possible_actions = available_moves(current_board)
    if random.random() < policy:
        last_move = random.choice(possible_actions)
    else:
        qs = [getQ(current_board, a) for a in possible_actions]
        maximum_Q = max(qs)
        if maximum_Q > 1:
            best_options = [i for i in range(len(possible_actions)) if qs[i] == maximum_Q]
            #for i in range(len(possible_actions)):
            #    if qs[i] == maximum_Q:
            #        best_options.append(i)
            index_selected = random.choice(best_options)
        else:
            index_selected = qs.index(maximum_Q)
        last_move = possible_actions[index_selected]
    prev_val={'last_board':last_board,'last_move':last_move}
    return prev_val


def learn(state, action, reward, result_state):
    prev = getQ(state, action)
    maxqnew = max([getQ(result_state, a) for a in available_moves(state)])
    q[(state, action)] = prev + learning_rate * ((reward + discount_factor*maxqnew) - prev)


def reward(prev_val, board, value):
    if prev_val['last_move']:
        learn(prev_val['last_board'], prev_val['last_move'], value, tuple(board)))

def check_win(playerX):
    #Validate if win and add reward to winner and loser and exit while
    for a,b,c in [(0,1,2), (3,4,5), (6,7,8),
                  (0,3,6), (1,4,7), (2,5,8),
                  (0,4,8), (2,4,6)]:
        if char == board[a] == board[b] == board[c]:
            game_in_progres = False
            if playerX:
                reward(prev_val, board, 1)

    #Validar si board is full after knowing there is no winner to add reward reward to both players TIE! exit while
    if game_in_progres:
        if not any([space == ' ' for space in board]): # tied game
            game_in_progres = False
            if playerX:
                reward(prev_val, board, 0.5)

    return game_in_progres

def display_board(board):
        row = " {} | {} | {}"
        hr = "\n-----------\n"
        print (row + hr + row + hr + row).format(*board)

def train():
    board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] # Initial empty board
    last_move = None
    game_in_progres = True
    player_x_turn = True
    while game_in_progres:
        char = 'X' if player_x_turn == True else 'O'
        # Player move

        if player_x_turn:
            prev_val = q_learning_move(last_move,board)
            spot = prev_val['last_move']
        else:
            spot = random.choice(available_moves(board))

        # Actualizar board con la posicion retornada por oplayermove
        board[spot-1] = char
        game_in_progres = check_win(player_x_turn)
        player_x_turn = False if player_x_turn else True


def game():
    board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] # Initial empty board
    last_move = None
    game_in_progres = True
    player_x_turn = True
    while game_in_progres:
        char = 'X' if player_x_turn == True else 'O'
        # Player move
        if player_x_turn:
            prev_val = q_learning_move(last_move,board)
            spot = prev_val['last_move']
        else:
            display_board(board)
            spot = int(raw_input("Your move? "))

        # Actualizar board con la posicion retornada por oplayermove
        board[spot-1] = char
        game_in_progres = check_win(player_x_turn)
        player_x_turn = False if player_x_turn else True


for i in xrange(0,200000):
    train()

while True:
    gameplay()
