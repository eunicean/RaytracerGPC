import math
import meth
import random
import pygame
from materials import *
from lights import *

MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()
        
        self.scene = []
        self.lights = []

        self.camPosition = [0,0,0]

        self.rtViewPort(0,0,self.width,self.height)
        self.rtProyection()

        self.rtColor(1,1,1)
        self.rtClearColor(0,0,0)
        self.rtClear()

        self.envMap = None

    def rtViewPort(self, posX,posY,width,height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height

    def rtProyection(self,fov=60,n=0.1):
        #fov - viewing angle
        #n   - nearplane value
        aspectRatio = self.vpWidth / self.vpHeight
        self.nearPlane = n
        self.topEdge = math.tan((fov*math.pi/180)/2) * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio

    def rtClearColor(self, r,g,b):
        #valores de 0 a 1
        self.clearColor = (r*255,
                           g*255,
                           b*255)

    def rtClear(self):
        #valores de 0 a 255
        self.screen.fill(self.clearColor)
        
    def rtColor(self, r,g,b):
        self.currColor = (r*255,
                          g*255,
                          b*255)

    def rtPoint(self, x,y, color = None):
        y = self.height - y
        if(0<=x<self.width) and (0<=y<self.height):
            if color != None:
                color = (int(color[0]*255),
                         int(color[1]*255),
                         int(color[2]*255))
                self.screen.set_at((x,y),color)
            else:
                self.screen.set_at((x,y),self.currColor)

    def rtCastRay(self,orig,dir, sceneObj = None, recursion = 0):
        if recursion >= MAX_RECURSION_DEPTH:
            return None
        
        depth = float('inf')
        intercept = None
        hit = None

        for obj in self.scene:
            if sceneObj != obj:
                intercept = obj.ray_intersect(orig,dir)
                if intercept != None:
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance
        
        return hit
    
    def rtRayColor(self, intercept, rayDirection,recursion=0):
        if intercept == None:
            if self.envMap:
                x = (math.atan2(rayDirection[2],rayDirection[0])/(2*math.pi) + 0.5) * self.envMap.get_width()
                y = math.acos(rayDirection[1])/math.pi * self.envMap.get_height()
                envColor = self.envMap.get_at((int(x),int(y)))

                return [envColor[i]/255 for i in range(3)]

            else:
                return None
        
        #Phong reflection model
        # LightColor = Ambient + Difusse + Specular
        # FinalColor = SurfaceColor * LightColor

        material = intercept.obj.material

        surfaceColor = intercept.obj.material.diffuse

        if material.texture and intercept.texcoords:
            tX = intercept.texcoords[0] * material.texture.get_width()
            tY = intercept.texcoords[1] * material.texture.get_height()
            texColor = material.texture.get_at((int(tX),int(tY)))
            texColor = [i/255 for i in texColor]
            surfaceColor = [surfaceColor[i] * texColor[i] for i in range(3)]

        reflectColor = [0,0,0]
        refractColor = [0,0,0]
        ambientColor = [0,0,0]
        diffuseColor = [0,0,0]
        specularColor = [0,0,0]
        finalColor = [0,0,0]

        if material.matType == OPAQUE:
            for light in self.lights:
                if light.lightType == "Ambient":
                    ambientColor = meth.additionVectors(ambientColor,light.getLightColor())
                else:
                    lightDir = None
                    if light.lightType == "Directional":
                        lightDir = [i*-1 for i in light.direction]
                    elif light.lightType == "Point":
                        lightDir = meth.substractionVectors(light.point, intercept.point)
                        lightDir = meth.normalizeVector(lightDir)
                        
                    shadowIntersect = self.rtCastRay(intercept.point,lightDir,intercept.obj)

                    if shadowIntersect == None:
                        diffuseColor = meth.additionVectors(diffuseColor,light.getDiffuseColor(intercept))
                        specularColor = meth.additionVectors(specularColor,light.getSpecularColor(intercept,self.camPosition))

        elif material.matType == REFLECTIVE:
            direction = [i*-1 for i in rayDirection]
            reflect = meth.reflectVector(intercept.normal, direction)
            reflectIntercept = self.rtCastRay(intercept.point, reflect, intercept.obj, recursion+1)
            reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion+1)
            
            for light in self.lights:
                if light.lightType != "Ambient":
                    lightDir = None
                    if light.lightType == "Directional":
                        lightDir = [i*-1 for i in light.direction]
                    elif light.lightType == "Point":
                        lightDir = meth.substractionVectors(light.point, intercept.point)
                        lightDir = meth.normalizeVector(lightDir)

                    shadowIntersect = self.rtCastRay(intercept.point,lightDir,intercept.obj)
                    
                    if shadowIntersect == None:
                        specularColor = meth.additionVectors(specularColor,light.getSpecularColor(intercept,self.camPosition))
        elif material.matType == TRANSPARENT:
            outside = meth.dotProd(rayDirection, intercept.normal) < 0
            bias = meth.multiplyValueAndVector(0.001,intercept.normal)  #vector
            
            direction = [i*-1 for i in rayDirection]
            reflect = meth.reflectVector(intercept.normal, direction)
            reflectOrig = meth.additionVectors(intercept.point, bias) if outside else meth.substractionVectors(intercept.point, bias)
            reflectIntercept = self.rtCastRay(reflectOrig,reflect,None, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion+1)

            if not meth.totalInternalReflection(intercept.normal, rayDirection,1.0,material.ior):
                refract = meth.refractVector(intercept.normal,rayDirection,1.0,material.ior)
                refractOrig = meth.substractionVectors(intercept.point, bias) if outside else meth.additionVectors(intercept.point, bias)
                refractIntercept = self.rtCastRay(refractOrig,refract,None, recursion + 1)
                refractColor = self.rtRayColor(refractIntercept, refract, recursion+1)

                Kr, Kt = meth.fresnel(intercept.normal,rayDirection, 1.0,material.ior)
                reflectColor = meth.multiplyValueAndVector(Kr,reflectColor)
                refractColor = meth.multiplyValueAndVector(Kt,refractColor)

        lightColor = meth.additionVectors(meth.additionVectors(meth.additionVectors(meth.additionVectors(ambientColor,diffuseColor),specularColor),reflectColor),refractColor)
        surfaceColor = list(surfaceColor)
        finalColor = [min(1, value) for value in meth.mIVV(surfaceColor,lightColor)]
        return finalColor


    def rtRender(self):
        indices = [(i,j)for i in range(self.vpWidth) for j in range(self.vpHeight)]
        random.shuffle(indices)

        for i,j in indices:
            x = i + self.vpX
            y = j + self.vpY
            if 0<=x<self.width and 0<=y<self.height:
                    #Pass window coords to NDC coords (normalized coords) (-1 to 1)
                    Px =((x + 0.5 - self.vpX) / self.vpWidth)*2 - 1
                    Py =((y + 0.5 - self.vpY) / self.vpHeight)*2 - 1

                    Px *= self.rightEdge
                    Py *= self.topEdge

                    #create a ray
                    direction = (Px, Py, -self.nearPlane)
                    direction = meth.normalizeVector(direction)

                    intercept = self.rtCastRay(self.camPosition,direction)
                    rayColor = self.rtRayColor(intercept, direction)

                    if rayColor !=None:
                        self.rtPoint(x,y,rayColor)
                        pygame.display.flip()

