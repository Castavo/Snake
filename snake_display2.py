from pygame import font, draw, display, image, transform
from parameters import *

#=======================================================================================================================
# Colors and fonts
#=======================================================================================================================

noir, gris_clair, gris = (0, 0, 0), (230, 230, 230), (150, 150, 150)
rouge, vert_fonce, vert_clair, vert_fluo = (150, 0, 0), (0, 50, 0), (50, 100, 50), (0, 150, 0)

font.init()
arial = font.SysFont("arial", dx, bold = True)
medium_arial = font.SysFont("arial", dx * 3 // 2, bold = True)
big_arial = font.SysFont("arial", 2 * dx, bold = True)
huge_arial = font.SysFont("arial", 3 * dx, bold = True)

apple = transform.scale(image.load("apple.bmp"), (dx, dx))

#=======================================================================================================================
# Snake
#=======================================================================================================================

def display_body_part(screen, pos, ddx):
    i, j = pos
    x, y = j * dx, i * dx + ddx + y0
    draw.rect(screen, vert_fonce, (x, y, dx, dx))
    draw.rect(screen, vert_clair, (x, y, dx, dx), 2)

def display_tail(screen, tail, antecedent):
    i, j = tail
    k, l = antecedent
    u, v = k - i, l - j
    if abs(v) > 1:
        v = -v/abs(v)
    elif abs(u) > 1:
        u = -u/abs(u)
    if u + v > 0:
        i, j = k, l
    a, b = i + abs(v), j + abs(u)
    c, d = (i + a)/2 - u*0.8, (j + b)/2 - v*0.8
    draw.polygon(screen, vert_fonce, [(j * dx + abs(u), i * dx + y0 + abs(v)), (b * dx - abs(u), a * dx + y0 - abs(v)),
                                      (d * dx, c * dx + y0)])
    draw.polygon(screen, vert_clair, [(j * dx + abs(u), i * dx + y0 + abs(v)), (b * dx - abs(u), a * dx + y0 - abs(v)),
                                      (d * dx, c * dx + y0)], 3)

def display_head(screen, head, antecedent, ddx = 0):
    i, j = head
    x, y = j * dx, i * dx + ddx + y0
    draw.rect(screen, vert_fonce, (x, y, dx, dx))
    draw.rect(screen, vert_clair, (x, y, dx, dx), 2)

    k, l = antecedent
    u, v = k - i, l - j
    if abs(v) > 1:
        v = -v/abs(v)
    elif abs(u) > 1:
        u = -u/abs(u)
    if u + v < 0:
        u, v = abs(u), abs(v)
        y += dx//2 * u
        x += dx//2 * v
    draw.rect(screen, vert_fluo, (x + dx//4*v + dx//3*u, y + dx//4*u + dx//3*v, 2, 2))
    draw.rect(screen, vert_fluo, (x + dx//4*v + 2*dx//3*u, y + dx//4*u + 2*dx//3*v, 2, 2))

#=======================================================================================================================
# Obstacles and apple
#=======================================================================================================================

def display_obstacles(screen, obstacles):
    for (i, j) in obstacles:
        draw.rect(screen, gris, (j * dx + 2, i * dx + 2 + y0, dx - 4, dx - 4))
        draw.rect(screen, noir, (j * dx + 2, i * dx + 2 + y0, dx - 4, dx - 4), 2)

def display_apple(screen, i, j):
    screen.blit(apple,(j * dx, i * dx + y0))
    # draw.rect(screen, rouge, (j * dx + 2, i * dx + y0 + 2, dx - 4, dx - 4))


#=======================================================================================================================
# Whole game
#=======================================================================================================================


def display_upper_bar(screen, count, max_count):
    draw.rect(screen, gris, (0, 0, tfx, y0))

    message = "Apple count : " + str(count)
    screen.blit(arial.render(message, True, noir), (0, 0))

    message = "High Score : "
    tx, _ = arial.size(message + "00")
    screen.blit(arial.render(message + str(max_count), True, noir), (tfx - tx, 0))


def display_game(screen, snake, apple, count, max_count, obstacles=[], ddx = 0):
    # the background
    draw.rect(screen, gris_clair, (0, 0, tfx, tfy))
    display_upper_bar(screen, count, max_count)

    # obstacles
    display_obstacles(screen, obstacles)

    # the apple
    display_apple(screen, apple[0], apple[1])

    # the snake
    u = len(snake.list)
    if u == 1: # too short for a tail or a head
        display_body_part(screen, snake.list[0], ddx)
    else:
        for i in range(1, u - 1):
            display_body_part(screen, snake.list[(snake.head + i) % u], ddx)
        display_tail(screen, snake.list[snake.head - 1], snake.list[snake.head - 2])
        display_head(screen, snake.list[snake.head], snake.list[(snake.head + 1) % u])

    display.flip()

#=======================================================================================================================
# Auxiliary screens
#=======================================================================================================================

def display_end(screen):
    message = "YOU DIED"
    tx, ty = huge_arial.size(message)
    text2 = "Press [Enter] or [Space] to try again"
    tx2, ty2 = arial.size(text2)
    text3 = "Press [Escape] or [Return] to return to menu"
    tx3, ty3 = arial.size(text3)

    screen.blit(huge_arial.render(message, True, noir), ((tfx - tx) / 2, (tfy - ty - ty2) / 2))
    screen.blit(arial.render(text2, True, noir), ((tfx - tx2) / 2, (tfy + ty - ty2) / 2))
    screen.blit(arial.render(text3, True, noir), ((tfx - tx3) / 2, (tfy + ty + ty2) / 2))
    display.flip()


def display_menu(screen, item_list, name, i):
    n = len(item_list)
    dy = tfy // (n + 1)

    draw.rect(screen, gris_clair, (0, 0, tfx, tfy))
    draw.rect(screen, gris, (0, (2*i + 3) * dy // 2, tfx, int(2.6 * dx)))
    tx, ty = big_arial.size(name)
    screen.blit(big_arial.render(name, True, vert_fonce), ((tfx - tx) / 2, dy // 2))
    for k in range(0, n - 1):
        text = item_list[k]
        tx, ty = medium_arial.size(text)
        screen.blit(medium_arial.render(text, True, vert_clair), ((tfx - tx) / 2, (2 * k + 3) * dy // 2))
    text = 'Quit'
    tx, ty = medium_arial.size(text)
    screen.blit(medium_arial.render(text, True, vert_fonce), ((tfx - tx) / 2, (2 * k + 5) * dy // 2))

    display.flip()
