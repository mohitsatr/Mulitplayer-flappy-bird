import pygame
import sys
from network import Network
from box import *

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


# Create an instance of the Box class

#pipes
Pipes = []
def fill_pipes():
    red_coor,green_coor = place_pipes()
    green_pipe = Pipe(green_coor[0],green_coor[1],2)
    red_pipe = Pipe(red_coor[0],red_coor[1],1)

    
    Pipes.append(red_pipe)
    Pipes.append(green_pipe)






floor = scale(pygame.image.load("Assets\\base.png"),x=window_width+100)
floor_rect = floor.get_rect(topleft=(0,350))
clock = pygame.time.Clock()


def push_pull_coord(push_coor,push_value):
    pass





def main():
    n = Network()
    positions = n.connect()
    print("result from the connection is this ",positions)
    
    # due to something happening here , it's giving me error of rect assignment 

    player1_bird = Bird("blue")
    player1_bird.x,player1_bird.y = positions

 
    player2_bird = Bird("red")


    # player1 = n.connect()
    begin = False

    
 
    pushvalue = 50
    gravity_limit = 2 
    initial_gravity = 0

   # player1_bird.state = 3 

    fill_pipes()

    while True:

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




        if begin : 
        
            if len(Pipes) == 0:  
                fill_pipes()     
        
            for pipe in Pipes:
                pipe.draw(window)
                pipe.move(2)

                if pipe.x < -50:
                    Pipes.remove(pipe)
            
            
        
            if initial_gravity < gravity_limit:
                initial_gravity += 0.075
            


        window.blit(background,(0,0)) 

        window.blit(floor,floor_rect)
        move_floor(floor_rect,2)
    
      #   player1.move(keys)
 
      #   p = n.send(player1) # sending updated player1 , recieving player2 - but how is this working 
       # p = b.send(b2)
      # #  player2.move(keys)
        player1_bird.draw(window)

        player1_bird.draw(window)

       # player2_bird.draw(window)
        
      #  player1_bird.y += initial_gravity
    
        #b2.draw(window)
      #   player1.draw(window)
      #   p.draw(window)
      #   # box1.draw(window)
    
        player2_bird.x ,player2_bird.y = n.send((player1_bird.x,player1_bird.y))# sending 
        
        pygame.display.update()
        clock.tick(60)
        


main()

# i think - for each screen - there is their player that is player one .