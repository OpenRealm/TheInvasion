#Bienvenue sur "TheInvasion" !				  #
#Un jeu créée par OpenRealm ( ͡°⊖ ͡°)  		  #
#Ps : J'ai fait le jeu en anglais au cas ou xD#
###############################################
#Welcome on "TheInvasion" !					  #
#A game by OpenRealm ( ͡°⊖ ͡°)				  #
###############################################

import pygame,sys
from pygame.locals import *
pygame.init()

#Variables Global
width=1200
height=600
level=0
fps=25
addnewflamerate=20

#Colors Selection
black=(0,0,0)
green=(0,255,0)
white=(255,255,255)

fond = pygame.image.load("ImagesSprites/Fond.png")
icon_32x32 = pygame.image.load("TheInvasion.png")
pygame.display.set_icon(icon_32x32)
pygame.display.set_mode((1200, 600))

#Class Ufo
class ufo:
    global canvas
    up=False
    down=True
    velocity=15

    def __init__(self):
        self.image=load_image("ImagesSprites/Ufo.png")
        self.imagerect=self.image.get_rect()
        self.imagerect.right=width
        self.imagerect.top=height/2

    def update(self):
        if(self.imagerect.top<cacbrick.bottom):
            self.down=True
            self.up=False
        if(self.imagerect.bottom>firebrick.top):
            self.up=True
            self.down=False
        if(self.up):
            self.imagerect.top-=self.velocity
        if(self.down):
            self.imagerect.bottom+=self.velocity
        canvas.blit(self.image,self.imagerect)

    def return_height(self):
        return self.imagerect.top

#Class flames
class flames:
    flamespeed=20

    def __init__(self):
        self.image=load_image("ImagesSprites/LaserBulet.png")
        self.imagerect=self.image.get_rect()
        self.height=ufo.return_height()+20#+20 refers to the mouth of the dragon
        self.surface=pygame.transform.scale(self.image,(20,20))
        self.imagerect=pygame.Rect(width-106,self.height,20,20)#width-106 refers to the width of the dragon or starting point of the flame
    def update(self):
        self.imagerect.left-=self.flamespeed

#Class Plane
class plane:
    global moveup,movedown,gravity
    speed=10
    downspeed=20
    def __init__(self):
        self.image=load_image("ImagesSprites/plane.png")
        self.imagerect=self.image.get_rect()
        self.imagerect.topleft=(50,height/2)
        self.score=0

    def update(self):
        if(moveup and (self.imagerect.top>cacbrick.bottom)):
            self.imagerect.top-=self.speed
            self.score+=1
        if(movedown and (self.imagerect.bottom<firebrick.top)):
            self.imagerect.bottom+=self.downspeed
            self.score+=1
        if(gravity and (self.imagerect.bottom<firebrick.top)):
            self.imagerect.bottom+=self.speed


#Helper Functions
def terminate():
    pygame.quit()
    sys.exit()

def waitforkey():
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    terminate()
                return


def flamehitsmario(playerrect,flames):
    for f in flames:
        if playerrect.colliderect(f.imagerect):
            return True
        return False

def load_image(path):
    return pygame.image.load(path)

def check_level(score):
    global firebrick,cacbrick,level,addnewflamerate
    #addnewflamerate is being reduced to increase rate of production of new flame with level up
    if score in range(0,250):
        firebrick.top=height-50
        cacbrick.bottom=50
        addnewflamerate=20
        level=1
    elif score in range(250,500):
        firebrick.top=height-100
        cacbrick.bottom=100
        addnewflamerate=18
        level=2
    elif score in range(500,750):
        firebrick.top=height-150
        cacbrick.bottom=150
        addnewflamerate=16
        level=3
    elif score in range(750,1000):
        firebrick.top=height-200
        cacbrick.bottom=200
        addnewflamerate=15
        level=4

def drawtext(text,font,x,y,surface):
    textobj=font.render(text,1,black)
    textrec=textobj.get_rect()
    textrec.center=(x,y)
    surface.blit(textobj,textrec)

#Main Program
clock=pygame.time.Clock()
canvas=pygame.display.set_mode((width,height),RESIZABLE)
pygame.display.set_caption("TheInvasion")
font=pygame.font.SysFont(None,48)
scorefont=pygame.font.SysFont(None,30)
#Images loads and creating rects

endobj=load_image('ImagesSprites/End2.png')
end=endobj.get_rect()
end.centery=height/2
end.centerx=width/2

startobj=load_image('ImagesSprites/Start2.png')
start=startobj.get_rect()
start.centerx=width/2
start.centery=height/2

cacbrickobj=load_image('ImagesSprites/LaserTest01.png')
cacbrick=cacbrickobj.get_rect()

firebrickobj=load_image('ImagesSprites/GrassTest01.png')
firebrick=firebrickobj.get_rect()

#Sound
pygame.mixer.music.load("MusicSprites/mario_theme.wav")
gameover=pygame.mixer.Sound("MusicSprites/mario_dies.wav")

canvas.blit(startobj,start)
pygame.display.update()

#GamePlay

waitforkey()
topscore=0
ufo=ufo()

while True:
    flame_list=[]
    player=plane()
    moveup=movedown=gravity=False
    flameaddcounter=0
    gameover.stop()
    pygame.mixer.music.play(-1,0.0)
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()

            if event.type==KEYDOWN:
                if event.key==K_UP:
                    moveup=True
                    movedown=False
                    gravity=False
                    player.update()
                if event.key==K_ESCAPE:
                    terminate()

            if event.type==KEYUP:
                if event.key==K_UP:
                    gravity=True
                    moveup=False
                    player.update()
                if event.key==K_DOWN:
                    movedown=False
                    gravity=True
                    player.update()

        flameaddcounter+=1
        check_level(player.score)
        """
        New flame is produced when flamecounter =addnewflamerate
        Create new flames object
        adding the new flame object to flame_list
        """
        if(flameaddcounter==addnewflamerate):
            flameaddcounter=0
            newflame=flames()
            flame_list.append(newflame)

        if(flameaddcounter>addnewflamerate):
            flameaddcounter=0


        for f in flame_list:
            flames.update(f)


        for f in flame_list:
            if f.imagerect.left<=0:
                flame_list.remove(f)
        player.update()
        ufo.update()

        canvas.blit(fond, (0,0))
        canvas.blit(firebrickobj,firebrick)
        canvas.blit(cacbrickobj,cacbrick)
        canvas.blit(player.image,player.imagerect)
        canvas.blit(ufo.image,ufo.imagerect)

        drawtext('Score : %s | Top score : %s | Level : %s' %(player.score, topscore, level), scorefont, width/2, cacbrick.bottom + 10,canvas)

        for f in flame_list:
            canvas.blit(f.surface, f.imagerect)
        #Conditions to end the game
        if flamehitsmario(player.imagerect,flame_list):
            if player.score > topscore:
                topscore=player.score
            break

        if player.imagerect.top<=cacbrick.bottom or player.imagerect.bottom>=firebrick.top:
            if player.score>topscore:
                topscore=player.score

            break
        pygame.display.update()
        clock.tick(fps)
    pygame.mixer.music.stop()
    gameover.play()
    canvas.blit(endobj,end)
    pygame.display.update()
    waitforkey()
