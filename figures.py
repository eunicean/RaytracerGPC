import meth
import math

class Intercept(object):
    def __init__(self, distance, point, normal, texcoords, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj

class Shape(object):
    def __init__(self, position,material):
        self.position = position
        self.material = material

    def ray_intersect(self, orig, dir):
        return None
    

class Sphere(Shape):
    def __init__(self, position,radius,material):
        self.radius = radius
        super().__init__(position,material)

    def ray_intersect(self, orig, dir):
        L = meth.substractionVectors(self.position, orig)
        lengthL = meth.magnitudOfVector(L) #previously the magnitude of L
        tca = meth.dotProd(L,dir)
        d = (lengthL ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None
        
        thc = (self.radius**2 - d**2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        P = meth.additionVectors(orig,meth.multiplyValueAndVector(t0,dir))
        normal = meth.substractionVectors(P,self.position)
        normal = meth.normalizeVector(normal)

        u = (math.atan2(normal[2],normal[0])/(2 * math.pi))+0.5
        v = math.acos(normal[1])/math.pi

        return Intercept(distance= t0,
                         point= P,
                         normal= normal,
                         texcoords= (u,v),
                         obj= self)
    
class Plane(Shape):
    def __init__(self, position, material, normal):
        self.normal = meth.normalizeVector(normal)
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        #Distancia = (planepPos - origRay) o normal) / (dirRay o normal1``)
        denom = meth.dotProd(dir,self.normal)

        if abs(denom) <= 0.0001:
            return None
        
        num = meth.dotProd(meth.substractionVectors(self.position,orig),self.normal)
        t = num/denom

        if t < 0:
            return None
        
        #P = O + D * t
        P = meth.additionVectors(orig,meth.multiplyValueAndVector(t,dir))

        return Intercept(distance= t,
                         point= P,
                         normal= self.normal,
                         texcoords= None,
                         obj= self)
    
class Disk(Plane):
    def __init__(self, position, material, normal, radius):
        self.radius = radius
        super().__init__(position, material, normal)

    def ray_intersect(self, orig, dir):
        planeIntersect = super().ray_intersect(orig,dir) #if does contact to the plane which it belongs

        if planeIntersect is None:
            return None
        
        contactDistance =  meth.substractionVectors(planeIntersect.point,self.position) #vector
        contactDistance = meth.magnitudOfVector(contactDistance)

        if contactDistance > self.radius:
            return None
        
        return Intercept(distance= planeIntersect.distance,
                         point= planeIntersect.point,
                         normal= self.normal,
                         texcoords= None,
                         obj= self)
    
class AABB(Shape):
    def __init__(self, position, material, size):
        super().__init__(position, material)

        self.planes = [ ]
        self.size = size

        #sides
        leftPlane =   Plane(meth.additionVectors(self.position,((-size[0])/2,0,0)),normal=(-1,0,0),material=material)
        rightPlane =  Plane(meth.additionVectors(self.position,(( size[0])/2,0,0)),normal=(1,0,0), material=material)
        bottomPlane = Plane(meth.additionVectors(self.position,(0,(-size[1])/2,0)),normal=(0,-1,0),material=material)
        topPlane =    Plane(meth.additionVectors(self.position,(0,( size[1])/2,0)),normal=(0,1,0), material=material)
        backPlane =   Plane(meth.additionVectors(self.position,(0,0,(-size[2])/2)),normal=(0,0,-1),material=material)
        frontPlane =  Plane(meth.additionVectors(self.position,(0,0,( size[2])/2)),normal=(0,0,1), material=material)

        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)

        #Bounds
        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]
        bias = 0.001
        for i in range(3):
            self.boundsMin[i] = self.position[i] - (bias + size[i]/2)
            self.boundsMax[i] = self.position[i] + (bias + size[i]/2)

    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')
        u = 0
        v = 0
        bias = 0.001

        for plane in self.planes:
            planeIntersect = plane.ray_intersect(orig, dir)
            if planeIntersect is not None:
                planePoint = planeIntersect.point
                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect

                                #genereta u and v
                                if abs(plane.normal[0]) > 0:#this is a left or right plane
                                    #whe are in X, we use the Y a Z to create the uvs
                                    u = (planePoint[1] - self.boundsMin[1])/(self.size[1] + bias*2)
                                    v = (planePoint[2] - self.boundsMin[2])/(self.size[2] + bias*2)
                                elif abs(plane.normal[1]) > 0:
                                    #whe are in Y, we use the X a Z to create the uvs
                                    u = (planePoint[0] - self.boundsMin[0])/(self.size[0] + bias*2)
                                    v = (planePoint[2] - self.boundsMin[2])/(self.size[2] + bias*2)
                                elif abs(plane.normal[2]) > 0:
                                    #whe are in Z, we use the Y a X to create the uvs
                                    u = (planePoint[0] - self.boundsMin[0])/(self.size[0] + bias*2)
                                    v = (planePoint[1] - self.boundsMin[1])/(self.size[1] + bias*2)

        if intersect is None: return None
        
        return Intercept(distance= t,
                         point= intersect.point,
                         normal= intersect.normal,
                         texcoords= (u,v),
                         obj= self)
    
# Help of chatGPT:
# https://chat.openai.com/share/806e6b97-c8c8-49a2-874f-cc1aa6c2b7a1
class Triangle(Shape):
    def __init__(self,material, verts): #In this, verts[0] = (x,y,z) will determine the position
        self.verts = verts #every value in verts is an (x,y,z)
        super().__init__(verts[0], material)

    def ray_intersect(self, orig, dir):
        edge1 = meth.substractionVectors(self.verts[1],self.verts[0])
        edge2 = meth.substractionVectors(self.verts[2],self.verts[0])
        normal = meth.normalizeVector(meth.prodCrossV(edge1,edge2))

        denom = meth.dotProd(normal,dir) #this is h and a combined
        if abs(denom) <= 0.001:
            return None

        # d = meth.dotProd(normal,self.verts[0])
        # n = meth.dotProd(normal,orig)
        
        scalingFactor = 1.0 / meth.dotProd(edge1, meth.prodCrossV(dir,edge2))
        d = meth.substractionVectors(orig, self.verts[0])
        u = scalingFactor * meth.dotProd(d, meth.prodCrossV(dir,edge2)) #barycentric coordinate 
        orientation = meth.prodCrossV(d, edge1)
        v = scalingFactor * meth.dotProd(dir, orientation)# barycentric coordinate 

        if u < 0.0 or u > 1.0:
            return None
        if v < 0.0 or u + v > 1.0:
            return None

        # At this point, we have a valid intersection
        t = scalingFactor * meth.dotProd(edge2, orientation)
        if t <= 0:
            return None

        # Compute the intersection point and return the result
        P = meth.additionVectors(orig, meth.multiplyValueAndVector(t, dir))

        return Intercept(distance=t,
                         point=P,
                         normal=normal,
                         texcoords=None,
                         obj=self)