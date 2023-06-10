import pygame 
from box import *
import sys 
from utilses import *
from pygame import font 
from network import Network

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Controlled Box")
background_image = pygame.image.load("Assets\\background-night.png").convert()
background = pygame.transform.scale(background_image, (window_width, window_height))
clock = pygame.time.Clock()

game_over = pygame.image.load("Assets\\gameover.png")

def create_pipes():
    red_coor,green_coor = place_pipes()
    green_pipe = Pipe(green_coor[0],green_coor[1],2)
    red_pipe = Pipe(red_coor[0],red_coor[1],1)
    return green_pipe,red_pipe

def fill_pipes(p1,p2):
    pipesGroup.add(p1)
    pipesGroup.add(p2)


def get_pipe_crossing_coordinates(Upper,lower):
    start = Upper.rect.bottomright
    end = lower.rect.topright 
    return start,end



b = Flappy()
c = Flappy("red")

n = Network()
b.rect.topleft = n.connect() # gets initial positions from the server . 


p1 = pygame.sprite.Group()
p1.add(b)

p2 = pygame.sprite.Group()
p2.add(c)



pipesGroup = pygame.sprite.Group()

rb  = pygame.image.load("Assets\\restart.png")
restart_button = Button(200,200,rb)

pushvalue = 0
font.init()
font = pygame.font.SysFont('Bauhaus 93',60)

Game_ = {
    "player1" : {
        "score":0,"current_position":(0,0),"fly":False,"collision":False  
    },
    "player2" : {
        "score":0,"current_position":(0,0),"fly":False,"collision":False  
    }
}

def main(): 
    gravity = 2 
    fly_1 = False 
    legal = True 
    max_gravity = 2
    event_interval = 500  # Time interval in milliseconds (3 seconds in this example)
    event_timer = pygame.time.get_ticks() + event_interval
    collision = False 
    running = True
    score = 0 
    global SPEED
    line_crossed = True
    begin = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()      
                sys.exit()


            if event.type == pygame.KEYDOWN :
                if  event.key == pygame.K_SPACE:
                    fly_1 = True 
                    begin = True 

        if line_crossed :
            green,red = create_pipes()
            
            fill_pipes(green,red)
            line_crossed = False
    
        if score%5 == 0 :
            
            SPEED += 2
        window.blit(background,(0,0))
        pipesGroup.draw(window)
        pipesGroup.update(begin)
    

        draw_floor(window)


        start = None 
        end   = None 
        for pipe in pipesGroup:
            if pipe == red:
                start = pipe.rect.bottomright
            if pipe == green:
                end = pipe.rect.topright
        
        if start is not None and end is not None :
            pygame.draw.line(window,WHITE,start,end,0)
            if b.rect.clipline(start,end):
                line_crossed = True 
                score += 1
                    
        p1.update(window,fly_1,collision,begin)

        p2.update(window,Game_["player2"]["fly"],Game_["player2"]["collision"],begin)
        
        
        fly_1 = False


        col = check_collision(begin,b,p1,pipesGroup,floor_rect) 
        if col :
            collision = True 
           
        if collision: 
            window.blit(game_over,game_over.get_rect(topleft=(50,window_height//3)))
            restart = restart_button.draw(window)
            if restart == True:
                p1.remove(b)
                repos = n.restart_request()
                b.rect.topleft = repos
                p1.add(b)
                
                SPEED = 2.3
                collision,col = False,False
                begin = False
                score = 0 
                pipesGroup.empty()
         
            #draw_text(window,font,"Game Over",WHITE,50,window_height//3)


        draw_text(window,font,str(score),WHITE,0,0)

        p2.remove(c)
        update_state = n.send(Game_["player1"])
        Game_["player2"] = update_state
        c.rect.topleft = Game_["player2"]["current_position"]
        p2.add(c)
    
        pygame.display.update()
        clock.tick(60)

main()

