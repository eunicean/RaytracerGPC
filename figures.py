import meth
class Shape(object):
    def __init__(self, position):
        self.position = position

    def ray_intersect(self, orig, dir):
        return False
    

class Sphere(Shape):
    def __init__(self, position,radius):
        self.radius = radius
        super().__init__(position)

    def ray_intersect(self, orig, dir):
        L = meth.substractionVectors(self.position, orig)
        lengthL = meth.magnitudOfVector(L) #previously the magnitude of L
        tca = meth.dotProd(L,dir)
        d = (lengthL ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return False
        
        thc = (self.radius**2 - d**2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return False

        return True