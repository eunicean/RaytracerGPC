import meth
#function reflectVector,refractVector and totalInternalReflection is in library meth
class Light(object):
    def __init__(self, intensity = 1, color = (1,1,1), lightType = "None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType

    def getLightColor(self):
        return [self.color[0]*self.intensity,
                self.color[0]*self.intensity,
                self.color[0]*self.intensity]
    
    def getDiffuseColor(self, intercept):
        return None
    
    def getSpecularColor(self, intercept, viewPos):
        return None

class AmbientLight(Light):
    def __init__(self, intensity=1, color=(1, 1, 1)):
        super().__init__(intensity, color, "Ambient")

class DirectionalLight(Light):
    def __init__(self, direction = (0,-1,0), intensity=1, color=(1, 1, 1)):
        self.direction = meth.normalizeVector(direction)
        super().__init__(intensity, color, "Directional")

    def getDiffuseColor(self, intercept):
        dir = [i*-1 for i in self.direction]
        intensity = meth.dotProd(intercept.normal, dir) * self.intensity
        intensity = max(0,min(1,intensity))
        intensity *= 1 - intercept.obj.material.Ks
        return [(i*intensity) for i in self.color]
    
    def getSpecularColor(self, intercept, viewPos):
        dir = [i*-1 for i in self.direction]

        reflect = meth.reflectVector(intercept.normal,dir)
        viewDir = meth.substractionVectors(viewPos,intercept.point)
        viewDir = meth.normalizeVector(viewDir)

        specIntensity = max(0,meth.dotProd(viewDir,reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity

        specColor = [(i*specIntensity) for i in self.color]
        return specColor
    
class PointLight(Light):
    def __init__(self, point=(0,0,0),intensity=1, color=(1, 1, 1)):
        self.point = point
        super().__init__(intensity, color, "Point")

    def getDiffuseColor(self, intercept):
        dir = meth.substractionVectors(self.point,intercept.point)
        R = meth.magnitudOfVector(dir)
        dir = meth.normalizeWithMagnitud(dir,R)

        intensity = meth.dotProd(intercept.normal, dir) * self.intensity
        intensity *= 1 - intercept.obj.material.Ks

        # Ley de cuadrados inversos
        # If = Intensity / R^2
        # R is the distance between intersect point and the point light
        if R != 0:
            intensity /= R**2
        intensity = max(0,min(1,intensity))

        return [(i*intensity) for i in self.color]
    
    def getSpecularColor(self, intercept, viewPos):
        dir = meth.substractionVectors(self.point,intercept.point)
        R = meth.magnitudOfVector(dir)
        dir = meth.normalizeWithMagnitud(dir,R)

        reflect = meth.reflectVector(intercept.normal,dir)
        viewDir = meth.substractionVectors(viewPos,intercept.point)
        viewDir = meth.normalizeVector(viewDir)

        specIntensity = max(0,meth.dotProd(viewDir,reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity
        if R != 0:
            specIntensity /= R**2
        
        specIntensity = max(0,min(1,specIntensity))

        specColor = [(i*specIntensity) for i in self.color]
        return specColor