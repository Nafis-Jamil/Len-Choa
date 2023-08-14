import pygame as pg
import math
import copy
import random
points = [(600, 200),
          (500, 400),
          (600, 400),
          (700, 400),
          (400, 600),
          (600, 600),
          (800, 600),
          (300, 800),
          (600, 800),
          (900, 800)
          ]
start_page_points=[
    (314,264),
    (614,264),
    (914,264)
]

hor = 80
ver = 120
initial_points = [(hor, ver)]
ver = ver + 90
for i in range(6):
    initial_points.append((hor, ver))
    hor = hor + 80
    if i == 2:
        ver = ver + 90
        hor = 80


def calculateDistance(X, Y):
    val = ((X[0] - Y[0]) ** 2) + ((X[1] - Y[1]) ** 2)
    dist = math.sqrt(val)
    return dist


EMPTY = 0
TIGER = 1
FOX = 2
INVALID = -1
tiger_stage0 = True
fox_stage0 = True
turn = TIGER
tiger_position = INVALID
fox_kill = 0
fox_position = INVALID
count=0
INFINITY= math.inf
DEPTH=4
selected_state = []
START_PAGE=0
TIGER_AI=1
FOX_AI=2
MULTI_MODE=3
GAME_OVER=4
page=START_PAGE
gameboard = [0] * 10
initial_gameboard = [1, 2, 2, 2, 2, 2, 2]
HUMAN= INVALID


class Node(object):
    def __init__(self, hop1, hop2):
        self.hop1 = hop1
        self.hop2 = hop2


nodes = []

nodes.append(Node([1, 2, 3], [4, 5, 6]))
nodes.append(Node([0, 2, 4], [3, 7]))
nodes.append(Node([0, 1, 3, 5], [8]))
nodes.append(Node([0, 2, 6], [1, 9]))
nodes.append(Node([1, 5, 7], [0, 6]))
nodes.append(Node([2, 4, 6, 8], [0]))
nodes.append(Node([3, 5, 9], [4,0]))
nodes.append(Node([4, 8], [1, 9]))
nodes.append(Node([5, 7, 9], [2]))
nodes.append(Node([6, 8], [3, 7]))

pg.init()
screen = pg.display.set_mode((1200, 1000))
pg.display.set_caption("Len Choa")
tiger_path = 'tiger.png'
fox_path = 'fox.png'
tiger_start_path= 'tigerStart.png'
fox_start_path= 'foxStart.png'
multiplayer_path= 'multiplayer.png'
tiger_sprite = pg.image.load(tiger_path)
fox_sprite = pg.image.load(fox_path)
tiger_start_icon= pg.image.load(tiger_start_path)
fox_start_icon= pg.image.load(fox_start_path)
multiplayer_icon= pg.image.load(multiplayer_path)
screen2= pg.Surface((64,64),pg.SRCALPHA)
pg.draw.circle(screen2,(0,255,0,80),(32,32),32)
winner=INVALID
tfont= pg.font.SysFont("Arial",80)

def game_setup():
    global count,page,gameboard,initial_gameboard,tiger_stage0,fox_stage0,turn,tiger_position,fox_kill,fox_position
    global HUMAN,selected_state
    page = START_PAGE
    gameboard = [0] * 10
    initial_gameboard = [1, 2, 2, 2, 2, 2, 2]
    tiger_stage0 = True
    fox_stage0 = True
    turn = TIGER
    tiger_position = INVALID
    fox_kill = 0
    fox_position = INVALID
    global winner
    winner=INVALID
    HUMAN=INVALID
    count=0
    selected_state=[]

def draw(char_type, xy):
    if char_type == TIGER:
        screen.blit(tiger_sprite, (xy[0] - 32, xy[1] - 32))
    elif char_type == FOX:
        screen.blit(fox_sprite, (xy[0] - 32, xy[1] - 32))

def display_text(text, font, color, x, y):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))

def board():
    pg.draw.aaline(screen, (0, 0, 0), points[0], points[7])
    pg.draw.aaline(screen, (0, 0, 0), points[7], points[9])
    pg.draw.aaline(screen, (0, 0, 0), points[0], points[9])
    pg.draw.aaline(screen, (0, 0, 0), points[0], points[8])
    pg.draw.aaline(screen, (0, 0, 0), points[1], points[3])
    pg.draw.aaline(screen, (0, 0, 0), points[4], points[6])



def drawGame():
    screen.fill((255, 246, 225))
    board()

    if(fox_position!=INVALID):
        for i in nodes[fox_position].hop1:
            if(gameboard[i]==EMPTY):
                screen.blit(screen2,(points[i][0]-32,points[i][1]-32))

    for i in range(7):
        draw(initial_gameboard[i], initial_points[i])
    for i in range(10):
        draw(gameboard[i], points[i])
    pg.display.update()


def check_if_valid_initial(axes):
    for i in range(10):
        dist = calculateDistance(points[i], axes)
        if dist < 32 and gameboard[i] == EMPTY:
            return i
    return INVALID


def can_tiger_jump(pos, hop2):
    distance = hop2 - pos
    print("jamil")
    if (distance > 0):
        if (distance > 3):
            print(gameboard[pos + 3])
            if (gameboard[hop2 - 3] == FOX):
                gameboard[hop2 - 3] = EMPTY
                return True
        elif (distance < 3):
            if (gameboard[hop2 - 1] == FOX):
                gameboard[hop2 - 1] = EMPTY
                return True
    else:
        if (distance > -3):
            if (gameboard[pos - 1] == FOX):
                gameboard[pos - 1] = EMPTY
                return True
        elif (distance < -3):
            if (gameboard[pos - 3] == FOX):
                gameboard[pos - 3] = EMPTY
                return True
    return False



def tiger_check_if_valid(axes):
    global fox_kill
    position = INVALID
    for i in range(10):
        dist = calculateDistance(points[i], axes)
        if dist <= 32:
            position = i
            break
    if (position == INVALID):
        return position
    for i in nodes[tiger_position].hop1:
        if i == position and gameboard[i] == EMPTY:
            return position
    for i in nodes[tiger_position].hop2:
        if i == position and gameboard[i] == EMPTY:
            if (can_tiger_jump(tiger_position, i)):
                fox_kill += 1
                return position
            break

    return INVALID


def fox_check_selected(axes):
    for i in range(10):
        dist = calculateDistance(points[i], axes)
        if dist <= 32 and gameboard[i] == FOX:
            return i
    return fox_position

def fox_check_if_valid(axes):
    position = INVALID
    for i in range(10):
        dist = calculateDistance(points[i], axes)
        if dist <= 32:
            position = i
            break
    if (position == INVALID):
        return position
    for i in nodes[fox_position].hop1:
        if i == position and gameboard[i] == EMPTY:
            return position
    return INVALID


def is_tiger_trapped():
    position = 0
    for i in range(10):
        if (gameboard[i] == TIGER):
            position = i
            break
    for i in nodes[position].hop1:
        if gameboard[i] == EMPTY:
            return False
    for i in nodes[position].hop2:
        if gameboard[i]==EMPTY:
            return False
    return True
def heuristic_score(state):
    freespace = 0
    killscore = 0
    tiger_pos = 0
    for i in range(len(state[0])):
        if (state[0][i] == TIGER):
            tiger_pos = i
            break;
    for i in nodes[tiger_pos].hop1:
        if (state[0][i] == EMPTY):
            freespace += 1
    if (state[1]):
        killscore = 5
    return killscore + freespace


def find_all_moves(state, type, depth):
    if type == TIGER:
        states = []
        tiger_pos = 0
        for i in range(10):
            if (state[i] == TIGER):
                tiger_pos = i
                break
        for i in nodes[tiger_pos].hop1:
            if (state[i] == EMPTY):
                st = copy.deepcopy(state)
                st[tiger_pos] = EMPTY
                st[i] = TIGER
                states.append((st,False))
        for i in nodes[tiger_pos].hop2:
            if (state[i] == EMPTY):
                distance = i - tiger_pos
                if (distance > 0):
                    if (distance > 3):
                        if (state[i - 3] == FOX):
                            st = copy.deepcopy(state)
                            st[tiger_pos] = EMPTY
                            st[i] = TIGER
                            st[i - 3] = EMPTY
                            states.append((st,True))

                    elif (distance < 3):
                        if (state[i - 1] == FOX):
                            st = copy.deepcopy(state)
                            st[tiger_pos] = EMPTY
                            st[i] = TIGER
                            st[i - 1] = EMPTY
                            states.append((st,True))

                else:
                    if (distance > -3):
                        if (state[tiger_pos - 1] == FOX):
                            st = copy.deepcopy(state)
                            st[tiger_pos] = EMPTY
                            st[i] = TIGER
                            st[tiger_pos - 1] = EMPTY
                            states.append((st,True))

                    elif (distance < -3):
                        if (state[tiger_pos - 3] == FOX):
                            st = copy.deepcopy(state)
                            st[tiger_pos] = EMPTY
                            st[i] = TIGER
                            st[tiger_pos - 3] = EMPTY
                            states.append((st,True))
        return states
    else:
        states = []
        n=0
        if(fox_stage0):
            if(turn==TIGER):
                n= ((DEPTH-depth)+1)/2
            else:
                n= ((DEPTH-depth)+2)/2



        if (fox_stage0 and count+n < 7 ):

            for i in range(len(state)):
                if (state[i] == EMPTY):
                    st = copy.deepcopy(state)
                    st[i] = FOX
                    states.append((st,False))

        else:
            fox_positions = []
            for i in range(len(state)):
                if (state[i] == FOX):
                    fox_positions.append(i)

            for i in fox_positions:
                for j in nodes[i].hop1:
                    if (state[j] == EMPTY):
                        st = copy.deepcopy(state)
                        st[i] = EMPTY
                        st[j] = FOX
                        states.append((st,False))
        return states





def minimax(state, depth, type):
    global selected_state
    if depth == 0:
        return heuristic_score(state)
    if type == TIGER:
        maxVal = -INFINITY
        new_states = find_all_moves(state[0], type,depth)
        for i in new_states:
            val = minimax(i, depth - 1, FOX)
            if (val >= maxVal):
                if depth==DEPTH and val > maxVal:
                    selected_state.clear()
                    selected_state.append(i[0])
                elif depth==DEPTH and val == maxVal:
                    selected_state.append(i[0])
                maxVal=val
        return maxVal

    else:
        minVal = 5 * (depth + 1)

        if (state[1] != True):
            new_states = find_all_moves(state[0], type,depth)
            for i in new_states:
                val = minimax(i, depth - 1, TIGER)

                if (val <= minVal):
                    if depth == DEPTH and val < minVal:
                        selected_state.clear()
                        selected_state.append(i[0])
                    elif depth == DEPTH and val == minVal:
                        selected_state.append(i[0])
                    minVal = val

        return minVal




# game loop
def multiplayer_mode():
    global turn,tiger_stage0,tiger_position,fox_stage0,count,fox_position,winner,page
    while page==MULTI_MODE:
        pg.time.delay(50)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.type == pg.MOUSEBUTTONDOWN:
                    axes = pg.mouse.get_pos()
                    if (turn == TIGER):
                        if (tiger_stage0):
                            idx = check_if_valid_initial(axes)
                            if (idx != INVALID):
                                initial_gameboard[0] = EMPTY
                                tiger_position = idx
                                gameboard[tiger_position] = TIGER
                                tiger_stage0 = False
                                turn = FOX
                        else:
                            idx = tiger_check_if_valid(axes)
                            if (idx != INVALID):
                                gameboard[tiger_position] = EMPTY
                                tiger_position = idx
                                gameboard[tiger_position] = TIGER
                                turn = FOX
                    elif (turn == FOX):
                        if (fox_stage0):
                            idx = check_if_valid_initial(axes)
                            if (idx != INVALID):
                                initial_gameboard[count + 1] = EMPTY
                                gameboard[idx] = FOX

                                count += 1
                                turn = TIGER
                            if count > 5:
                                fox_stage0 = False
                        else:

                            fox_position = fox_check_selected(axes)
                            if (fox_position != INVALID):
                                idx = fox_check_if_valid(axes)
                                if (idx != INVALID):
                                    gameboard[fox_position] = EMPTY
                                    gameboard[idx] = FOX
                                    turn = TIGER
                                    fox_position = INVALID


        drawGame()
        pg.event.clear()
        if(fox_kill>2):
            winner=TIGER
            drawGame()
            page=GAME_OVER
        if(is_tiger_trapped()):
            winner=FOX
            drawGame()
            page=GAME_OVER






#tiger ai
# drawGame()
def tiger_ai():
    global fox_stage0, count, gameboard, turn, fox_kill,fox_position,winner,page, selected_state
    drawGame()
    while page==TIGER_AI:
        pg.time.delay(50)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                axes = pg.mouse.get_pos()
                if (turn == FOX):

                    if (fox_stage0):
                        idx = check_if_valid_initial(axes)
                        if (idx != INVALID):
                            initial_gameboard[count + 1] = EMPTY
                            gameboard[idx] = FOX
                            count += 1
                            turn = TIGER
                        if count > 5:
                            fox_stage0 = False
                    else:
                        fox_position = fox_check_selected(axes)
                        if (fox_position != INVALID):
                            idx = fox_check_if_valid(axes)
                            if (idx != INVALID):
                                gameboard[fox_position] = EMPTY
                                gameboard[idx] = FOX
                                turn = TIGER
                                fox_position = INVALID

        drawGame()

        if turn == TIGER:
            selected_state = []
            pg.time.delay(1000)
            val = minimax((gameboard, False), DEPTH, TIGER)
            if(len(selected_state)==0):
                winner = FOX
                drawGame()
                page = GAME_OVER
                break
            random.shuffle(selected_state)
            for i in range(10):
                if (gameboard[i] == FOX):
                    if (selected_state[0][i] == EMPTY):
                        fox_kill += 1
                        break
            gameboard = copy.deepcopy(selected_state[0])

            turn = FOX
            initial_gameboard[0] = EMPTY

        pg.event.clear()
        if (fox_kill > 2):
            winner = TIGER
            drawGame()
            page=GAME_OVER
        if (is_tiger_trapped()):
            winner = FOX
            drawGame()
            page=GAME_OVER




#FOX AI
#
def fox_ai():
     global turn, tiger_stage0, gameboard, tiger_position, fox_stage0, count,winner,page, selected_state
     drawGame()
     while page==FOX_AI:
        pg.time.delay(50)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.type == pg.MOUSEBUTTONDOWN:
                    axes = pg.mouse.get_pos()
                    if (turn == TIGER):
                        if (tiger_stage0):
                            idx = check_if_valid_initial(axes)
                            if (idx != INVALID):
                                initial_gameboard[0] = EMPTY
                                tiger_position = idx
                                gameboard[tiger_position] = TIGER
                                tiger_stage0 = False
                                turn = FOX
                        else:
                            idx = tiger_check_if_valid(axes)
                            if (idx != INVALID):
                                gameboard[tiger_position] = EMPTY
                                tiger_position = idx
                                gameboard[tiger_position] = TIGER
                                turn = FOX


        drawGame()
        if (turn == FOX):
            pg.time.delay(1000)
            val = minimax((gameboard, False), DEPTH, FOX)
            random.shuffle(selected_state)
            gameboard = copy.deepcopy(selected_state[0])
            selected_state=[]
            if (fox_stage0):
                count += 1
                initial_gameboard[count] = EMPTY
            if (count > 5):
                fox_stage0 = False
            turn = TIGER

        pg.event.clear()
        if (fox_kill > 2):
            winner = TIGER
            drawGame()
            page=GAME_OVER
        if (is_tiger_trapped()):
            winner = FOX
            drawGame()
            page=GAME_OVER







#

def check_start_page(axes):
    for i in range(3):
        dist= calculateDistance(start_page_points[i],axes)
        if(dist<90):
            return i
    return INVALID
def draw_start_page():
    screen.fill((34, 166, 153))
    pg.draw.circle(screen,(255,255,255),(250+64,200+64),90)
    pg.draw.circle(screen, (255, 255, 255), (550 + 64, 200 + 64), 90)
    pg.draw.circle(screen, (255, 255, 255), (850 + 64, 200 + 64), 90)
    screen.blit(multiplayer_icon,(250,200))
    screen.blit(tiger_start_icon, (550, 200))
    screen.blit(fox_start_icon, (850, 200))
    display_text('Len Choa',tfont,(0,0,0),460,500)
    pg.display.update()


def draw_last_page():
    screen.fill((34, 166, 153))
    if(winner==TIGER):
        display_text("Tiger Wins", tfont, (0,0,0), 460,500)
    else:
        display_text("Fox Wins", tfont, (0, 0, 0), 460, 500)


    display_text("Click to Continue", tfont, (0, 0, 0), 300, 900)

    pg.display.update()




#main game loop:
running= True
while running:
    for event in pg.event.get():
        if event.type ==pg.MOUSEBUTTONDOWN:
            if(page==START_PAGE):
                idx= check_start_page(pg.mouse.get_pos())
                if(idx!=INVALID):
                    if(idx==0):
                        page=MULTI_MODE
                    elif(idx==1):
                        page=FOX_AI

                    else:
                        page=TIGER_AI

            elif(page==GAME_OVER):
                game_setup()


        if event.type == pg.QUIT:
                pg.quit()
                quit()
    if(page==START_PAGE):
        draw_start_page()
    elif(page==MULTI_MODE):
        multiplayer_mode()
        pg.time.delay(1000)
    elif(page==GAME_OVER):
        draw_last_page()
    elif(page==TIGER_AI):
        tiger_ai()
        pg.time.delay(1000)
    elif (page == FOX_AI):
        fox_ai()
        pg.time.delay(1000)




