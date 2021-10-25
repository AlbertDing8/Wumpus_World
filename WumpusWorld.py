import pygame
import os
import random

pygame.init()
pygame.display.init()

# Constants
MULTIPLIER = 2.0
WIDTH, HEIGHT = 170 * MULTIPLIER, 210 * MULTIPLIER
TOP = 43 * MULTIPLIER
BORDER = 3 * MULTIPLIER
UNIT = 32 * MULTIPLIER
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus World")

background = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'Game_Board.png')))
blank_block = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'Blank_Block.png')))
pit_block = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'Pit_Block.png')))
char = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'Player.png')))
wumpus = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'Wumpus.png')))
smelly_block = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'Smelly.png')))
windy_block = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'Windy.png')))
gold = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'Gold.png')))

pygame.mixer.music.load('Main WW Theme.wav')
pygame.mixer.music.set_volume(0.25)

GAME_QUIT = pygame.USEREVENT + 1


# Player Class
class Player:
    def __init__(self):
        self.curr_x = 0
        self.curr_y = 0
        self.visited = {0: [True, False, False, False, False],
                        1: [False, False, False, False, False],
                        2: [False, False, False, False, False],
                        3: [False, False, False, False, False],
                        4: [False, False, False, False, False]}
        self.alive = True
        self.gold = False


class GameBoard:
    def __init__(self):
        self.image = blank_block
        self.pit = False
        self.wumpus = False
        self.smelly = False
        self.windy = False
        self.gold = False

    def is_pit(self):
        self.image = pit_block
        self.pit = True

    def is_wumpus(self):
        self.wumpus = True

    def is_smelly(self):
        self.smelly = True

    def is_windy(self):
        self.windy = True

    def is_gold(self):
        self.gold = True


# Initialize game and map generation
def game_initialization():
    h = []
    for i in range(5):
        ele = []
        for j in range(5):
            ele.append(GameBoard())
        h.append(ele)

    # Generate Pits
    for i in range(3):
        pit_x, pit_y = random.randint(1, 4), random.randint(1, 4)
        run = True
        while run:
            if not h[pit_x][pit_y].pit:
                h[pit_x][pit_y].is_pit()
                if (pit_x - 1) >= 0:
                    h[pit_x - 1][pit_y].is_windy()
                if (pit_x + 1) <= 4:
                    h[pit_x + 1][pit_y].is_windy()
                if (pit_y - 1) >= 0:
                    h[pit_x][pit_y - 1].is_windy()
                if (pit_y + 1) <= 4:
                    h[pit_x][pit_y + 1].is_windy()
                run = False
            else:
                pit_x, pit_y = random.randint(1, 4), random.randint(1, 4)

    # Place Wumpus
    w_x, w_y = random.randint(1, 4), random.randint(1, 4)
    run = True
    while run:
        if not h[w_x][w_y].pit:
            h[w_x][w_y].is_wumpus()
            if (w_x - 1) >= 0:
                h[w_x - 1][w_y].is_smelly()
            if (w_x + 1) <= 4:
                h[w_x + 1][w_y].is_smelly()
            if (w_y - 1) >= 0:
                h[w_x][w_y - 1].is_smelly()
            if (w_y + 1) <= 4:
                h[w_x][w_y + 1].is_smelly()
            run = False
        else:
            w_x, w_y = random.randint(1, 4), random.randint(1, 4)

    # Place Gold
    g_x, g_y = random.randint(1, 4), random.randint(1, 4)
    run = True
    while run:
        if h[g_x][g_y].pit or h[g_x][g_y].wumpus:
            g_x, g_y = random.randint(1, 4), random.randint(1, 4)
        else:
            h[g_x][g_y].is_gold()
            run = False

    return h


# Display Game
def game(p, h):
    screen.blit(background, (0, 0))
    for i in range(5):
        for j in range(5):
            if p.visited[i][j]:
                screen.blit(h[i][j].image, (BORDER + (i * (UNIT + MULTIPLIER)),
                                            TOP + ((4 - j) * (UNIT + MULTIPLIER))))
                if h[i][j].smelly:
                    screen.blit(smelly_block, (BORDER + (i * (UNIT + MULTIPLIER)),
                                               TOP + ((4 - j) * (UNIT + MULTIPLIER))))
                if h[i][j].windy:
                    screen.blit(windy_block, (BORDER + (i * (UNIT + MULTIPLIER)),
                                              TOP + ((4 - j) * (UNIT + MULTIPLIER))))
                if h[i][j].pit:
                    p.alive = False
                if h[i][j].wumpus:
                    screen.blit(wumpus, (BORDER + (i * (UNIT + MULTIPLIER)),
                                         TOP + ((4 - j) * (UNIT + MULTIPLIER))))
                    p.alive = False
                if h[i][j].gold and not p.gold:
                    screen.blit(gold, (BORDER + (i * (UNIT + MULTIPLIER)),
                                       TOP + ((4 - j) * (UNIT + MULTIPLIER))))

    if p.alive:
        screen.blit(char, (BORDER + (p.curr_x * (UNIT + MULTIPLIER)), TOP + ((4 - p.curr_y) * (UNIT + MULTIPLIER))))

    pygame.display.update()


# Player died
def death():
    pygame.time.wait(2000)
    pygame.event.post(pygame.event.Event(GAME_QUIT))


# Main Function
def main():
    pygame.mixer.music.play()

    # Generate Map
    hidden = game_initialization()

    # define a variable to control the main loop
    running = True

    # Creating clock class
    clock = pygame.time.Clock()

    p = Player()

    game(p, hidden)

    # main loop
    while running:
        # Prevents obscene amounts of game window refreshing
        clock.tick(FPS)

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT or event.type == GAME_QUIT:
                # exit game
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if p.curr_y < 4:
                        p.curr_y += 1
                        p.visited[p.curr_x][p.curr_y] = True
                elif event.key == pygame.K_DOWN:
                    if p.curr_y > 0:
                        p.curr_y -= 1
                        p.visited[p.curr_x][p.curr_y] = True
                elif event.key == pygame.K_LEFT:
                    if p.curr_x > 0:
                        p.curr_x -= 1
                        p.visited[p.curr_x][p.curr_y] = True
                elif event.key == pygame.K_RIGHT:
                    if p.curr_x < 4:
                        p.curr_x += 1
                        p.visited[p.curr_x][p.curr_y] = True
                elif event.key == pygame.K_SPACE:
                    if hidden[p.curr_x][p.curr_y].gold:
                        p.gold = True
                    if p.curr_x == 0 and p.curr_y == 0 and p.gold:
                        main()

        game(p, hidden)

        # Check to see if player is alive
        if not p.alive:
            death()

    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
