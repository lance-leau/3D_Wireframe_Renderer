import VertexTable
import Button
import pygame

SliderNob = pygame.image.load("./../Images/SliderNob.png").convert_alpha()
        

class DiyShape():
    def __init__(self, vertexTable):
        self.vertexTable = vertexTable
        self.SelectedA = 0
        self.SelectedB = 0
        self.currPoint = 0
    
    def AddEdge(self, edgeTable):
        edgeTable.append([self.SelectedA, self.SelectedB])
    
    def ShowVertices(self, screen, projectedPoints):
        for i in range (len(projectedPoints)):
            if i == self.SelectedA:
                pygame.draw.circle(screen, (255, 0, 0), projectedPoints[i], 3, 6)
            elif i == self.SelectedB:
                pygame.draw.circle(screen, (0, 0, 255), projectedPoints[i], 3, 6)
            else:
                pygame.draw.circle(screen, (255, 255, 255), projectedPoints[i], 3, 6)