import pygame
import random

from network import Network

WIDTH, HEIGHT = 800, 600
MAZE_WIDTH, MAZE_HEIGHT = 4, 4
CELL_SIZE = WIDTH // MAZE_WIDTH, HEIGHT // MAZE_HEIGHT
AGENT_COLOR = (255, 0, 0)
GOAL_COLOR = (0, 255, 0)
WALL_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (51, 51, 51)

LEARNING_RATE = 0.1
EXPLORATION_CHANCE = 0.1
DISCOUNT_FACTOR = 0.9

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

maze = [
    [0, 1, 0, 1],
    [0, 0, 0, 1],
    [1, 0, 1, 1],
    [0, 0, 0, 10]
]
agent_position = (0, 0)
goal_position = (MAZE_WIDTH - 1, MAZE_HEIGHT - 1)
q_table = {(x, y) : {action : 0 for action in ['up', 'down', 'left', 'right']} for x in range(MAZE_WIDTH) for y in
           range(MAZE_HEIGHT)}

ACTIONS = ['up', 'down', 'left', 'right']


def q_learning() :
    global agent_position, q_table

    current_state = agent_position
    action = getAction(current_state, q_table)

    new_state = current_state
    if action == 'up' :
        new_state = (current_state[0] - 1, current_state[1])
    elif action == 'down' :
        new_state = (current_state[0] + 1, current_state[1])
    elif action == 'left' :
        new_state = (current_state[0], current_state[1] - 1)
    elif action == 'right' :
        new_state = (current_state[0], current_state[1] + 1)

    reward = 0 if maze[new_state[0]][new_state[1]] == 0 else 100 if new_state == goal_position else -5
    max_future_q = max(q_table[new_state].values())
    current_q = q_table[current_state][action]
    new_q = (reward + DISCOUNT_FACTOR * max_future_q)
    q_table[current_state][action] = new_q

    if new_state != current_state :
        agent_position = new_state


def getAction(current_state, q_table) :
    valid_actions = []
    if current_state[0] > 0 and maze[current_state[0] - 1][current_state[1]] != 1 :
        valid_actions.append('up')
    if current_state[0] < MAZE_HEIGHT - 1 and maze[current_state[0] + 1][current_state[1]] != 1 :
        valid_actions.append('down')
    if current_state[1] > 0 and maze[current_state[0]][current_state[1] - 1] != 1 :
        valid_actions.append('left')
    if current_state[1] < MAZE_WIDTH - 1 and maze[current_state[0]][current_state[1] + 1] != 1 :
        valid_actions.append('right')
    if max(q_table[current_state].values()) == 0 or random.uniform(0, 1) <= EXPLORATION_CHANCE :
        action = random.choice(valid_actions)
    else :
        action = max(q_table[current_state], key=q_table[current_state].get)
    return action


def layout() :
    c = 0
    for i in range(0, HEIGHT, HEIGHT // MAZE_HEIGHT) :
        for j in range(0, WIDTH, WIDTH // MAZE_WIDTH) :
            pygame.draw.rect(win, BACKGROUND_COLOR, (j, i, WIDTH // MAZE_WIDTH, HEIGHT // MAZE_HEIGHT), 0)
            pygame.draw.rect(win, (0, 0, 0) if maze[c // MAZE_WIDTH][c % MAZE_WIDTH] == 1 else (255, 255, 255),
                             (j + 3, i + 3, WIDTH // MAZE_WIDTH - 6, HEIGHT // MAZE_HEIGHT - 6), 0)
            c += 1
    pygame.draw.circle(win, AGENT_COLOR, (agent_position[1] * WIDTH // MAZE_WIDTH + WIDTH // (MAZE_WIDTH * 2),
                                          agent_position[0] * HEIGHT // MAZE_HEIGHT + HEIGHT // (MAZE_HEIGHT * 2)), 30,
                       0)


running = True
clock = pygame.time.Clock()
episode = 0
user_start_position = None
user_input_directions = []
user_input_taken = False

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def reset_to_user_start() :
    global agent_position, user_start_position, user_input_directions
    agent_position = user_start_position
    user_input_directions = []

def read_pos(str):
    str = str.split(",")
    print(str)
    return int(str[0]), int(str[1])


execute_user_action = False
user_action = ['0,0']
n= Network()
best_action = "Random"
start_q_learning = False
count =0
received_data = None
reached = False

while running :
    clock.tick(30)
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

    received_data= n.send(best_action)

    if received_data not in user_action and not reached:
        user_action.clear()
        user_action.append(received_data)
        start_q_learning =True
        user_start_position = read_pos(received_data)
        agent_position = user_start_position
        execute_user_action = True

    # if received_data and not execute_user_action :





    if  start_q_learning:
        q_learning()

    win.fill(BACKGROUND_COLOR)
    layout()




    if agent_position == goal_position :
        episode += 1
        # print(q_table)

        if user_start_position and episode > 10 and user_start_position != goal_position :
            reset_to_user_start()
            print("Reset to user's start position:", user_start_position)

            action = getAction(agent_position, q_table)

            print("Best action to reach the goal from here:", action)
            best_action =action
            user_input_taken = False
            execute_user_action = False
            start_q_learning= False

    if user_start_position == goal_position :
        agent_position = user_start_position
        reached = True
        start_q_learning= False
        font = pygame.font.Font(None, 36)
        text = font.render('Reached Goal!', True, (0, 255, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        rect_width = text_rect.width + 20
        rect_height = text_rect.height + 20

        rect_surface = pygame.Surface((rect_width, rect_height))
        rect_surface.fill((128, 128, 128))

        win.blit(rect_surface, (WIDTH // 2 - rect_width // 2, HEIGHT // 2 - rect_height // 2))
        win.blit(text, text_rect.topleft)


    pygame.display.set_caption(f"Episode: {episode}")
    pygame.display.update()

pygame.quit()
