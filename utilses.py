
import pygame,sys
def check_collision(begin,bird,obj,obj2,floor):
    if begin :
        if pygame.sprite.groupcollide(obj,obj2,False,False):
            return True  # with pipes 
        

        if bird.rect.y <= 0: # with sky boundary 
            return True 

        if bird.rect.colliderect(floor): # with floor 
            return True


def draw_text(screen,font,text,text_col,x,y):
    img = font.render(text,True,text_col)

    screen.blit(img,(x,y))
     
