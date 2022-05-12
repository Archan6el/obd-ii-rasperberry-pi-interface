import obd
from pygame.locals import *
import pygame

pygame.init()
obd.logger.setLevel(obd.logging.DEBUG)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

connection = obd.Async("/dev/rfcomm99", protocol="6", baudrate="9600", fast=False, timeout = 30)

#Continuously query until the amount of supported commands is greater than 100
while len(connection.supported_commands) < 100:
    connection = obd.Async("/dev/rfcomm99", protocol="6", baudrate="9600", fast=False, timeout = 30)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.mouse.set_visible(False)

#Initial values for speed, rpm, and load
speed = 0
rpm = 0
load = 0

#Method used to draw our graphics to the screen
def draw_screen():
    
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, pygame.Rect(5, 5, 150, 150), 2)
    pygame.draw.rect(screen, WHITE, pygame.Rect(270, 5, 150, 150), 2)
    pygame.draw.rect(screen, WHITE, pygame.Rect(155, 100, 115, 115), 2)
    
    speedF = pygame.font.SysFont(None, 50)
    speedText = speedF.render("Speed", True, WHITE)
    screen.blit(speedText, (15, 160))
     
    rpmF = pygame.font.SysFont(None, 50)
    rpmText = rpmF.render("RPM", True, WHITE)
    screen.blit(rpmText, (310, 160))
    
    loadF = pygame.font.SysFont(None, 50)
    loadText = loadF.render("Load", True, WHITE)
    screen.blit(loadText, (175, 60))

#Commands to query for data
c1 = obd.commands.SPEED  
c2 = obd.commands.RPM
c3 = obd.commands.ENGINE_LOAD

#Tracks the values of speed, rpm, and load since they will be constantly changing as you drive
def speedTracker(s):
    global speed
    if not s.is_null():
        speed = int(s.value.magnitude * .621)
    
def rpmTracker(r):
    global rpm
    if not r.is_null():
        rpm = int(r.value.magnitude)

def loadTracker(l):
    global load
    if not l.is_null():
        load = int(l.value.magnitude)

#Watches the data extracted by the obd adapter        
connection.watch(c1, callback=speedTracker)
connection.watch(c2, callback=rpmTracker)
connection.watch(c3, callback=loadTracker)
connection.start()
    
running =  True
#Pygame loop which displays our graphics as well as our speed, load, and rpm values
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.display.quit()
                pygame.quit()
    
    draw_screen()
   
    speedFont = pygame.font.SysFont(None, 50)
    speedTxt = speedFont.render(str(speed) + " mph", True, WHITE)
    
    rpmFont = pygame.font.SysFont(None, 75)
    rpmTxt = rpmFont.render(str(rpm), True, WHITE)
    
    loadFont = pygame.font.SysFont(None, 75)
    loadTxt = speedFont.render(str(load) + "%", True, WHITE)
    
    screen.blit(speedTxt, (22, 50))

    screen.blit(rpmTxt, (285, 50))
    
    screen.blit(loadTxt, (172, 130))
    
    pygame.display.update()
    pygame.display.flip()
    
pygame.quit()
