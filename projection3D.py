import pygame # used to display the wireframe
import sys
from pygame.locals import *
import math
import numpy


EdgeTable = []
(temp1, temp2, temp3) = ([], [], [])
if len(sys.argv) == 1 or "0" in sys.argv:
    # je sais pas comment appeler cet objet
    temp1 = [[11, 5],  [5, 17],  [17, 7],  [7, 15], [25, 21], [15, 3] ,
             [19, 21], [3, 9],   [25, 23], [1, 3],  [23, 19], [1, 5]  ,
             [19, 11], [5, 7],   [11, 23], [7, 3],  [23, 17], [17, 25],
             [25, 15], [15, 21], [21, 9],  [9, 19], [9, 1],   [1, 11] ]
if "1" in sys.argv:
    # pyramide
    temp2 = [[0, 6], [6, 8], [8, 2], [2, 0], [0, 22], [6, 22], [2, 22], [8, 22]]
if "2" in sys.argv:
    # cube
    temp3 = [[0, 6], [6, 8], [8, 26], [26, 20], [20, 18], [18, 0], [18, 24], [24, 6], [24, 26], [2, 0], [2, 8], [2, 20]]
            
EdgeTable.extend(temp1)
EdgeTable.extend(temp2)
EdgeTable.extend(temp3)

offsetScreen = (300, 275)
turnSpeed = 0.03
distanceFromScreen = 250
screenSize = (600, 600)
ShapeSize = 50

shapeOffset = -0.12

#A  -> 0     B -> 1     C -> 2    D  -> 3     E -> 4     F -> 5     G  -> 6     H -> 7     I -> 8
#A1 -> 9    B1 -> 10   C1 -> 11   D1 -> 12   E1 -> 13   F1 -> 14     G1 -> 15   H1 -> 16   I1 -> 17
#A2 -> 18   B2 -> 19   C2 -> 20   D2 -> 21   E2 -> 22   F2 -> 23     G2 -> 24   H2 -> 25   I2 -> 26



VertexTable = [ (0, 0, 0), (0, 1, 0), (0, 2, 0),
                (1, 0, 0), (1, 1, 0), (1, 2, 0),
                (2, 0, 0), (2, 1, 0), (2, 2, 0),
                (0, 0, 1), (0, 1, 1), (0, 2, 1),
                (1, 0, 1), (1, 1, 1), (1, 2, 1),
                (2, 0, 1), (2, 1, 1), (2, 2, 1), 
                (0, 0, 2), (0, 1, 2), (0, 2, 2),
                (1, 0, 2), (1, 1, 2), (1, 2, 2),
                (2, 0, 2), (2, 1, 2), (2, 2, 2)]

def lowerShape(offset):
    temp2 = []
    for i in range(len(VertexTable)):
        temp1 = []
        temp1.append(VertexTable[i][0] -1)
        temp1.append(VertexTable[i][1] -1)
        temp1.append(VertexTable[i][2] -1 + offset)
        temp2.append(temp1)
    return temp2
VertexTable = lowerShape(shapeOffset)


# flip around and set size
temp2 = []
for i in range(len(VertexTable)):
    temp1 = []
    temp1.append(VertexTable[i][0] * ShapeSize)
    temp1.append(VertexTable[i][2] * -ShapeSize)
    temp1.append(VertexTable[i][1] * ShapeSize)
    temp2.append(temp1)
VertexTable = temp2

RotateMatrixX = [[               1,                   0,                   0 ],
                 [               0, math.cos(turnSpeed), -math.sin(turnSpeed)],
                 [               0, math.sin(turnSpeed),  math.cos(turnSpeed)]]

RotateMatrixY = [[ math.cos(turnSpeed),               0, math.sin(turnSpeed)],
                 [                   0,               1,                   0],
                 [-math.sin(turnSpeed),               0, math.cos(turnSpeed)]]

RotateMatrixZ = [[ math.cos(turnSpeed), -math.sin(turnSpeed),               0],
                 [ math.sin(turnSpeed),  math.cos(turnSpeed),               0],
                 [                   0,                    0,               1]]

def RotateVertexTableX():
    rotMat = numpy.array(RotateMatrixX)
    for i in range(len(VertexTable)):
        point = numpy.array(VertexTable[i])
        rPoint = numpy.dot(rotMat, point)
        VertexTable[i] = rPoint
def RotateVertexTableY():
    rotMat = numpy.array(RotateMatrixY)
    for i in range(len(VertexTable)):
        point = numpy.array(VertexTable[i])
        rPoint = numpy.dot(rotMat, point)
        VertexTable[i] = rPoint
def RotateVertexTableZ():
    rotMat = numpy.array(RotateMatrixZ)
    for i in range(len(VertexTable)):
        point = numpy.array(VertexTable[i])
        rPoint = numpy.dot(rotMat, point)
        VertexTable[i] = rPoint


def ZoomVertexTable():
    for i in range(len(VertexTable)):
        temp = []
        for j in range(3):
            temp.append( VertexTable[i][j] *1.005)
        VertexTable[i] = temp

def Projection(x, y, z, focalLen, offset):
    Xprojected = ((focalLen * x) / (focalLen + z)) + offset[0]
    Yprojected = (focalLen * y) / (focalLen + z) + offset[1]
    return (Xprojected, Yprojected)

def GetProjectionFromVertexTable(table, focalLen, offset):
    ret = []
    for i in range(len(table)):
        ret.append(Projection(table[i][0], table[i][1], table[i][2], focalLen, offset))
    return ret



screen = pygame.display.set_mode(screenSize)

clock = pygame.time.Clock()
white = (255, 255, 255)
black = (0, 0, 0)
quit = False


def drawCube(color):
    for i in range(len(EdgeTable)):
        point1 = projectedPoints[EdgeTable[i][0]]
        point2 = projectedPoints[EdgeTable[i][1]]
        pygame.draw.line(screen, color, point1, point2, 4)

projectedPoints = GetProjectionFromVertexTable(VertexTable, distanceFromScreen, offsetScreen)
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
            sys.exit

    # delete previous lines:
    drawCube(black)

    # update points position:
    if "zoom" in sys.argv:
        ZoomVertexTable()
    if "x" in sys.argv:
        RotateVertexTableX()
    if "y" in sys.argv:
        RotateVertexTableY()
    if "z" in sys.argv:
        RotateVertexTableZ()

    # update projected points position:
    projectedPoints = GetProjectionFromVertexTable(VertexTable, distanceFromScreen, offsetScreen)

    # draw lines on canvas
    drawCube(white)
    
    # update the canvas
    pygame.display.update()
    clock.tick(30)

pygame.quit