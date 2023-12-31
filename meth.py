# AUTHOR:   Eunice Anahi Mata Ixcayau
# CARNET:   21231
# PROF:     Carlos Alonso
# CLASS:    Computer Graphics
# SECTION:  20

#matrices

import math
import numpy

def multiplymatrix(A,B):
    
    if len(A[0]) == len(B):
        C = [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]

        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(A[0])):
                    C[i][j] += A[i][k] * B[k][j]

        return C
    else:
        return None

def multiplyMatrixVector(A,B):
    # A es el vector
    # B es la matriz
    if len(A) == len(B):
        C = [0,0,0,0]

        for i in range(len(A)):
            for j in range(len(B[0])):
                C[i] += B[i][j] * A[j]

        return C
    else:
        return None
    

def barycentrinCoords(A,B,C,P):

    areaPBC = (B[1]- C[1]) * (P[0]-C[0]) + (C[0] - B[0]) * (P[1]-C[1])
    areaACP = (C[1]- A[1]) * (P[0]-C[0]) + (A[0] - C[0]) * (P[1]-C[1])
    areaABC = (B[1]- C[1]) * (A[0]-C[0]) + (C[0] - B[0]) * (A[1]-C[1])

    # areaPBC = abs((P[0]*B[1] + B[0]*C[1] + C[0]*P[1]) - 
    #               (P[1]*B[0] + B[1]*C[0] + C[1]*P[0]))
    # areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
    #               (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))
    # areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
    #               (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    if areaABC ==0:
        return None

    u = areaPBC / areaABC
    v = areaACP / areaABC
    w = 1-u-v

    if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and math.isclose(u+v+w,1.0):
        return u,v,w
    else:
        return None

def getMatrixMinor(matrix,i,j):
    return [row[:j] + row[j+1:] for row in (matrix[:i]+matrix[i+1:])] #minor matrix

def matrixDeterm(matrix):
    if len(matrix) == 2: #case for 2x2 matrix
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    determinant = 0
    for c in range(len(matrix)):
        determinant += ((-1)**c)*matrix[0][c]*matrixDeterm(getMatrixMinor(matrix,0,c))
    return determinant

def invMatrix(mx):
    det = matrixDeterm(mx)
    if(det==0):
        print('Determinant is zero')
        return
    if len(mx) == 2: #case for 2x2 matrix 
        return [[mx[1][1]/det, -1*mx[0][1]/det],
                [-1*mx[1][0]/det, mx[0][0]/det]]
    cofactors = []
    for i in range(len(mx)):
        cofactRow = []
        for j in range(len(mx)):
            minorValue = getMatrixMinor(mx,i,j)
            cofactRow.append(((-1)**(i+j)) * matrixDeterm(minorValue))
        cofactors.append(cofactRow)
        
    inverse = list(map(list,zip(*cofactors))) #gets the transpose of the matrix
    for i in range(len(inverse)):
        for j in range(len(inverse)):
            inverse[i][j] = inverse[i][j]/det
    return inverse

def substractionVectors(a,b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def prodCrossV(a,b):
    cross_product = [a[1] * b[2] - a[2] * b[1],
                     a[2] * b[0] - a[0] * b[2],
                     a[0] * b[1] - a[1] * b[0]]
    return cross_product

def normalizeVector(vector):
    vectorList = list(vector)
    magnitude = magnitudOfVector(vector)
    if magnitude == 0: #error if magnitude is 0
        print("Unable to normalize")
    
    normVector = [e / magnitude for e in vectorList]
    return tuple(normVector)

def magnitudOfVector(vector): #core proceess for the funcionality of the narmalization of a vector
    vectorList = list(vector)
    magnitude = math.sqrt(sum(e ** 2 for e in vectorList))
    return magnitude

def normalizeWithMagnitud(vector, magnitude):
    vList = list(vector)
    if magnitude == 0: #error if magnitude is 0
        print("Unable to normalize")
    
    normVector = [e / magnitude for e in vList]
    return tuple(normVector)
     
def dotProd(v1, v2):
    return sum(x*y for x, y in zip(v1, v2))

def multiplyValueAndVector(value,vector):
    vectorList = list(vector)
    return [value*v for v in vectorList]

def additionVectors(a,b):
    return [va+vb for va,vb in zip(a,b)]

def mIVV(a,b): 
    #multiplication of Individual Values of a Vector
    return [va*vb for va,vb in zip(a,b)]

def reflectVector(normal, direction):
    reflect = 2 * dotProd(normal,direction)
    reflect = multiplyValueAndVector(reflect, normal)
    reflect = substractionVectors(reflect, direction)
    return reflect

def totalInternalReflection(incident, normal, n1, n2): 
    #returns true or false if there is total internal reflection
    #incident is a vector
    #normal is a vector
    #n1 is mayor IOR
    #n2 is minor IOR

    c1 = dotProd(normal, incident)
    if c1 < 0:
        c1 = -1 * c1
    else:
        n1,n2 = n2,n1

    if n1 < n2:
        return False

    theta1 = math.acos(c1)  #angulo incidente
    thetaC = math.asin(n2/n1) #angulo critico

    return theta1>=thetaC # true if there is total internal reflection

def refractVector(normal, incident, n1,n2):
    #Snell's law
    c1 = dotProd(normal, incident)
    if c1 < 0:
        c1 = -1 * c1
    else:
        normal = [i*-1 for i in normal]
        n1,n2 = n2,n1
    
    n = n1/n2
    # normal * sqrt(1-n^2 * sin^2(ang))
    c2 = (1-n**2 * (1 - c1**2))**0.5

    # n*incident
    Ta = multiplyValueAndVector(n, incident)
    # (n*c1-c2)*normal
    v = n*c1-c2
    Tb = multiplyValueAndVector(v,normal)
    # n*incident + (n*c1-c2)*normal
    T = additionVectors(Ta,Tb)
    T = normalizeVector(T)
    return T

def fresnel(normal, incident,n1,n2):
    #frenell's ecuation
    c1 = dotProd(normal, incident)
    if c1 < 0:
        c1 = -1 * c1
    else:
        normal = [i*-1 for i in normal]
        n1,n2 = n2,n1

    s2 = (n1*(1-c1**2)**0.5)/n2  #seno of the exit angle
    c2 = (1-s2**2)**0.5

    F1 = (((n2*c1) - (n1*c2))/((n2*c1) + (n1*c2)))**2
    F2 = (((n1*c2) - (n2*c1))/((n1*c2) + (n2*c1)))**2

    Kr = (F1+F2)/2
    Kt = 1- Kr
    return Kr, Kt