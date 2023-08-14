import math
import copy


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
nodes.append(Node([3, 5, 9], [4]))
nodes.append(Node([4, 8], [1, 9]))
nodes.append(Node([5, 7, 9], [2]))
nodes.append(Node([6, 8], [3, 7]))

EMPTY = 0
TIGER = 1
FOX = 2
DEPTH = 4
INFINITY = math.inf
fox_live = 6


def heuristic_score(state):
    freespace=0
    killscore=0
    tiger_pos=0
    for i in range(len(state)):
        if (state[i] == TIGER):
            tiger_pos = i
            break;
    for i in nodes[tiger_pos].hop1:
        if (state[i] == EMPTY):
            freespace+=1
    fc=0
    for i in state:
        if(i==FOX):
            fc+=1
    if(fc<fox_live):
        killscore=5
    return killscore+freespace



def find_all_moves(state, type):
    if type == TIGER:
        states = []
        tiger_pos = 0
        for i in range(len(state)):
            if (state[i] == TIGER):
                tiger_pos = i
                break;
        for i in nodes[tiger_pos].hop1:
            if (state[i] == EMPTY):
                st = copy.deepcopy(state)
                st[tiger_pos] = EMPTY
                st[i] = TIGER
                states.append(st)
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
                            states.append(st)

                    elif (distance < 3):
                        if (state[i - 1] == FOX):
                            st = copy.deepcopy(state)
                            st[tiger_pos] = EMPTY
                            st[i] = TIGER
                            st[i - 1] = EMPTY
                            states.append(st)

                else:
                    if (distance > -3):
                        if (state[tiger_pos - 1] == FOX):
                            st = copy.deepcopy(state)
                            st[tiger_pos] = EMPTY
                            st[i] = TIGER
                            st[tiger_pos - 1] = EMPTY
                            states.append(st)

                    elif (distance < -3):
                        if (state[tiger_pos - 3] == FOX):
                            st = copy.deepcopy(state)
                            st[tiger_pos] = EMPTY
                            st[i] = TIGER
                            st[tiger_pos - 3] = EMPTY
                            states.append(st)
        return states
    else:
        states = []
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
                    states.append(st)
        return states



selected_state = []


def minimax(state, depth, type):
    global selected_state
    if depth == 0:
        return heuristic_score(state)
    if type == TIGER:
        maxVal = -INFINITY
        new_states = find_all_moves(state, type)
        for i in new_states:
            val = minimax(i, depth - 1, FOX)
            if (val > maxVal):
                maxVal = val
                selected_state = i
        return maxVal

    else:
        minVal = 5 * (depth + 1)
        jump = False
        fc = 0
        for i in state:
            if (i == FOX):
                fc += 1
        if (fc < fox_live):
            jump = True
        if (jump != True):
            new_states = find_all_moves(state, type)
            for i in new_states:
                val = minimax(i, depth - 1, TIGER)
                if (val < minVal):
                    minVal = val
                    selected_state = i

        return minVal


gameboard = [2, 0, 1, 2, 2, 2, 2, 2, 0, 0]
val= minimax(gameboard,2,TIGER)
print(selected_state)