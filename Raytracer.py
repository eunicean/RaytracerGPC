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

raytracer.envMap = pygame.image.load("textures/harbor.jpg")
raytracer.rtClearColor(0.25,0.25,0.25)
# raytracer.rtClearColor(0.741,0.878,0.996)


#TEXTURES
jupiterTexture = pygame.image.load("textures/jupiter.jpg")
marbleTexture = pygame.image.load("textures/marble.jpg")
#MATERIALS
brick = Material(diffuse=(1,0.4,0.4),spec=8, Ks= 0.01)
grass = Material(diffuse=(0.4,1,0.4),spec=32, Ks= 0.1)
water = Material(diffuse=(0.4,0.4,1),spec=256, Ks= 0.2)
mirror = Material(diffuse=(0.9,0.9,0.9),spec=64, Ks=0.2,matType=REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9),spec=32, Ks=0.15,matType=REFLECTIVE)
jupiter = Material(texture=jupiterTexture)
marble = Material(texture=marbleTexture, spec=64, Ks=0.1, matType=REFLECTIVE)
glass = Material(diffuse=(0.9,0.9,0.9),spec=64, Ks=0.2, ior=1.5, matType=TRANSPARENT)

# raytracer.scene.append(Sphere(position=(0,0,-7), radius=2, material = mirror))
# raytracer.scene.append(Sphere(position=(0.5,-1,-5), radius=0.3, material = water))

# raytracer.scene.append(Sphere(position=(-2,0,-7), radius=1.5, material = marble))
# raytracer.scene.append(Sphere(position=(2,0,-7), radius=2, material = jupiter))
# raytracer.scene.append(Sphere(position=(0,-1,-5), radius=0.5, material = mirror))

raytracer.scene.append(Sphere(position= (0,0,-5), radius= 2, material= glass))

raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(-1,-1,-1), intensity=0.9))
# raytracer.lights.append(PointLight(point=(2.5,0,-5),intensity=0.5,color=(1,0,1)))

raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time: ", pygame.time.get_ticks()/1000, "secs")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if closed, the programm will be stopped
            isRunning == False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

pygame.quit()

#falla: solo dibuja el circulo en negro en vez de refractar
#toca: clase 28-09