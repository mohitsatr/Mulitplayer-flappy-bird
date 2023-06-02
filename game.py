import pygame
import sys
from network import Network
from box import *
from utilses import collision 
# 1 : flying 
# 2 : falling 
#3 : mid   


def scale(obj,x=None,y=None):
    if x == None:
        x = obj.get_width()
    elif y == None  :
        y = obj.get_height()
    return pygame.transform.scale(obj,(x,y))

# Initialize Pygame
pygame.init()
 
# Create the window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Controlled Box")
background_image = pygame.image.load("Assets\\background-night.png").convert()
background = pygame.transform.scale(background_image, (window_width, window_height))


Pipes = []


def fill_pipes():
    red_coor,green_coor = place_pipes()


    green_pipe = Pipe(green_coor[0],green_coor[1],2)
    end_line = green_pipe.get_rect(green_pipe.image).midbottom
    red_pipe = Pipe(red_coor[0],red_coor[1],1)

    start_line = red_pipe.get_rect(red_pipe.image).midbottom
    
    Pipes.append(red_pipe)
    Pipes.append(green_pipe)


floor = scale(pygame.image.load("Assets\\base.png"),x=window_width+100)
floor_rect = floor.get_rect(topleft=(0,350))
clock = pygame.time.Clock()


def main():
    n = Network()
    positions = n.connect()
    print("result from the connection is this ",positions)
    
    # due to something happening here , it's giving me error of rect assignment 

    player1_bird = Bird("blue")
    player1_bird.x,player1_bird.y = positions

 
    player2_bird = Bird("red")


    # player1 = n.connect()
    score = 0
    
    pushvalue = 50
    gravity_limit = 2 
    initial_gravity = 2

   # player1_bird.state = 3 
    running = True  
    fill_pipes()

    start_line = (0,0)
    end_line = (0,0)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1_bird.state = 1 
                    initial_gravity = 0 
                    #oring_pos = push_pull_coord(b.y,push_value)
                    player1_bird.y -= pushvalue
                    

        
        
        if initial_gravity < gravity_limit:

            player1_bird.state = 1
            initial_gravity += 0.075
            


        window.blit(background,(0,0)) 


        if len(Pipes) == 0:  
            fill_pipes()     


        for pipe in Pipes:
            pipe.draw(window)
            pipe.move(2)
            if pipe.x < -50:
                Pipes.remove(pipe)  

            if pipe == "green":
                end_line = pipe.get_rect(pipe.image).midtop

            if pipe == "red":
                start_line = pipe.get_rect(pipe.image).midbottom
    
            pygame.draw.line(window,WHITE,start_line,end_line,1)

            if player1_bird.get_rect(player1_bird.image).clipline((start_line,end_line)):
                score += 1 
                start_line,end_line = (0,0),(0,0)

        window.blit(floor,floor_rect)
        move_floor(floor_rect,2)
        
        if player1_bird.collision(floor_rect):
            running = False

        player2_bird.draw(window)

        player1_bird.draw(window)



       # player2_bird.draw(window)
        print(score)
        player1_bird.y += initial_gravity
        player1_bird.state = 2
    
        #b2.draw(window)
      #   player1.draw(window)
      #   p.draw(window)
      #   # box1.draw(window)
        player2_bird.x,player2_bird.y = n.send((player1_bird.x,player1_bird.y))
        #player2_bird.x ,player2_bird.y = n.send((player1_bird.x,player1_bird.y))# sending 
        
        pygame.display.update()
        clock.tick(60)
        


main()

# i think - for each screen - there is their player that is player one .