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
raytracer.rtClearColor(0.741,0.878,0.996)

#TESTS
# brick = Material(diffuse=(1,0.4,0.4),spec=8, Ks= 0.01)
# grass = Material(diffuse=(0.4,1,0.4),spec=32, Ks= 0.1)
# water = Material(diffuse=(0.4,0.4,1),spec=256, Ks= 0.2)

# raytracer.scene.append(Sphere(position=(1,1,-5), radius=0.5, material = grass))
# raytracer.scene.append(Sphere(position=(0,0,-7), radius=2, material = brick))
# raytracer.scene.append(Sphere(position=(0.5,-1,-5), radius=0.3, material = water))
# raytracer.lights.append(AmbientLight(intensity=0.1))
# raytracer.lights.append(DirectionalLight(direction=(-1,-1,-1), intensity=0.7))
# raytracer.lights.append(PointLight(point=(2.5,0,-5),intensity=0.5,color=(1,0,1)))

#RT1
snow = Material(diffuse=(1,1,1), spec=8, Ks=0.07)
carbon = Material(diffuse=(0,0,0), spec=8, Ks=0.07)
carrot = Material(diffuse=(0.984,0.521,0), spec=8, Ks=0.07)

#spheres
#body
raytracer.scene.append(Sphere(position=(0,0.15,-9), radius=1.3, material=snow))
raytracer.scene.append(Sphere(position=(0,-2.2,-9), radius=1.7, material=snow))
#face
raytracer.scene.append(Sphere(position=(0,1.65,-9), radius=1, material=snow))
raytracer.scene.append(Sphere(position=(0.4,1.6,-7.8), radius=0.15, material=carbon))
raytracer.scene.append(Sphere(position=(-0.4,1.6,-7.8), radius=0.15, material=carbon))
raytracer.scene.append(Sphere(position=(0,1.5,-7.8), radius=0.15, material=carrot))
raytracer.scene.append(Sphere(position=(-0.4,1.25,-7.8), radius=0.07, material=carbon))
raytracer.scene.append(Sphere(position=(0.4,1.25,-7.8), radius=0.07, material=carbon))
raytracer.scene.append(Sphere(position=(-0.25,1.15,-7.8), radius=0.07, material=carbon))
raytracer.scene.append(Sphere(position=(0.25,1.15,-7.8), radius=0.07, material=carbon))
raytracer.scene.append(Sphere(position=(0,1.1,-7.8), radius=0.07, material=carbon))
#buttons
raytracer.scene.append(Sphere(position=(0,0.25,-6.9), radius=0.15, material=carbon))
raytracer.scene.append(Sphere(position=(0,-0.85,-6.9), radius=0.17, material=carbon))
raytracer.scene.append(Sphere(position=(0,-2.2,-6.9), radius=0.19, material=carbon))

#lights
raytracer.lights.append(AmbientLight(intensity=0.9))
raytracer.lights.append(PointLight(point=(2.5,0,-5),intensity=0.7,color=(0.937,0.137,0.235)))
raytracer.lights.append(PointLight(point=(-2.5,2,-5),intensity=0.8,color=(1,0.862,0.521)))

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
