# https://gist.github.com/fheisler/430e70fa249ba30e707f
import random
import cPickle as pickle

x_wins = 0
ties = 0
policy = 0.9
learning_rate = 0.9
discount_factor = 0.9
q = {}

def available_moves(current_board):
    available_spots = []
    for i in range(0,9):
        if current_board[i] == ' ':
            available_spots.append(i + 1)

    return available_spots

def getQ(board, action):
    if q.get((board, action)) is None:
        q[(board, action)] = 1.0
    return q.get((board, action))

def get_qO(board, action):
    if q_O.get((board, action)) is None:
        q_O[(board, action)] = 1.0
    return q_O.get((board, action))

def calculate_Qs(current_board, actions):
    qs = []
    for action in actions:
        if q.get((current_board, action)) is None:
            q[(current_board, action)] = 1.0
        qs.append(q)

    return qs

def q_learning_move_O(last_move, current_board):
    last_board = tuple(current_board)
    possible_actions = available_moves(current_board)
    qs = [get_qO(last_board, a) for a in possible_actions]
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

def q_learning_move(last_move, current_board, policy=0.5):
    last_board = tuple(current_board)
    possible_actions = available_moves(current_board)
    if random.random() < policy:
        last_move = random.choice(possible_actions)
    else:
        qs = [getQ(last_board, a) for a in possible_actions]
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
        learn(prev_val['last_board'], prev_val['last_move'], value, tuple(board))

def check_win(playerX, board,prev_val):
    global x_wins
    global ties
    char = 'X' if playerX == True else 'O'
    game_in_progres = True
    #Validate if win and add reward to winner and loser and exit while
    for a,b,c in [(0,1,2), (3,4,5), (6,7,8),
                  (0,3,6), (1,4,7), (2,5,8),
                  (0,4,8), (2,4,6)]:
        if char == board[a] == board[b] == board[c]:
            game_in_progres = False
            display_board(board)
            print "\n\n"
            if playerX:
                x_wins += 1
                reward(prev_val, board, 1)
            else:
                reward(prev_val, board, -1)

    #Validar si board is full after knowing there is no winner to add reward reward to both players TIE! exit while
    if game_in_progres:
        if not any([space == ' ' for space in board]): # tied game
            game_in_progres = False
            display_board(board)
            print "\n\n"
            if playerX:
                ties += 1
                reward(prev_val, board, 0.5)

    return game_in_progres

def display_board(board):
        row = " {} | {} | {}"
        hr = "\n-----------\n"
        print (row + hr + row + hr + row).format(*board)

def train():
    global policy
    board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] # Initial empty board
    last_move = None
    game_in_progres = True
    player_x_turn = True
    while game_in_progres:
        char = 'X' if player_x_turn == True else 'O'
        # Player move

        if player_x_turn:
            prev_val = q_learning_move(last_move,board,policy)
            spot = prev_val['last_move']
        else:
            #prev_val = q_learning_move_O(last_move,board)
            spot = random.choice(available_moves(board))#prev_val['last_move']

        # Actualizar board con la posicion retornada por oplayermove
        board[spot-1] = char
        game_in_progres = check_win(player_x_turn, board,prev_val)
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
            prev_val = q_learning_move(last_move,board, 0)
            spot = prev_val['last_move']
        else:
            display_board(board)
            spot = int(raw_input("Your move? "))

        # Actualizar board con la posicion retornada por oplayermove
        board[spot-1] = char
        game_in_progres = check_win(player_x_turn, board,prev_val)
        player_x_turn = False if player_x_turn else True

fileObject = open("trained_rival",'r')
q_O = pickle.load(fileObject)
for i in xrange(0,1000000):
    train()
print "X stats"
print "WINS", x_wins
print "Ties", ties
print "Lost", 1000000 - x_wins - ties

while True:
    game()

'''
Lo entrenamos jugando contra un rival que juega aleatorio y tambien contra un rival
que ya sabia jugar
Jugando contra un rival que ya sabia jugar muy bien obtuvo
WINS 0 Ties 72075, Lost 927925. Jugando contra este un humanoi, notamos que no sabia jugar, debido
a que en el entrenamiento nunca pudo ganar... bla bla

COmparando con un algortimo de un tercero, el entrena ambos contricantes,
por lo que alcanza un aprendizaje mayor en menos iteraciones. EL prendizaje ideal
es es, mejor que entrenar contra un random o entrenar contra un rival que ya sabe jugar

Para aprender usamos learning policy de 0.5, jugando contra Humano, de CERO Para
que solo jugara con lo que aprendio y no usando escogencias aleatorias

Prueba 1:
learning_rate = 0.3
discount_factor = 0.9
Iteraciones aprendiendo: 1000000
WINS 777888
Ties 100367
Lost 121745

Prueba 2:
learning_rate = 0.3
discount_factor = 0.9
Iteraciones aprendiendo: 1000000
X stats
WINS 778279
Ties 99962
Lost 121759

Prueba 3:
learning_rate = 0.3
discount_factor = 0.1
Iteraciones aprendiendo: 1000000
X stats
WINS 779495
Ties 99872
Lost 120633

Prueba 4:
learning_rate = 0.1
discount_factor = 0.1
Iteraciones aprendiendo: 1000000
X stats
WINS 777752
Ties 99696
Lost 122552

Prueba 5: - POLICY CHANGED! REDUCED TO .2
learning_rate = 0.3
discount_factor = 0.1
Iteraciones aprendiendo: 1000000
X stats
WINS 861010
Ties 78102
Lost 60888

Prueba 5: -POLICY CHANGED! REDUCED TO .9
learning_rate = 0.3
discount_factor = 0.1
Iteraciones aprendiendo: 1000000
X stats
WINS 655859
Ties 122305
Lost 221836
'''
