import pygame
from pygame.locals import *

from rt import Raytracer

from figures import *
from lights import *
from materials import *

width = 128
height = 128

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED) #to show images in real time
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
water = Material(diffuse=(0.4,0.4,1),spec=256, Ks= 0.2, ior=4,matType=TRANSPARENT)
mirror = Material(diffuse=(0.9,0.9,0.9),spec=64, Ks=0.2,matType=REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9),spec=32, Ks=0.15,matType=REFLECTIVE)
jupiter = Material(texture=jupiterTexture)
marble = Material(texture=marbleTexture, spec=64, Ks=0.1, matType=REFLECTIVE)
glass = Material(diffuse=(0.9,0.9,0.9),spec=64, Ks=0.1, ior=1.5, matType=TRANSPARENT)
diamond = Material(diffuse=(0.9,0.9,0.9),spec=128, Ks=0.2, ior=2.417, matType=TRANSPARENT)
jupiter = Material(texture=jupiterTexture)
jupiterglassball = Material(texture=jupiterTexture, spec=64, Ks=0.1,matType= REFLECTIVE)
canica = Material(texture=marbleTexture, diffuse=(0.8,0.8,1.0), spec=64, Ks=0.15, ior=1.5, matType=TRANSPARENT)

# raytracer.scene.append(Sphere(position=(0.5,-1,-5), radius=0.3, material = water))

# raytracer.scene.append(Sphere(position=(-2,0,-7), radius=1.5, material = marble))
# raytracer.scene.append(Sphere(position=(0,-1,-5), radius=0.5, material = mirror))

# raytracer.scene.append(Sphere(position= (0,1,-5), radius= 0.85, material= water))
# raytracer.scene.append(Sphere(position= (0,-1,-5), radius= 0.85, material= diamond))
# raytracer.scene.append(Sphere(position= (-2,1,-5), radius= 0.85, material= brick))
# raytracer.scene.append(Sphere(position=(-2,-1,-5), radius=0.85, material = jupiter))
# raytracer.scene.append(Sphere(position=(2,1,-5), radius=0.85, material = mirror))
# raytracer.scene.append(Sphere(position=(-2,-1,-5), radius=0.85, material = jupiterglassball))

raytracer.scene.append(Sphere(position=(0,0,-5), radius=1.0,material=canica))
raytracer.scene.append(Plane(position=(0,-5,0),normal=(0,1,0),material=brick))
raytracer.scene.append(Disk(position=(0,-1.5,-5),normal=(0,1,0),radius=1.5,material=mirror))

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
