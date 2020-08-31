# Wumpus_Game
My AI project 02

## Main Features

Find unknown rooms to explore

If the agent see any signal (B, S, BS)

-> Find the nearest safe room

If the room is already safe

-> Choose an unknown room to explore

When go to the golden room

-> Pick the gold immediately

## Advanced Features

Use BFS to find the nearest unknown room to explore

If there is out of possible room:

-> Use BFS to find the shortest way to escape to save life

## Bugs list

When the agent accidentally goes through the door, the game auto win

-> FIXED by check 'ENTER'

When finished a map then choose replay, the KB remains the same as the first map -> The game acts cool

-> FIXED by init_KB when select a new map at the map_selection_menu()

# TODO list

Shoot arrow feature

Update the KB of a specific room to decide whether that room is safe or not
