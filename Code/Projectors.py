import VertexTable
import pygame

class Projectors():
    def __init__(self, vertexTable, focalLen, edgeTable, offset = (255, 255)):
        temp = []
        self.focalLen = focalLen
        for i in range(len(vertexTable.VertexTable)):
            temp.append(self.ProjectPoint(vertexTable.VertexTable[i][0], vertexTable.VertexTable[i][1], vertexTable.VertexTable[i][2], offset))
        self.projectedPoints = temp
        self.EdgeTable = edgeTable
        self.minFocalLen = 50
        self.maxFocalLen = 550
        
    def ProjectPoint(self, x, y, z, offset):
        Xprojected = ((self.focalLen * x) / (self.focalLen + z)) + offset[0]
        Yprojected = (self.focalLen * y) / (self.focalLen + z) + offset[1]
        return (Xprojected, Yprojected)
    
    def DrawShape(self, color, screen):
        for i in range(len(self.EdgeTable)):
            point1 = self.projectedPoints[self.EdgeTable[i][0]]
            point2 = self.projectedPoints[self.EdgeTable[i][1]]
            pygame.draw.line(screen, color, point1, point2, 4)
    
    def DrawPoints(self, points, screen, color):
        for point in points:
            pygame.draw.circle(screen, color, point, 1, 25)