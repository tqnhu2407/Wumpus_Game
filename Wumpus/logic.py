import random

'''
obj is a list having 3 elements:
obj[0] = 
    1: visited
    0: not visited
obj[1] = 
    0: no object
    1: gold
    2: pit
    3: wumpus
    4: door
obj[2] = (signals)
    0: no signal
    1: breeze
    2: stench
    3: breeze and stench
'''

VISITED = 1
NOT_VISITED = 0

NO_OBJ = 0
GOLD = 1
PIT = 2
WUMPUS = 3
DOOR = 4

NO_SIGNAL = 0
BREEZE = 1
STENCH = 2
BREEZE_STENCH = 3

B, S, P, W, visited = [], [], [], [], []

def print_obj(rooms, x, y):
    curr_room = rooms[x][y]
    print(f'Room ({x}, {y})')
    for i in range(len(curr_room)):
        print(curr_room[i])


def init_KB():
    
    global B, S, P, W, visited
    B, S, P, W, visited = [], [], [], [], []
    for i in range(10):
        B.append([])
        S.append([])
        P.append([])
        W.append([])
        visited.append([])
        for j in range(10):
            B[i].append('UNK')
            S[i].append('UNK')
            P[i].append('UNK')
            W[i].append('UNK')
            visited[i].append(False)


def update_KB(rooms, x, y):
    
    print('')
    print(f'The Agent is in room({y+ 1}, {10 - x})')
    
    global B, S, P, W, visited
    curr_room = rooms[x][y]
    visited[x][y] = True
    
    if curr_room[1] == GOLD:
        print('There is a GOLD here!')
    
    if curr_room[1] == PIT:
        print('There is a Pit here')
        P[x][y] = 'TRUE'
        return
    elif curr_room[1] != PIT:
        P[x][y] = 'FALSE'
     
    if curr_room[1] == WUMPUS:
        print('There is a Wumpus here')
        W[x][y] = 'TRUE'
        return
    elif curr_room[1] != WUMPUS:
        W[x][y] = 'FALSE'
    
    if curr_room[1] == NO_OBJ or curr_room[1] == DOOR:
        P[x][y] = 'FALSE'
        W[x][y] = 'FALSE'
    
    if curr_room[2] == NO_SIGNAL:
        print('There is no Breeze or Stench here')
        B[x][y] = 'FALSE'
        S[x][y] = 'FALSE'
    
    if curr_room[2] == BREEZE:
        print('There is Breeze here')
        B[x][y] = 'TRUE'
        S[x][y] = 'FALSE'
        if is_a_room(x, y-1) and P[x][y - 1] == 'UNK': # left
            P[x][y - 1] = 'MAYBE'
        if is_a_room(x, y+1) and P[x][y + 1] == 'UNK': # right
            P[x][y + 1] = 'MAYBE'
        if is_a_room(x-1, y) and P[x - 1][y] == 'UNK': # up
            P[x - 1][y] = 'MAYBE'
        if is_a_room(x+1, y) and P[x + 1][y] == 'UNK': # down
            P[x + 1][y] = 'MAYBE'
        
    if curr_room[2] == STENCH:
        print('There is Stench here')
        S[x][y] = 'TRUE'
        B[x][y] = 'FALSE'
        if is_a_room(x, y-1) and W[x][y - 1] == 'UNK': # left
            W[x][y - 1] = 'MAYBE'
        if is_a_room(x, y+1) and W[x][y + 1] == 'UNK': # right
            W[x][y + 1] = 'MAYBE'
        if is_a_room(x-1, y) and W[x - 1][y] == 'UNK': # up
            W[x - 1][y] = 'MAYBE'
        if is_a_room(x+1, y) and W[x + 1][y] == 'UNK': # down       
            W[x + 1][y] = 'MAYBE'
    
    if curr_room[2] == BREEZE_STENCH:
        print('There are both Breeze and Stench here')
        B[x][y] = 'TRUE'
        S[x][y] = 'TRUE'
        if is_a_room(x, y-1) and P[x][y - 1] == 'UNK': # left
            P[x][y - 1] = 'MAYBE'
        if is_a_room(x, y+1) and P[x][y + 1] == 'UNK': # right
            P[x][y + 1] = 'MAYBE'
        if is_a_room(x-1, y) and P[x - 1][y] == 'UNK': # up
            P[x - 1][y] = 'MAYBE'
        if is_a_room(x+1, y) and P[x + 1][y] == 'UNK': # down
            P[x + 1][y] = 'MAYBE'
        if is_a_room(x, y-1) and W[x][y - 1] == 'UNK': # left
            W[x][y - 1] = 'MAYBE'
        if is_a_room(x, y+1) and W[x][y + 1] == 'UNK': # right
            W[x][y + 1] = 'MAYBE'
        if is_a_room(x-1, y) and W[x - 1][y] == 'UNK': # up
            W[x - 1][y] = 'MAYBE'
        if is_a_room(x+1, y) and W[x + 1][y] == 'UNK': # down       
            W[x + 1][y] = 'MAYBE'


def is_a_room(x, y): 
    '''
    Check if this room is not out of map
    '''
    if x >= 0 and x <= 9 and y >= 0 and y <= 9:
        return True
    return False


def update_dir(rooms, x, y): # Check the current position and infer the next room to go
    
    global B, S, P, W, visited
    update_KB(rooms, x, y)
    curr_room = rooms[x][y]
    '''
    Choose which room to go
    '''
    new_dir = 'UP' # defauld :D

    if curr_room[2] != NO_SIGNAL: # Have a signal
        new_dir = find_nearest_saferoom(rooms, x, y)
    elif is_saferoom(x, y): # If this room is already safe
        new_dir = find_nearest_unkroom(rooms, x, y)
    print(f'Action: {new_dir}')
    return new_dir


def find_nearest_saferoom(rooms, x, y):
    '''
    Check if there is still a safe room to go
    '''
    if is_a_room(x-1, y) and is_saferoom(x-1, y):
        return 'UP'
    if is_a_room(x+1, y) and is_saferoom(x+1, y):
        return 'DOWN'
    if is_a_room(x, y-1) and is_saferoom(x, y-1):
        return 'LEFT'
    if is_a_room(x, y+1) and is_saferoom(x, y+1):
        return 'RIGHT'


def is_saferoom(x, y):

    global B, S, P, W, visited
    if visited[x][y] and W[x][y] == 'FALSE' and P[x][y] == 'FALSE' and B[x][y] == 'FALSE' and S[x][y] == 'FALSE':
        return True
    return False


def find_nearest_unkroom(rooms, x, y):
    '''    
    Apply BFS to find the nearest unknown room to explore
    If we can't find an unknown room
    -> Return to the door to save life
    '''
    path = []
    frontier = [[x, y]]
    explored = []
    for i in range(10):
        explored.append([])
        for j in range(10):
            explored[i].append(False)
            
    start_room = [x, y]
    target_unkroom = []
    
    while frontier:
    
        curr_room = frontier.pop(0)
        explored[curr_room[0]][curr_room[1]] = True
        
        if is_unkroom(curr_room[0], curr_room[1]): # Found an unk room
            target_unkroom = [curr_room[0], curr_room[1]]
            break
        else:
            surrounding_rooms = [[-1, 0], [0, -1], [1, 0], [0, 1]] # U, L, D, R
            for s in surrounding_rooms:
                
                temp_x, temp_y = curr_room[0] + s[0], curr_room[1] + s[1]
                # If the surrounding room is safe or unknown
                if is_a_room(temp_x, temp_y) and not explored[temp_x][temp_y]:
                    if is_saferoom(temp_x, temp_y) or is_unkroom(temp_x, temp_y):
                        next_room = [temp_x, temp_y]
                        frontier.append(next_room)
                        path.append({
                            'Current': curr_room,
                            'Next': next_room
                        })
    
    path_found = [target_unkroom]
    if not target_unkroom:
        path_found = find_way_out(rooms, x, y)
        if len(path_found) == 1:
            return 'ENTER'
    else:
        while target_unkroom != start_room:
            for step in path:
                if step['Next'] == target_unkroom:
                    target_unkroom = step['Current']
                    path_found.insert(0, target_unkroom)
    
    if len(path_found) == 1:
        decided_next_room = path_found[0]
    else:
        decided_next_room = path_found[1] # Because path[0] is the start_room
    
    if start_room[0]-1 == decided_next_room[0] and start_room[1] == decided_next_room[1]:
        return 'UP'
    if start_room[0]+1 == decided_next_room[0] and start_room[1] == decided_next_room[1]:
        return 'DOWN'
    if start_room[0] == decided_next_room[0] and start_room[1]-1 == decided_next_room[1]:
        return 'LEFT'
    if start_room[0] == decided_next_room[0] and start_room[1]+1 == decided_next_room[1]:
        return 'RIGHT'


def is_unkroom(x, y):
    global B, S, P, W, visited
    if not visited[x][y] and W[x][y] == 'UNK' and P[x][y] == 'UNK' and B[x][y] == 'UNK' and S[x][y] == 'UNK':
        return True
    return False


def find_way_out(rooms, x, y):
    
    door = []
    for i in range(10):
        for j in range(10):
            if rooms[i][j][1] == 4:
                door = [i, j]
    
    path = []
    frontier = [[x, y]]
    explored = []
    for i in range(10):
        explored.append([])
        for j in range(10):
            explored[i].append(False)
    start_room = [x, y]
    
    while frontier:
    
        curr_room = frontier.pop(0)
        explored[curr_room[0]][curr_room[1]] = True
        
        if curr_room == door: # Found the door
            break
        else:
            surrounding_rooms = [[-1, 0], [0, -1], [1, 0], [0, 1]] # U, L, D, R
            for s in surrounding_rooms:
                
                temp_x, temp_y = curr_room[0] + s[0], curr_room[1] + s[1]
                # If the surrounding room is safe (visited)
                if is_a_room(temp_x, temp_y) and not explored[temp_x][temp_y]:
                    if is_saferoom(temp_x, temp_y):
                        next_room = [temp_x, temp_y]
                        frontier.append(next_room)
                        path.append({
                            'Current': curr_room,
                            'Next': next_room
                        })
    
    path_found = [door]
    while door != start_room:
        for step in path:
            if step['Next'] == door:
                door = step['Current']
                path_found.insert(0, door)
    
    return path_found







