# Those nice constants

n, m = 27, 27 # size of the game

dx = 20 # Size of a square

y0 = dx * 17 // 15 # size of the top bar

tfx, tfy = m * dx, y0 + n * dx # size of the window


tick_default = 75 # take between each snake movement (in ms)

growth_rate = int((n * m)**0.5/10) # number of square the snake wins by eating an apple

max_count = 0

space = []
for i in range(n):
    space +=[(i, j) for j in range(m)]


in_game_menu = {'Resume' : True, 'Menu': False, 'Quit': False}
in_game_list = list(in_game_menu)

#walls or not, speeding or not
levels = {'Classic.' : (True, False), 'Trump\'s nightmare' : (False, False),
          'Vitamins.' : (True, True), 'Wait, those are not vitamins' : (False, True),
          'Quit': (0, 0)}

level_list = list(levels)