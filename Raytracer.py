import pygame
from pygame.locals import *

from rt import Raytracer

from figures import *
from lights import *
from materials import *

width = 256
height = 256

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE) #to show images in real time
screen.set_alpha(None)

raytracer = Raytracer(screen)
raytracer.rtClearColor(0.25,0.25,0.25)

brick = Material(diffuse=(1,0.4,0.4),spec=8)
grass = Material(diffuse=(0.4,1,0.4),spec=32)
water = Material(diffuse=(0.4,0.4,1),spec=256)

raytracer.scene.append(Sphere(position=(-2,0,-5), radius=0.5, material = brick))
raytracer.scene.append(Sphere(position=(0,0,-5), radius=0.5, material = grass))
raytracer.scene.append(Sphere(position=(2,0,-5), radius=0.5, material = water))
raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(0,-1,-1), intensity=0.7))

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if closed, the programm will be stopped
            isRunning == False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    raytracer.rtClear()
    raytracer.rtRender()

    pygame.display.flip()

pygame.quit()
