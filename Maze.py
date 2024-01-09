import pygame

WIDTH, HEIGHT = 800, 600
MAZE_WIDTH, MAZE_HEIGHT = 8, 8
BACKGROUND_COLOR = (51, 51, 51)
AGENT_COLOR = (255, 0, 0)
WALL_COLOR = (0, 0, 0)
CELL_SIZE = WIDTH // MAZE_WIDTH, HEIGHT // MAZE_HEIGHT


pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

maze = [
    [0, 1, 0, 1],
    [0, 0, 0, 1],
    [1, 0, 1, 1],
    [0, 0, 0, 10]
]


agent_position = [0, 0]
goal_position = [MAZE_WIDTH - 1, MAZE_HEIGHT - 1]

def layout():
    c = 0
    for i in range(0, HEIGHT, HEIGHT // MAZE_HEIGHT):
        for j in range(0, WIDTH, WIDTH // MAZE_WIDTH):
            pygame.draw.rect(win, BACKGROUND_COLOR, (j, i, WIDTH // MAZE_WIDTH, HEIGHT // MAZE_HEIGHT), 0)
            color = WALL_COLOR if maze[c // (MAZE_WIDTH) ][c % (MAZE_WIDTH)] == 1 else (255, 255, 255)
            pygame.draw.rect(win, color, (j + 3, i + 3, WIDTH // MAZE_WIDTH - 6, HEIGHT // MAZE_HEIGHT - 6), 0)
            c += 1
    pygame.draw.circle(
        win,
        AGENT_COLOR,
        (
            agent_position[1] * CELL_SIZE[0] + CELL_SIZE[0] // 2,
            agent_position[0] * CELL_SIZE[1] + CELL_SIZE[1] // 2
        ),
        min(CELL_SIZE) // 3,
        0
    )


running = True
clock = pygame.time.Clock()
reached_goal = False

while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not reached_goal and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and agent_position[0] > 0 and maze[agent_position[0] - 1][agent_position[1]] != 1:
                agent_position[0] -= 1
            elif event.key == pygame.K_DOWN and agent_position[0] < MAZE_HEIGHT - 1 and maze[agent_position[0] + 1][agent_position[1]] != 1:
                agent_position[0] += 1
            elif event.key == pygame.K_LEFT and agent_position[1] > 0 and maze[agent_position[0]][agent_position[1] - 1] != 1:
                agent_position[1] -= 1
            elif event.key == pygame.K_RIGHT and agent_position[1] < MAZE_WIDTH - 1 and maze[agent_position[0]][agent_position[1] + 1] != 1:
                agent_position[1] += 1


    layout()
    if agent_position == goal_position:
        font = pygame.font.Font(None, 36)
        text = font.render('Reached Goal!', True, (0, 255, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        rect_width = text_rect.width + 20
        rect_height = text_rect.height + 20

        rect_surface = pygame.Surface((rect_width, rect_height))
        rect_surface.fill((128, 128, 128))

        win.blit(rect_surface, (WIDTH // 2 - rect_width // 2, HEIGHT // 2 - rect_height // 2))
        win.blit(text, text_rect.topleft)

        reached_goal = True


    pygame.display.update()


pygame.quit()
