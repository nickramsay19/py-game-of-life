# Import and initialize the pygame library
import pygame
import math
pygame.init()

# Set up the drawing window
screen_width, screen_height = 700, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Conway\'s Game of Life')

# setup grid
view_size = 50
grid = [ [ False for x in range(0, view_size) ] for y in range(0, view_size)]

# setup button press timer for double click prevention
click_timer = 0

# define the conway function
def conway(g):
    
    # generate a hard copy of g
    new = [ [ cell for cell in row ] for row in g ]
    
    for x, row in enumerate(g):
        for y, cell in enumerate(row):

            # count alive adjacent
            alive = 0
            
            for pos in [(-1,-1), (-1,0), (-1,1), (1,-1), (1,0), (1,1), (0,-1), (0,1)]:
                try:
                    if g[x + pos[0]][y + pos[1]]: alive += 1
                except: pass
            
            # make changes
            if cell == 1:
                if alive <= 1: # starvation
                    new[x][y] = False
                elif alive >= 4: # overpopulation
                    new[x][y] = False
            else:
                if alive == 3: # reproduction
                    new[x][y] = True
    return new

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                grid = conway(grid)
    
    # Fill the background with white
    screen.fill((50, 50, 50))      
      
    # check mouse input
    if pygame.mouse.get_pressed()[0] == 1 and click_timer == 0:
        pos = pygame.mouse.get_pos()
        
        cell = (math.ceil(int(view_size * pos[0] / screen_width)), math.ceil(int(view_size * pos[1] / screen_height)))
        
        grid[cell[0]][cell[1]] = not grid[cell[0]][cell[1]]
        
        click_timer = 10
    elif click_timer > 0:
        click_timer -= 1
        
    # draw gridlines
    for i in range(0, view_size):
        pygame.draw.line(screen, (40,40,40), (i * int(screen_width / view_size), 0), (i * int(screen_width / view_size), screen_height))
        pygame.draw.line(screen, (40,40,40), (0, i * int(screen_height / view_size)), (screen_height, i * int(screen_height / view_size)))
    
    # draw cells
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (200,200,200), 
                                 (
                                     x * int(screen_width / view_size) + 1,
                                     y * int(screen_height / view_size) + 1,
                                     int(screen_width / view_size) - 1,
                                     int(screen_width / view_size) - 1
                                 ))
    

    # Flip the display
    pygame.display.update()

# Done! Time to quit.
pygame.quit()