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