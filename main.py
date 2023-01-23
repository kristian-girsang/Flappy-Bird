import pygame, sys, random

# Function to draw the floor on the screen
def draw_floor():
    # Blit the floor surface at the current floor x position and at the bottom of the screen
    screen.blit(floor_surface,(floor_x_pos,900))
    screen.blit(floor_surface,(floor_x_pos + 576,900))

# Function to create the pair of pipes
def create_pipe():
    # Choose the height of the pipe
    random_pipe_pos = random.choice(pipe_height)
    # Get the rect of the top pipe with midbottom position of (700,random_pipe_pos - 300)
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
    # Get the rect of the bottom pipe with a midtop position of (700,random_pipe_pos)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    return bottom_pipe, top_pipe

# Function to move the pipes on the screen
def move_pipes(pipes):
    # Move each pipe on the x-axis by pixels
    for pipe in pipes:
        pipe.centerx -= 5
    # Get only the pipes that are visible on the screen
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

# Function to draw the pipes on the screen
def draw_pipes(pipes):
    for pipe in pipes:
        # If the bottom of the pipe is greater than or equal to 1024 pixels, draw the pipe normally
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            # Otherwise, flip the pipe and draw it
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

# Function to check for collision between the bird and pipes
def check_collision(pipes):
    global can_score
    for pipe in pipes:
        # If the bird collides with a pipe, play the hit sound and set can_score to True
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            can_score = True
            return False
    # If the bird collides with the top or bottom of the screen, set can_score to True        
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        can_score = True
        return False
    return True

# Function to rotate the bird based on its movement
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3,1)
    return new_bird

# Function to animate the bird
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

# Function to check for scoring
def pipe_score_check():
    global score, can_score
    # If there are pipes in the pipe_list
    if pipe_list:
        for pipe in pipe_list:
            # If the bird passes a pipe and can_score id True, increase the score and play the score sound
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            # If a pipe goes off the left side of the screen, set can_score to True
            if pipe.centerx < 0:
                can_score = True

# Function to display the score on the screen
def score_display(game_state):
    if game_state == 'main_game':
        # Render the current score and display it on the screen
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        # Render the current score and display it on the screen
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
        # Render the highscore and display it on the screen
        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)

# Function to update the high score if the current score is grater than the high score
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

# Initialize pygame and set the screen size
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

# Load and scale the background image
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# Load the floor surface
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# Load the bird frames
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
# Creating the list of the bird frames, this list will be used to change the bird image for animation
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
# Setting the initial frame of the bird
bird_index = 0
# Setting the bird surface to the first frame of the bird
bird_surface = bird_frames[bird_index]
# Creating a rect object for the bird, this will be used to position the bird on the screen
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)


# Load the pipe surface
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
# Create a list to store the pipes
pipe_list = []
# Create a custom event for spawning pipes
SPAWNPIPE = pygame.USEREVENT    # timer
# Set a timer for the custom event to occur every 1200 milliseconds
pygame.time.set_timer(SPAWNPIPE,1200)
# Define a list of possible heights for the pipes
pipe_height = [400,600,800]

# Load the game over sound
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
# Create a rect object for the game over image, and make its position in the center
game_over_rect = game_over_surface.get_rect(center = (288,512))

# Load the flap sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')

# Load the hit sound
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')

# Load the score sound
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
# Create a variable for counting how many times the sound has been played
score_sound_countdown = 100

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: # check if any of the keyboard pressed
            if event.key == pygame.K_SPACE and game_active:
                # If the spacebar is pressed and the game is active, the bird should move up and play the flap sound 
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                # If the spacebar is pressed and the game is not active, the game should be reset
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) # create a new pipe

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            # Update the bird's animation
            bird_surface,bird_rect = bird_animation()

    # Clear the screen
    screen.blit(bg_surface,(0,0))
    
    if game_active:
        # Bird
        # If the game is active, update the bird's position by appliying gravity, rotate the bird, and render it on the screen
        bird_movement += gravity # gravity is increasing downward
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        # Check if there is acollision between the bird and the pipes
        game_active = check_collision(pipe_list)

        # Pipes
        # Move and render the pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #Score
        # Update and render the score
        pipe_score_check()
        score_display('main_game')
    else:
        # If the game is not active, render the game over message and update the high score
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    # Draw the floor
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    # Update the screen
    pygame.display.update()
    clock.tick(120) # FPS