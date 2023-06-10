import pygame
from queue  import Queue
import random 

window_width = 400
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


SPEED = 2.3
# 1 : flying 
# 2 : falling 
#3 : mid 

def rotate(image):
    return pygame.transform.rotate(image,45)

def scale(obj,x=None,y=None):
    if x == None:
        x = obj.get_width()
    elif y == None  :
        y = obj.get_height()
    return pygame.transform.scale(obj,(x,y))



Floor_x = 350 # floor starts at 
floor = scale(pygame.image.load("Assets\\base.png"),x=window_width+100)
floor_rect = floor.get_rect(topleft=(0,Floor_x))


def draw_floor(window):
    window.blit(floor,floor_rect)             
    move_floor(floor_rect,SPEED)  

class Flappy(pygame.sprite.Sprite):
    def __init__(self,color="blue") -> None:
        pygame.sprite.Sprite.__init__(self)
        self.bird_images = []
        self.color = color 
        self.current = 0
        self.bird_images.append(pygame.image.load(f"Assets\\{self.color}bird-upflap.png"))
        self.bird_images.append(pygame.image.load(f"Assets\\{self.color}bird-midflap.png"))
        self.bird_images.append(pygame.image.load(f"Assets\\{self.color}bird-downflap.png"))

        
        self.image = self.bird_images[self.current]

        self.rect= self.image.get_rect()
        self.rect.topleft = (0,0)
        self.fly = False
        
        self.grav  = 0
        self.angle = 1

    def render(self,window):
        if self.rect.x != 0 :
            window.blit(self.image,self.rect)
    
    def is_flying(self):
        self.grav = 3 # it restricts the total_acc from incresasing beyond -16 
        total_acc = 0
        self.grav -= 7 # direct relationship with bird's flying and falling . 
        total_acc += self.grav*(-self.grav) # without minus sign , variable will become positive 

        self.rect.y += total_acc
      
        total_acc = 0 

        
        
        
            

    def update(self,window,fly,collision,begin):
        self.render(window)
        if begin :  
            if not collision:
                self.image = self.bird_images[int(self.current)]

                if fly :
                    self.is_flying()
            
        
                if self.grav < 2.5:  # means bird is flying 
                    self.grav += 0.3
                    img = pygame.transform.rotate(self.image,25)
                    self.image = img
                
                
                if self.grav >= 2.5  :  
                    self.grav = 3 
                    img = pygame.transform.rotate(self.image,-25)
                    self.image = img 
            
            
                self.rect.y += self.grav 

            else:
                global SPEED
                SPEED = 0
                self.grav = 3
                if self.rect.y < 320:
                    self.rect.y += self.grav
                                        

            


class Bird:
    angle = 0 
    def __init__(self,color="blue"):
        self.player = None
        self.angle = 0 
        self.x = None 
        self.y = None 
        self.state = 3
        self.color = color 

        self.image = pygame.image.load(f"Assets/{color}bird-midflap.png")


        self.MOVEMENTS = Queue(3)
        
        self.MOVEMENTS.put(pygame.image.load(f"Assets\\{self.color}bird-upflap.png"))
        self.MOVEMENTS.put(pygame.image.load(f"Assets\\{self.color}bird-midflap.png"))
        self.MOVEMENTS.put(pygame.image.load(f"Assets\\{self.color}bird-downflap.png"))
    
    

    
    def change_state(self,c_state): # so this only rotates the img , does to show it on window
        r_img = ""
        if c_state == 1 :
            r_img = pygame.transform.rotate(self.image,self.angle)
            if self.angle < 45 :
                self.angle += 2
        

        elif c_state == 2 :
            r_img = pygame.transform.rotate(self.image,self.angle)
            if self.angle > -20:
                self.angle -= 2

    
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

        elif self.state == 2 :
            self.image = self.change_state(2)

      

    def draw(self,window): 
        if self.x and self.y :
            self.update()
            
            window.blit(self.image,self.image.get_rect(topleft=(self.x,self.y)))#self.image.get_rect(topleft=(self.x,self.y)))
    
    
GAP = 50
starting = window_width+50


def place_pipes(): #red pipe minimum y = -250
    red_coors = (starting,random.randint(-250,-100))#random.randint(-450,-100))
    grn = (starting+random.randint(0,GAP),300) #minimum green y = 300

  #  green_coors = (starting+50,red_coors[1]+GAP+int(window_height*1/1.5))

    return (red_coors,grn)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,color=1) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

        self.color = "red" if color == 1 else "green"
        self.image = self.get_pipe(color)

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)

    def render(self,window):
        window.blit(self.image,self.rect)    

    def get_pipe(self,color):
        if color == 1:
            return pygame.transform.rotate(pygame.image.load("Assets/pipe-red.png"),180)
            
        else :
            return pygame.image.load("Assets/pipe-green.png")
    def __str__(self):
        return self.color

    def move(self):    
        self.rect.x  -= SPEED

    def offscreen(self):
        if self.rect.x < -50:
            self.kill()

    
    
    # def __eq__(self,val):
    #     return self.color == val

    def update(self,begin):
        if begin :
            self.move()
            self.offscreen()
            

def move_floor(floor,val):
    if floor.right <= window_width :
        floor.right = window_width+100
    floor.right -= val



class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self,screen):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action