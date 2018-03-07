#Xueyang (Sean) Wang
#XW1154
#12/12/2017
#CS4613 AI Project: Mini Camelot

import time
from tkinter import*
from functools import partial

class Board: #basic board setup
    def __init__(self, white = None, black = None):
        self.board = [] #initialization
        for i in range(0,112):
            self.board.append("-") #empty space representation
        self.empty =  ['A1','A2','A3','B1','B2','C1','F1','G1','G2','H1','H2','H3','A12','A13','A14','B13','B14','C14',
                        'F14','G13','G14','H12','H13','H14']
        if white is None:
            self.white = ['C5','D5','E5','F5','D6','E6']
        else:
            self. white = white
        if black is None:
            self.black = ['D9',"E9",'C10','D10','E10','F10']
        else:
            self.black = black

    def print_board(self): #fill the board with pieces and print with coordinates
        for i in range(0, len(self.board)-1):
            self.board[i] = '-'
        for w_coord in self.white:
            index = coord_decode(w_coord)
            self.board[index] = 'W'
        for b_coord in self.black:
            index = coord_decode(b_coord)
            self.board[index] = 'B'
        for coord in self.empty:
            index = coord_decode(coord)
            self.board[index] = ''

        row = 0
        color = ""
        tag = ""
        for i in range(0, len(self.board)):
            if self.board[i] == '':
                color = "red"
                tag = "Empty"
            elif self.board[i] == "W":
                color = "white"
                tag = "Piece"
            elif self.board[i] == "B":
                color = "black"
                tag = "Piece"
            elif self.board[i] == "-":
                color = "LightBlue"
                tag = "Square"
            if i%8 == 0:
                row += 1
            cv.create_rectangle((i%8)*SqSize, row*SqSize, ((i%8)+1)*SqSize, (row+1)*SqSize, fill = color, tag = tag)
            cv.update()

def move(board, player=None):
    moves = [] #possible coordinates to moves to
    flag = False #must capture or not

    #initialize pieces to move
    if player is None:
        pieces = board.white + board.black
    elif player == 1:
        pieces = board.white
    elif player == -1:
        pieces = board.black
    else:
        return moves

    for coord in pieces: #decode to integers
        if coord[0] == 'A':
            row_moves = [-8,-7,1,8,9] #UP, RIGHT-UP, RIGHT, DOWN, RIGHT-DOWN
        elif coord[0] == 'H':
            row_moves = [-9,-8,-1,7,8] #LEFT-UP, UP, LEFT, LEFT-DOWN, DOWN
        else:
            row_moves = [-9,-8,-7,-1,1,7,8,9] #ALL 8
        index = coord_decode(coord)

        for loc in row_moves:
            #capturing move white to black, player
            if player == 1 and coord_encode(index + loc) in board.black:
                #testing edges/boundaries where it cannot skip over
                if(not(coord_encode(index + loc)[0] == 'A' and coord[0] == 'B')) and (not(coord_encode(index + loc)[0] == 'H' and coord[0] == 'G')):
                    new_locate = index + loc + loc #twice, skip-over, space immediately available
                    if new_locate in range(0,112) and coord_encode(new_locate) not in board.black and coord_encode(new_locate) not in board.white:
                        moves.append([coord, coord_encode(new_locate), coord_encode(index + loc)])
                        flag = True
            #capturing move black to white, AI
            if player == -1 and coord_encode(index + loc) in board.white:
                if(not(coord_encode(index + loc)[0] == 'A' and coord[0] == 'B')) and (not(coord_encode(index + loc)[0] == 'H' and coord[0] == 'G')):
                    new_locate = index + loc + loc
                    if new_locate in range(0,112) and coord_encode(new_locate) not in board.black and coord_encode(new_locate) not in board.white:
                        moves.append([coord, coord_encode(new_locate), coord_encode(index + loc)])
                        flag = True
            #cantering move white to white, player
            if player == 1 and coord_encode(index + loc) in board.white:
                if(not(coord_encode(index + loc)[0] == 'A' and coord[0] == 'B')) and (not(coord_encode(index + loc)[0] == 'H' and coord[0] == 'G')):
                    new_locate = index + loc + loc
                    if new_locate in range(0,112) and coord_encode(new_locate) not in board.black and coord_encode(new_locate) not in board.white:
                        moves.append([coord,coord_encode(new_locate), coord_encode(index + loc)])
            #cantering move black to black, AI
            if player == -1 and coord_encode(index + loc) in board.black:
                if(not(coord_encode(index + loc)[0] == 'A' and coord[0] == 'B')) and (not(coord_encode(index + loc)[0] == 'H' and coord[0] == 'G')):
                    new_locate = index + loc + loc
                    if new_locate in range(0,112) and coord_encode(new_locate) not in board.black and coord_encode(new_locate) not in board.white:
                        moves.append([coord,coord_encode(new_locate), coord_encode(index+loc)])
            #plain move for all
            if index + loc in range(0, 112) and coord_encode(index + loc) not in board.empty and coord_encode(index + loc) not in board.white and coord_encode(index + loc) not in board.black:
                moves.append([coord, coord_encode(index + loc)])

    if flag: #if capture, must perform capture moves
        temp = []
        for element in moves:
            if len(element) == 3: #either capture or cantering
                if player == 1 and element[2] in board.black: #if white, then capture has to be black
                    temp.append(element)
                if player == -1 and element[2] in board.white: #if black, then capture has to be white
                    temp.append(element)
        moves = list(temp)
    return moves

def HumanTurn1(event):
    global maxD, Nodes, maxP, minP, start_time
    maxD = 0  # MaxDepth
    Nodes = 0  # Nodes Generated
    maxP = 0  # MaxNodes Prunes
    minP = 0  # MinNodes Prunes
    start_time = 0  # 10sec rules for AB search
    global coor
    coor.append(coord_encode(event.x // SqSize + (event.y // SqSize - 1) * 8))

def HumanTurn2(event):
    global coor
    coor.append(coord_encode(event.x // SqSize + (event.y // SqSize - 1) * 8))

def HumanTurn3(event):
    global coor
    coor.append(coord_encode(event.x // SqSize + (event.y // SqSize - 1) * 8))
    player_move(g)

def suc_move(board):
    global human_num
    if win(board) != 0:
        end(win(board))
    print("Successive Moves Activated! Another move? (Y/N)")
    cont = input()
    if (cont.upper() == "Y"):
        human_num = 1
    else:
        human_num = -1
    cv.update()

def player_move(board):
    global human_num,coor #more than one move
    global x,y
    print(board.white)
    if win(board) != 0:
        end(win(board))
    print("Selection")
    if human_num == -1:
        ai_move(board, ab_search(board,0))
        return

    coordinate = coor
    coor = []
    print(coordinate)
    if len(coordinate) == 3:
        if coordinate[2]== 'A1': #if plain move
            coordinate.remove('A1')
    else:
        print("That is not an acceptable move! Try again...")
        print(move(board,1))
        return

    if coordinate in move(g,1):
        for piece in range(0,len(board.white)): #movement
            if board.white[piece] == coordinate[0]:
                board.white[piece] = coordinate[1]
                cv.update()
                board.print_board()
        if len(coordinate) == 3: #capturing move or cantering
            if coordinate[2] in board.black: #if removal is a black piece
                board.black.remove(coordinate[2])
                cv.update()
                board.print_board()
            suc_move(board)
            if human_num == 1:
                print("Make another move!")
                return
            else:
                ai_move(board, ab_search(board, 0))
        else:
            ai_move(board,ab_search(board,0))
    else: #prompt for input again
        print("That is not an acceptable move! Try again...")
        print(move(board,1))
        return

def ai_move(board, given_move):
    global human_num
    result()
    if given_move in move(board,-1):
        for p in range(0,len(board.black)): #movement
            if board.black[p] == given_move[0]:
                board.black[p] = given_move[1]
        if len(given_move) == 3: #capturing or cantering
            if given_move[2] in board.white:
                board.white.remove(given_move[2])
    else: #error, cannot move
        print("Error - AI moves")
    if win(board) != 0:
        end(win(board))
    print("Please make your selection")
    human_num = 1
    cv.update()
    g.print_board()

def ab_search(board, depth):
    global maxD
    global Nodes
    global maxP
    global minP
    global start_time
    global depth_limit
    global u_value
    #Initialization
    start_time = float(time.time())
    Nodes += 1
    alpha = -u_value
    beta = u_value
    flag = None #capturing move, must return

    possible_moves = move(board,-1)
    moves_and_val = {}

    for m in range(0, len(possible_moves)):
        new_move = possible_moves[m]
        new_board = Board(list(board.white), list(board.black))  # search tree, assume such move is made
        for b in range(0, len(new_board.black)): #movements
            if new_board.black[b] == new_move[0]:
                new_board.black[b] = new_move[1]
        if len(new_move) == 3: #capturing move or cantering
            flag = new_move
            if new_move[2] not in board.black:
                new_board.white.remove(new_move[2])
        value = maxV(new_board,alpha,beta,depth+1) #pruning
        moves_and_val[m] = value

    best = min(moves_and_val, key = moves_and_val.get) #selecting values
    finish_time = float(time.time())

    print("Time:", finish_time - start_time) #print total time spent in AB search
    print("Utility:",int(moves_and_val[best])) #print best evaluated number
    if flag is None:
        return possible_moves[best]
    else:
        return flag

def maxV(board, alpha, beta, depth): #player alpha value
    global maxD
    global Nodes
    global maxP
    global minP
    global u_value
    Nodes += 1
    maxD = max(maxD, depth)

    if terminate(board, depth):
        return u_eval(board)
    value = -u_value
    possible_moves = move(board, 1)
    for moves in possible_moves:
        new_board = Board(list(board.white), list(board.black))
        for p in range(0, len(new_board.white)):
            if new_board.white[p] == moves[0]:
                new_board.white[p] = moves[1]
        if len(moves) == 3:
            if moves[2] not in new_board.white:
                new_board.black.remove(moves[2])
        value = max(value,minV(new_board,alpha,beta,depth+1))
        if value >= beta:
            maxP += 1
            return value
        alpha = max(alpha,value)
    return value

def minV(board, alpha, beta, depth): #AI beta value
    global maxD
    global Nodes
    global maxP
    global minP
    global u_value

    Nodes += 1
    maxD = max(maxD, depth)

    if terminate(board, depth):
        return u_eval(board)
    value = u_value
    possible_moves = move(board, -1)
    for moves in possible_moves:
        new_board = Board(list(board.white), list(board.black))
        for p in range(0, len(new_board.black)):
            if new_board.black[p] == moves[0]:
                new_board.black[p] = moves[1]
        if len(moves) == 3:
            if moves[2] not in new_board.black:
                new_board.white.remove(moves[2])
        value = min(value, maxV(new_board, alpha, beta, depth + 1))
        if value <= alpha:
            minP += 1
            return value
        beta = min(beta, value)
    return value

def coord_decode(coord): #decoding player location on grid into integer
    coord_dict = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
    if len(coord)>3 or coord[0] not in coord_dict.keys():
        print("Error, coordinate not found")
    else:
        index = (int(coord[1:])*8) + coord_dict[coord[0]]
        return index-8

def coord_encode(index): #encoding player location on grid into string
    index_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H'}
    row = int(index/8)+1
    col = index_dict[index%8]
    return str(col) + str(row)

def terminate(board, depth): #terminal stage
    global start_time #time
    global depth_limit #depth

    current_time = float(time.time()) #current running
    if depth != 0 and (current_time - start_time) >= 9.9:
        return True #terminate: too long
    if depth >= depth_limit:
        return True #terminate: too deep
    state = win(board) #check winning conditions
    if state == 1 or state == -1 or state == 2:
        return True #terminate: winner found or draw
    return False

def win(board): #checking winning conditions
    white_win = ['D14','E14'] #white goals
    black_win = ['D1','E1'] #black goals
    if len(board.white) == 1 and len(board.black) == 1:
        return 2 #if only one w_/b_warrior lef
    if len(board.white) == 0 and len(board.black) >= 2: #if no w_warriors are left
        return -1
    if len(board.black) == 0 and len(board.white) >= 2: #if no b_warriors are left
        return 1

    count_W = 0
    count_B = 1
    #otherwise, check if white_win or black_win is satisfied
    for coord in board.white:
        if coord in white_win:
            count_W += 1
            if count_W == 2:
                return 1
    for coord in board.black:
        if coord in black_win:
            count_B += 1
            if count_B == 2:
                return -1
    return 0

def result(): #Printing required information per step done by AI
    print("Max Depth: ", maxD)
    print("Nodes Generated: ", Nodes)
    print("Max Pruned: ", maxP)
    print("Min Pruned: ", minP)

def end(num):
    if num == 1:
        print("GAME OVER. White has won the game")
        MainGUI.destroy()
    elif num == -1:
        print("GAME OVER. Black has won the game")
        MainGUI.destroy()
    elif num == 2:
        print("GAME OVER. Draw")
        MainGUI.destroy()

#updated evaluation function with heristics
def u_eval(board): #return a utility value based on current board
    #update with based on integer distance
    global u_value
    bd = 14 #Minimal Black castle distance from white pieces
    wd = 14 #Minimal White castle distance from black pieces

    white_winners = ['D14','E14']
    black_winners = ['D1','E1']

    distance = 14 #White piece from black piece

    for i in board.white:
        if i in white_winners:
            return u_value
        for w in white_winners:
            bd = min(bd,(coord_decode(w) - coord_decode(i))/8)

    for i in board.black:
        if i in black_winners:
            return -u_value
        for b in black_winners:
            wd = abs(min(bd,(coord_decode(b) - coord_decode(i))/8))

    eval_num = 0.5*((len(board.white) - len(board.black))/6)
    eval_num = 0.25*(1/wd) + 0.25*(1/bd)

    return eval_num * u_value

    #for j in board.black:
     #   far += (())

#Creating an input for user to choose going first or going second
def getOrder():
    global human_num,set
    LP = Label(MainGUI, text="Would you like to go first(F) or second(S)?", justify=LEFT, padx=10)
    LP1 = Radiobutton(MainGUI, text="First", padx=10, variable=order, value=1)
    LP2 = Radiobutton(MainGUI, text="Second", padx=10, variable=order, value=-1)
    LP.grid(row=0, column=1, columnspan=3)
    LP1.grid(row=1, column=2, columnspan=1)
    LP2.grid(row=1, column=3, columnspan=1)
    human_num = order.get()
    if order.get() == 1 or order.get() == -1:
        set = 1

# Creating an input for user to choose difficulty
def getLevel():
    global u_value, depth_limit,set
    DP = Label(MainGUI, text="How difficult do you want the game to be?", justify=LEFT, padx=20)
    DP1 = Radiobutton(MainGUI, text="Level 1", padx=10, variable=level, value=1, command=g.print_board())
    DP2 = Radiobutton(MainGUI, text="Level 2", padx=10, variable=level, value=2, command=g.print_board())
    DP3 = Radiobutton(MainGUI, text="Level 3", padx=10, variable=level, value=3, command=g.print_board())
    DP.grid(row=2, column=1, columnspan=4)
    DP1.grid(row=3, column=1, columnspan=1)
    DP2.grid(row=3, column=2, columnspan=1)
    DP3.grid(row=3, column=3, columnspan=1)
    u_value = 0
    if level.get() == 1:
        u_value = 50
    elif level.get() == 2:
        u_value = 100
    elif level.get() == 3:
        u_value = 1000
    depth_limit = level.get() + 3
    if set == 1 and (level.get() == 1 or level.get() == 2 or level.get() == 3):
        set = 2

SqSize = 40
Piece_diameter = 38
piece_offset = (SqSize-Piece_diameter)
MainGUI = Tk()
order = IntVar()
level = IntVar()
suc = IntVar()
x = 0
y = 0
set = 0
maxD = 0  # MaxDepth
Nodes = 0  # Nodes Generated
maxP = 0  # MaxNodes Prunes
minP = 0  # MinNodes Prunes
start_time = 0  # 10sec rules for AB search
MainGUI.title("My AI Game Mini Camelot")
h = SqSize*15
w = SqSize*8
cv = Canvas(MainGUI,height = h, width = w)
cv.grid(row = 7, column = 0 )
human_num = IntVar() #default going first
u_value = 50 #default evaluation value
depth_limit = IntVar() # difficulty evaluation
#  default depth_limit is 3

g = Board() #GAME BOARD

while set != 2 :
    getOrder()
    getLevel()
print("GAME GENERATING...")
maxD = 0  # MaxDepth
Nodes = 0  # Nodes Generated
maxP = 0  # MaxNodes Prunes
minP = 0  # MinNodes Prunes
start_time = 0  # 10sec rules for AB search
flag = False
coor = []
if human_num == 1:
    print("Please select the piece you want to move! Using Left Click")
    cv.bind("<Double-Button-1>" ,HumanTurn1)
    print("Please select the location you are moving to! Using Right Cluck")
    cv.bind("<Double-Button-3>" ,HumanTurn2)
    print("If capturing or cantering, please clicked on the piece you are jumping over. If plain move please click first box")
    print("Using Middle Click")
    cv.bind("<Double-Button-2>",HumanTurn3)
else:
    ai_move(g,ab_search(g, 0))
    print("Please select the piece you want to move! Using Left Click")
    cv.bind("<Double-Button-1>" ,HumanTurn1)
    print("Please select the location you are moving to! Using Right Cluck")
    cv.bind("<Double-Button-3>" ,HumanTurn2)
    print("If capturing or cantering, please clicked on the piece you are jumping over. If plain move please click first box")
    print("Using Middle Click")
    cv.bind("<Double-Button-2>",HumanTurn3)
MainGUI.mainloop()
