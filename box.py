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
        

        if c_state == 2 :
            r_img = self.image
       
        return r_img 
    
    def get_rect(self,image):
        return image.get_rect(topleft=(self.x,self.y))

    def collision(self,obj):
        bird_rectangle = self.get_rect(self.image)

        if bird_rectangle.colliderect(obj):
            return True 


    def update(self):
        if self.state == 1:
            tmpr = self.MOVEMENTS.get()
            self.image = tmpr 
            self.image = self.change_state(1)# rotated image shouldnot be queue for next round 

            self.MOVEMENTS.put(tmpr)

        else :
            self.image = self.change_state(2)
      

    def draw(self,window): 
        if self.x and self.y :
            self.update()
            
            window.blit(self.image,self.image.get_rect(topleft=(self.x,self.y)))#self.image.get_rect(topleft=(self.x,self.y)))
    
        if self.angle >= 90:
            self.angle = 90 
        
        if self.angle <= -90:
            self.angle = -90


GAP = 50
starting = window_width+50
def place_pipes(): #red pipe minimum y = -250
    red_coors = (starting,random.randint(-250,-100))#random.randint(-450,-100))
    grn = (starting+random.randint(0,GAP),300) #minimum green y = 300



  #  green_coors = (starting+50,red_coors[1]+GAP+int(window_height*1/1.5))

    return (red_coors,grn)


class Pipe:
    def __init__(self,x,y,color=1) -> None:
        self.x = x
        self.y = y
        self.image = self.get_pipe(color)

        self.color = "red" if color == 1 else "green"

        
    
    def get_rect(self,image):
        return image.get_rect(topleft=(self.x,self.y))
    

    def get_pipe(self,color):
        if color == 1:
            return pygame.transform.rotate(pygame.image.load("Assets/pipe-red.png"),180)
            
        else :
            return pygame.image.load("Assets/pipe-green.png")


    def move(self,val):    
        self.x  -= val 

    def draw(self,window):
        window.blit(self.image,self.image.get_rect(topleft=(self.x,self.y)))

    def __eq__(self, __value: object) -> bool:
        return self.color.__eq__(__value)

P = Pipe(40,80,1)



def move_floor(floor,val):
    if floor.right == window_width :
        floor.right = window_width+100
    floor.right -= val


