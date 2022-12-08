import VertexTable
import Button
import pygame

SliderNob = pygame.image.load("./../Images/SliderNob.png").convert_alpha()
        

def ShowVertices(screen, projectedPoints):
    
    buttonList = []
    for i in range (len(projectedPoints)):
        buttonList.append(Button.Button(projectedPoints[i][0], projectedPoints[i][1], SliderNob, 0.2))
    
    for i in range (len(projectedPoints)):
        buttonList[i].draw(screen)