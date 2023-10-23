import pygame
from pygame.locals import *

from rt import Raytracer

from figures import *
from lights import *
from materials import *

size = 512
width = size
height = size

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED) #to show images in real time
screen.set_alpha(None)

raytracer = Raytracer(screen)

raytracer.envMap = pygame.image.load("textures/meadow1.jpg")
raytracer.rtClearColor(0.25,0.25,0.25)


#TEXTURES
marbleTexture = pygame.image.load("textures/marble.jpg")
columnTexture = pygame.image.load("textures/column.jpg")
marmolmossTexture = pygame.image.load("textures/marmolmoss.jpg")
baseColumnTexture = pygame.image.load("textures/basecolumn.jpg")
cealingTexture = pygame.image.load("textures/cealing1.jpg")
#MATERIALS
dirt = Material(diffuse=(0.866,0.631,0.368),spec=128, Ks=0.2)
mirror = Material(diffuse=(0.9,0.9,0.9),spec=64, Ks=0.2,matType=REFLECTIVE)
marble = Material(texture=marbleTexture)
glass = Material(diffuse=(0.9,0.9,0.9),spec=64, Ks=0.1, ior=1.5, matType=TRANSPARENT)
pinkGlass = Material(diffuse=(1,0.784,0.866),spec=64, Ks=0.1, ior=1.5, matType=TRANSPARENT)

column = Material(texture=columnTexture)
marmolmoss = Material(texture=marmolmossTexture)
base = Material(texture=baseColumnTexture)
cealing = Material(texture=cealingTexture)

#EXTRAS
raytracer.scene.append(Oval(position=(0,0,-12), radii = [0.5,1,1], material=marble))
raytracer.scene.append(Triangle(verts=[(0,0,-10),(-1,1.5,-10),(1,1.5,-10)],material=pinkGlass))
raytracer.scene.append(Cylinder(position=(0,-1.2,-12), radius=0.3, height=1.25, material=column))
raytracer.scene.append(Sphere(position=(0,-1,-3),radius= 0.4 ,material=glass))

#COLUMNS
raytracer.scene.append(Cylinder(position=(1.2,0,-10), radius=0.3, height=3, material=column))
raytracer.scene.append(Cylinder(position=(-1.2,0,-10), radius=0.3, height=3, material=column))
raytracer.scene.append(Cylinder(position=(2.5,0,-12), radius=0.3, height=3.5, material=column))
raytracer.scene.append(Cylinder(position=(-2.5,0,-12), radius=0.3, height=3.5, material=column))
raytracer.scene.append(Cylinder(position=(3.5,0,-14), radius=0.3, height=4, material=column))
raytracer.scene.append(Cylinder(position=(-3.5,0,-14), radius=0.3, height=4, material=column))

#CEILING
raytracer.scene.append(Cylinder(position=(0,2.4,-12), radius=3.5, height=1.4, material=cealing))
raytracer.scene.append(Cylinder(position=(0,2.4,-12), radius=3.2, height=1.4, material=column))
raytracer.scene.append(Cylinder(position=(0,2.6,-12), radius=3.6, height=0.5, material=marble))
raytracer.scene.append(AABB(position=(1.3,3.3,-10),size=(0.7,1,0.65),material=marmolmoss))
raytracer.scene.append(AABB(position=(3.2,4,-13),size=(0.7,1,0.65),material=marmolmoss))
raytracer.scene.append(AABB(position=(-1.3,3.3,-10),size=(0.7,1,0.65),material=marmolmoss))
raytracer.scene.append(AABB(position=(-3.2,4,-13),size=(0.7,1,0.65),material=marmolmoss))
raytracer.scene.append(Sphere(position=(0,4,-12),radius= 1.5 ,material=marmolmoss))

#COLUMN BASES
raytracer.scene.append(AABB(position=(1.2,1.65,-10),size=(0.7,0.5,0.65),material=base))
raytracer.scene.append(AABB(position=(-1.2,1.65,-10),size=(0.7,0.5,0.65),material=base))
raytracer.scene.append(AABB(position=(1.2,-1.65,-10),size=(0.7,0.5,0.65),material=base))
raytracer.scene.append(AABB(position=(-1.2,-1.65,-10),size=(0.7,0.5,0.65),material=base))

raytracer.scene.append(AABB(position=(0,-1.95,-12),size=(0.7,0.5,0.65),material=base))
raytracer.scene.append(AABB(position=(2.5,1.95,-12),size=(0.7,0.5,0.65),material=base))
raytracer.scene.append(AABB(position=(-2.5,1.95,-12),size=(0.7,0.5,0.65),material=base))
raytracer.scene.append(AABB(position=(2.5,-1.95,-12),size=(0.7,0.5,0.65),material=base))
raytracer.scene.append(AABB(position=(-2.5,-1.95,-12),size=(0.7,0.5,0.65),material=base))

raytracer.scene.append(AABB(position=(3.5,2.1,-14),size=(0.7,0.5,0.65),material=base))
raytracer.scene.append(AABB(position=(-3.5,2.1,-14),size=(0.7,0.5,0.65),material=base))
raytracer.scene.append(AABB(position=(3.5,-2.32,-14),size=(0.7,0.5,0.65),material=base))
raytracer.scene.append(AABB(position=(-3.5,-2.32,-14),size=(0.7,0.5,0.65),material=base))

#BASE
raytracer.scene.append(AABB(position=(0,-2.4,-12),size=(7,0.25,1),material=marmolmoss))
raytracer.scene.append(AABB(position=(0,-2.65,-12),size=(8,0.25,1),material=marmolmoss))
raytracer.scene.append(AABB(position=(0,-2.80,-12),size=(9,0.25,1),material=marmolmoss))
raytracer.scene.append(AABB(position=(0,-3.05,-12),size=(10,0.25,1),material=marmolmoss))

#LIGHTS
raytracer.lights.append(AmbientLight(intensity=0.5, color=(0.937,0.137,0.235)))
raytracer.lights.append(DirectionalLight(direction=(-1,-1.4,-1), intensity=0.7, color=(0.941,0.501,0.501)))
raytracer.lights.append(DirectionalLight(direction=(1,-2,-1), intensity=0.3, color=(1,0.854,0.725)))
raytracer.lights.append(PointLight(point=(-1.35,3.3,-10),intensity=0.7,color=(0.839,0.156,0.156)))
raytracer.lights.append(PointLight(point=(-3.2,3.3,-10),intensity=0.7,color=(0.839,0.156,0.156)))

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

rect = pygame.Rect(0, 0, width, height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "result.png")

pygame.quit()
#1:31