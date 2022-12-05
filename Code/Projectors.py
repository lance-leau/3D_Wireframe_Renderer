import VertexTable
import pygame

class Projectors():
    def __init__(self, vertexTable, focalLen, edgeTable, offset = (255, 255)):
        temp = []
        for i in range(len(vertexTable.VertexTable)):
            temp.append(self.ProjectPoint(vertexTable.VertexTable[i][0], vertexTable.VertexTable[i][1], vertexTable.VertexTable[i][2], focalLen, offset))
        self.projectedPoints = temp
        self.EdgeTable = edgeTable
        
    def ProjectPoint(self, x, y, z, focalLen, offset):
        Xprojected = ((focalLen * x) / (focalLen + z)) + offset[0]
        Yprojected = (focalLen * y) / (focalLen + z) + offset[1]
        return (Xprojected, Yprojected)
    
    def DrawShape(self, color, screen):
        for i in range(len(self.EdgeTable)):
            point1 = self.projectedPoints[self.EdgeTable[i][0]]
            point2 = self.projectedPoints[self.EdgeTable[i][1]]
            pygame.draw.line(screen, color, point1, point2, 4)