import pygame as pg, sys, random


def draw_bg(): 
    screen.blit(bg_surface, (bg_x_pos, 0))
    screen.blit(bg_surface, (bg_x_pos + 699, 0)) #duplicates the image and puts it on the right side of screen

def create_plat(): 
    random_plat_height = random.choice(plat_height) #picks a random height number from list (for location of platform)
    new_plat = platform.get_rect(midtop = (plat_width, random_plat_height)) #spawns new platforms with specified width and height
    return new_plat

def move_plats_easy(plats): 
    for plat in plats:
        plat.centerx -= 5 #controls speed of the platform movement towards player in easy mode
    return plats

def move_plats_hard(plats): 
    for plat in plats:
        plat.centerx -= 10 #controls speed of the platform movement towards player in hard mode
    return plats

def draw_plats(plats): 
    if easy_mode:
        for plat in plats:
            screen.blit(platform,plat) #projects new platforms on the screen
    if hard_mode:
        for plat in plats:
            screen.blit(platform2,plat) #projects new platforms on the screen

def check_collision(plats):
    for plat in plats:
        if runner_rect.colliderect(plat):
            return False #ends the game if a collision is made with a platform
    if runner_rect.top <= -100 or  runner_rect.bottom >= 430:
        return False #ends the game if a collision is made with the top or bottom of the screen
    return True #continues the game if there are no collisions

def rotate_runner(runner): 
    new_runner = pg.transform.rotozoom(runner,-runner_movement*3, 1) #rotates the bunny/runner as it moves (to show falling/jumping)
    return new_runner

def runner_animation(): 
    new_runner = runner_frames[runner_index]
    new_runner_rect = new_runner.get_rect(center = (200, runner_rect.centery)) #controls where runner spawns
    return new_runner,new_runner_rect

def score_board(game_state):
    if game_state == 'game_running':
        score_surface = game_text.render('Score: '+str(int(score_number)), True, (255, 255, 255)) #to show scoreboard when game running
        score_rect = score_surface.get_rect(topleft= (25, 15))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_text.render('Score: '+str(int(score_number)), True, (255, 255, 255)) #to show scoreboard when game over as well
        score_rect = score_surface.get_rect(topleft= (25, 15))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_text.render('High Score: '+str(int(high_score)), True, (255, 255, 255)) #to show high score
        high_score_rect = high_score_surface.get_rect(topleft= (525, 15))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score_number, high_score): 
    if score_number > high_score:
        high_score = score_number #updates high score when score is higher than the current high score
    return high_score


#initialising the game, mixer, screen, and text font 
pg.init()
pg.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512) #initialises mixer, default values from pygame docs
screen = pg.display.set_mode((700, 410)) #screen size
pg.display.set_caption('Bunny Run')
clock = pg.time.Clock()
game_text = pg.font.Font('Cloude_Regular_1.02.ttf',60) #initialises font


#game variables
gravity = 0.15
runner_movement = 0
start_menu = True
easy_mode = False
hard_mode = False
game_active = False
score_number = 0
high_score = 0
x_count = 0

#backgrounds
start_menu_bg = pg.image.load('img/startmenu.png').convert()
options = pg.image.load('img/options.png').convert_alpha() #convert_alpha() for smoother running + retain image transparency
bg_surface = pg.image.load('img/bg4.png').convert() #convert() to help with smoother game running
bg_x_pos = 0

#different images of runner to loop through
runner_down = pg.image.load('img/rabbit_down.png').convert_alpha()
runner_normal = pg.image.load('img/rabbit_normal.png').convert_alpha()
runner_up = pg.image.load('img/rabbit_up.png').convert_alpha()
runner_frames = [runner_down, runner_normal, runner_up] #list of different images
runner_index = 0
runner = runner_frames[runner_index]
runner_rect = runner.get_rect(center = (200,150)) #where runner/bunny spawns

runner_img = pg.USEREVENT + 1 #moves through the runner images
pg.time.set_timer(runner_img, 200) #timer for how long between each runner image

platform = pg.image.load('img/plat1.png').convert_alpha()
platform2 = pg.image.load('img/plat2.png').convert_alpha()
platform_list = []
SPAWNPLATFORM = pg.USEREVENT
pg.time.set_timer(SPAWNPLATFORM, 1200)
plat_height = [50, 100, 150, 175, 200, 225, 240, 250, 275, 280, 300] #different heights for the platforms to spawn at
plat_width = 710 #what width the platform spawns at

#game over screen
game_over_screen = pg.image.load('img/gameover.png').convert_alpha()
game_over_rect = game_over_screen.get_rect(topleft = (0,0))

#game music
pg.mixer.music.load('retro_funk.mp3')
pg.mixer.music.set_volume(0.2) #lowers the volume
pg.mixer.music.play()

#while the program is running
while True:
    for event in pg.event.get(): 
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN: #for addition of start menu and easy/hard modes
            if event.key == pg.K_e and start_menu:  #starts the easy game when space is pressed
                start_menu = False
                game_active = True
                easy_mode = True
            elif event.key == pg.K_h and start_menu:  #starts the hard game when space is pressed
                start_menu = False
                game_active = True
                hard_mode = True

        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_SPACE and game_active: #movement of runner while game is active
                runner_movement = 0 #sets runner movement at 0
                runner_movement -= 6 #how high the runner/bunny jumps
            if event.key == pg.K_RETURN and not game_active: #restarts game when game is not active
                game_active = True
                platform_list.clear()
                runner_rect.center = (200,150)
                runner_movement = 0
                score_number = 0

        if event.type == SPAWNPLATFORM: #adds new platforms on a loop
            platform_list.append(create_plat())

        if event.type == runner_img: #loops through the list of different runner images
            if runner_index < 2:
                runner_index += 1
            else:
                runner_index = 0
            runner,runner_rect = runner_animation()

        if event.type == pg.KEYDOWN: #addition of x_count to track how many times x is pressed
            if event.key == pg.K_x: #to pause/unpause the music when x is pressed
                x_count =x_count + 1
                if x_count%2 == 0 :
                    pg.mixer.music.unpause()
                if x_count%2 == 1:
                    pg.mixer.music.pause()

            if event.key == pg.K_ESCAPE: #to quit the game when escape is pressed
                pg.quit()
                sys.exit()


    bg_x_pos -= 1 #moves the bg as a parallax background
    draw_bg()
    if bg_x_pos <= -699: #resets image position for continuous bg movement
        bg_x_pos = 0

    if start_menu: #shows the start menu
        screen.blit(start_menu_bg, (0,0))

    elif start_menu == False: #When the player starts the game
        if game_active: 

            #runner/bunny
            runner_movement += gravity
            rotated_runner = rotate_runner(runner)
            runner_rect.centery += runner_movement
            screen.blit(rotated_runner, runner_rect) #rotates the runner as game is active
            screen.blit(options, (0,0)) #shows the options menu over the game
            game_active = check_collision(platform_list) #checks for collisions with the platforms

            if easy_mode: #addition of easy and hard modes
                #easy platforms
                platform_list = move_plats_easy (platform_list)
                draw_plats(platform_list)
                #scoreboard
                score_number += 0.0072  #how fast the score goes up
                score_board('game_running')
            if hard_mode:
                #hard platforms
                platform_list = move_plats_hard(platform_list)
                draw_plats(platform_list)
                #scoreboard
                score_number += 0.0079  #how fast the score goes up
                score_board('game_running')
        else: #addition of options menu overlay
            screen.blit(game_over_screen,game_over_rect) #shows the gameover screen when game is not active
            screen.blit(options, (0, 0))
            high_score = update_score(score_number, high_score)
            score_board('game_over')

    
    pg.display.update()
    clock.tick(120) #framerate