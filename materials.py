OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material(object):
    def __init__(self, diffuse = (1,1,1), spec = 1.0, Ks = 0.01,ior = 1.0, texture = None, matType = OPAQUE):
        #ior: indice of refraction
        self.diffuse = diffuse
        self.spec = spec #determines how perfect will be a surface
        self.Ks = Ks #specular coeficent
        self.ior = ior
        self.texture = texture
        self.matType =  matType #tipo de material