import pygame
import sys
from network import Network
from box import *
from utilses import collision ,draw_text
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


font = pygame.font.SysFont('Bauhaus 93',60 )


def fill_pipes():
    red_coor,green_coor = place_pipes()
    score_line_x = red_coor[0]
    score_line_y = green_coor[0]

    green_pipe = Pipe(green_coor[0],green_coor[1],2)
    
    red_pipe = Pipe(red_coor[0],red_coor[1],1)


    
    Pipes.append(red_pipe)
    Pipes.append(green_pipe)


floor = scale(pygame.image.load("Assets\\base.png"),x=window_width+100)
floor_rect = floor.get_rect(topleft=(0,350))
clock = pygame.time.Clock()


# scoreline = ScoreLine(score_line_x,0,score_line_y,window_height,)

gameOver = False   



def main():
    n = Network()
    positions = n.connect()
    print("result from the connection is this ",positions)
    
    # due to something happening here , it's giving me error of rect assignment 

    player1_bird = Bird("blue")
    player1_bird.x,player1_bird.y = positions

 
    player2_bird = Bird("red")


    #scores
    score = 0
   
    line_crossed = False 


    pushvalue = 50
    gravity_limit = 2 
    initial_gravity = 2

   # player1_bird.state = 3 
    
    fill_pipes()
    start = window_width
    running = True 

    if running == False :
        gameOver = True 

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
            
        else :
            player1_bird.state = 2
        

         



        if line_crossed:  
            fill_pipes()    
            line_crossed = False
             


        #print(scoreline.start_x,scoreline.start_y,"-",scoreline.end_x,scoreline.end_y)

        for pipe in Pipes:
            pipe.draw(window)
            pipe.move(2)
            if pipe.x < -100:
                Pipes.remove(pipe)  
        
            
        start = 0,0
        end = 0,0
        for pipe in Pipes :
            if pipe == "red":
                start = pipe.get_rect(pipe.image).bottomright

            if pipe == "green":    
                end = pipe.get_rect(pipe.image).topright


        if player1_bird.get_rect(player1_bird.image).clipline(start,end):
            line_crossed = True 
            score += 1
            
            
        if not line_crossed:
            pygame.draw.line(window,WHITE,start,end,1)


        window.blit(floor,floor_rect)             
        move_floor(floor_rect,2)               
        
        if player1_bird.collision(floor_rect):
            running = False 

        player2_bird.draw(window)

        player1_bird.draw(window)

        draw_text(window,str(score),font,WHITE,50,50)


       # player2_bird.draw(window)
        player1_bird.y += initial_gravity
    
        print(player1_bird.x,player1_bird.y," ",player1_bird.angle)
        #b2.draw(window)
      #   player1.draw(window)
      #   p.draw(window)
      #   # box1.draw(window)
        player2_bird.x,player2_bird.y = n.send((player1_bird.x,player1_bird.y))
        #player2_bird.x ,player2_bird.y = n.send((player1_bird.x,player1_bird.y))# sending 
        
        pygame.display.update()
        clock.tick(30)


def game_over():
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()



        window.blit(background,(0,0)) 

        window.blit(floor,floor_rect)             
        move_floor(floor_rect,2)    
    
        pygame.display.update()


main()



# i think - for each screen - there is their player that is player one .