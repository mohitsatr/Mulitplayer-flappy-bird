import pygame
from queue  import Queue
import random 

window_width = 370
window_height = 400



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
magenta = (255, 0, 255)
cyan = (0, 255, 255)
maroon = (128, 0, 0)
dark_green = (0, 128, 0)
navy = (0, 0, 128)
gray = (128, 128, 128)



# 1 : flying 
# 2 : falling 
#3 : mid 

def rotate(image):
    return pygame.transform.rotate(image,45)

# im = pygame.image.load("Assets\\bluebird-midflap.png")
# rotated = rotate(im)
# pygame.image.save(rotated,"B:\Mohit\\Projects\\fl-mu\Assets\\rotated.png")

class Bird:
    angle = 0 
    def __init__(self,color="blue"):
        self.player = None
        self.angle = 0 
        self.x = None 
        self.y = None 
        self.state = 2  
        self.color = color 

        self.image = pygame.image.load(f"Assets/{color}bird-midflap.png")
    

        self.MOVEMENTS = Queue(3)
        
        self.MOVEMENTS.put(pygame.image.load(f"Assets\\{self.color}bird-upflap.png"))
        self.MOVEMENTS.put(pygame.image.load(f"Assets\\{self.color}bird-midflap.png"))
        self.MOVEMENTS.put(pygame.image.load(f"Assets\\{self.color}bird-downflap.png"))
    
    
    def change_state(self,c_state): # so this only rotates the img , does to show it on window
        r_img = ""
        if c_state == 1 :
            r_img = pygame.transform.rotate(self.image,45)
        
        if c_state == 2:
            r_img = pygame.transform.rotate(self.image,self.angle)
            self.angle -= 1
        else :
            r_img = self.image
        return r_img 

    def update(self):
        self.image = self.MOVEMENTS.get()
        self.MOVEMENTS.put(self.image)
    
    def draw(self,window): 
        if self.x and self.y :
            self.update()
            # self.image = self.change_state(self.state)
            window.blit(self.image,self.image.get_rect(topleft=(self.x,self.y)))#self.image.get_rect(topleft=(self.x,self.y)))
        

        if self.angle >= 90:
            self.angle = 90 
        
        if self.angle <= -90:
            self.angle = -90


GAP = 20 
starting = window_width+50
def place_pipes():
    red_coors = (starting,random.randint(-500,-100))

    green_coors = (starting+50,red_coors[1]+GAP+int(window_height*1/1.5))

    return (red_coors,green_coors)


class Pipe:
    def __init__(self,x,y,color=1) -> None:
        self.x = x
        self.y = y
        self.image = self.get_pipe(color)


    
    def get_pipe(self,color):
        if color == 1:
            return pygame.transform.rotate(pygame.image.load("Assets/pipe-red.png"),180)
            
        else :
            return pygame.image.load("Assets/pipe-green.png")


    def move(self,val):    
        self.x  -= val 

    def draw(self,window):
        window.blit(self.image,self.image.get_rect(topleft=(self.x,self.y)))


def move_floor(floor,val):
    if floor.right == window_width :
        floor.right = window_width+100
    floor.right -= val


