from pygame import *
from parameters2 import *
from snake_display2 import display_game, display_end, display_menu
from save import upload, download
from random import choice
import os


""" A snake is represented by: *a list of the blocks forming his body
                               *an integer indicating where the head is in the list : [*****tail,head****]"""


#======================================================================================================================
# Initialisation
#======================================================================================================================

init()

# the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = "200,40"
display.set_caption("SNAKE")
screen = display.set_mode((tfx, tfy))
icon = image.load("apple.bmp")
display.set_icon(icon)

#=======================================================================================================================
# Snake and apple things
#=======================================================================================================================
class Snake(object):
    def __init__(self, list, head):
        self.list = list
        self.head = head

    def is_dead(self, obstacles=[]):
        sent = False
        pos = self.list[self.head]
        for i in range(len(self.list)):
            if i != self.head and self.list[i] == pos:
                sent = True
        return sent or pos in obstacles

    def update(self, direction, growth):
        i, j = self.list[self.head]

        if direction == "up":
            next = ((i - 1) % n, j)
        elif direction == "down":
            next = ((i + 1) % n, j)
        elif direction == "left":
            next = (i, (j - 1) % m)
        else:
            next = (i, (j + 1) % m)

        if growth > 0:
            self.list.insert(self.head, next)
            return growth - 1
        else:
            self.head = (self.head - 1) % len(self.list)
            self.list[self.head] = next
            return 0

def new_apple(snake, obstacles):
    return choice([a for a in space if a not in snake.list and a not in obstacles])

#=======================================================================================================================
# Auxiliary screens
#=======================================================================================================================


def handle_end():
    dead = True

    while dead:
        display_end(screen)
        eve = event.wait()
        if eve.type == KEYDOWN and eve.key in [K_SPACE, K_RETURN, K_UP]:
            return 0

        elif eve.type == KEYDOWN and eve.key in [K_ESCAPE, K_BACKSPACE]:
            return 1

        elif eve.type == QUIT:
            return -1


def handle_menu(item_list, name):
    global play
    i = 0 # currently selected item
    param = True

    while param:
        display_menu(screen, item_list, name, i)
        eve = event.wait()
        if eve.type == KEYDOWN:
            if eve.key == K_ESCAPE:
                play = False
                param = False

            elif eve.key == K_UP:
                i = (i - 1) % len(item_list)

            elif eve.key == K_DOWN:
                i = (i + 1) % len(item_list)

            elif eve.key == K_SPACE or eve.key == K_RETURN:
                param = False
                return(item_list[i])


        elif eve.type == QUIT:
            play = False
            param = False

    return(item_list[-1])
#=======================================================================================================================
# Main function
#=======================================================================================================================

def main():
    global play, growth, max_count, settings
    play, growth = True, 3 * growth_rate

    level = handle_menu(level_list, "CHOOSE A LEVEL")
    walls_ON, speeding_ON = levels[level]
    if level == 'Quit':
        play = False

    direction = "up"
    snake = Snake([(n // 2, m // 2)], 0)
    walls = [(0, i) for i in range(m)] + [(i, 0) for i in range(1, n)] + \
            [(n - 1, i) for i in range(1, m)] + [(i, m-1) for i in range(1, n - 1)]
    obstacles = walls * walls_ON
    apple = new_apple(snake, obstacles)
    count = 0
    max_count = download(level)
    tick = tick_default
    t0 = time.get_ticks()

    while play:
        display_game(screen, snake, apple, count, max_count, obstacles)

        for eve in event.get(): #directing the snake

            if eve.type == KEYDOWN: # moving the snake
                if eve.key in [K_z, K_UP]:
                    direction = "up"
                elif eve.key in [K_s, K_DOWN]:
                    direction = "down"
                elif eve.key in [K_q, K_LEFT]:
                    direction = "left"
                elif eve.key in [K_d, K_RIGHT]:
                    direction = "right"

                elif eve.key in [K_SPACE, K_ESCAPE]:
                    choice = handle_menu(in_game_list, "PAUSE")
                    if choice == 'Menu':
                        upload(level, max_count)
                        main()
                    elif choice == 'Quit':
                        upload(level, max_count)
                        play = False

            elif eve.type == QUIT :
                play = False

        if snake.list[snake.head] == apple: # eating the apple
            growth += growth_rate
            apple = new_apple(snake, obstacles)
            count += 1
            tick -= tick/20 * speeding_ON

        if count > max_count: # keeping track of the best count yet
            max_count = count

        if time.get_ticks() - t0 > tick: # time to move the snake
            growth = snake.update(direction, growth)
            t0 = time.get_ticks()

        if snake.is_dead(obstacles):
            i = handle_end()
            if i == 0: #on recommence une partie
                direction = "up"
                snake = Snake([(n // 2, m // 2)], 0)
                apple = new_apple(snake, obstacles)
                count = 0
                tick = tick_default
                t0 = time.get_ticks()

            if i == -1: #fenêtre fermée
                upload(level, max_count)
                play = False

            if i == 1: #retour menu
                upload(level, max_count)
                main()
    quit()





if __name__ == '__main__':
    main()


