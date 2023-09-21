class Material(object):
    def __init__(self, diffuse = (1,1,1), spec = 1.0, Ks = 0.01):
        self.diffuse = diffuse
        self.spec = spec #determines how perfect will be a surface
        self.Ks = Ks #specular coeficent