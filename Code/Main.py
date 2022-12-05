# This project was made by Lancelot

import VertexTable, Projectors
import sys,  pygame
import Button

#create display window
screen = pygame.display.set_mode((1024, 576))
pygame.display.set_caption("3D Wire Frame Renderer")

screen.fill((33, 40, 48))

#load button images
nextShape = pygame.image.load('Images/NextShape.png').convert_alpha()
ToggleX = pygame.image.load('Images/ToggleX.png').convert_alpha()
ToggleY = pygame.image.load('Images/ToggleY.png').convert_alpha()
ToggleZ = pygame.image.load('Images/ToggleZ.png').convert_alpha()
ZoomIn = pygame.image.load('Images/ZoomIn.png').convert_alpha()
ZoomOut = pygame.image.load('Images/ZoomOut.png').convert_alpha()

#create button instances
nextShapeButton = Button.Button(21, 39, nextShape, 1)
ToggleXButton = Button.Button(34, 167, ToggleX, 1)
ToggleYButton = Button.Button(34, 256, ToggleY, 1)
ToggleZButton = Button.Button(34, 345, ToggleZ, 1)
ZoomInButton = Button.Button(34, 447, ZoomIn, 1)
ZoomOutButton = Button.Button(137, 447, ZoomOut, 1)

def launchWindow():
    # Set rotation to false
    rotateX = False 
    rotateY = False 
    rotateZ = False 
    # set offset
    offset = (640, 288)
    vertexTable = VertexTable.Vertexes(VertexTable.vertexTable, 0)
    projection = Projectors.Projectors(vertexTable, 250, vertexTable.EdgeTable, offset)
    pygame.draw.rect(screen, (69, 74, 79), pygame.Rect(0, 0, 256, 576))
    
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                sys.exit
        
        # Draw buttons on window, check if clicked
        if nextShapeButton.draw(screen):
            vertexTable.CurrShape += 1
            if (vertexTable.CurrShape > 2):
                vertexTable.CurrShape = 0
            vertexTable.EdgeTable = vertexTable.GetEdgeTable()
        
        if ToggleXButton.draw(screen):
            rotateX = not rotateX
        if ToggleYButton.draw(screen):
            rotateY = not rotateY
        if ToggleZButton.draw(screen):
            rotateZ = not rotateZ
        
        if ZoomInButton.draw(screen):
            vertexTable.Zoom(0.1)
        if ZoomOutButton.draw(screen):
            vertexTable.Zoom(-0.1)
        
        # Earase previous frame
        projection.DrawShape((33, 40, 48), screen)
        
        # Modify the VertexTable if needed
        if rotateX:
            vertexTable.RotateVertexTableX()
        if rotateY:
            vertexTable.RotateVertexTableY()
        if rotateZ:
            vertexTable.RotateVertexTableZ()
        
        # Update the projection
        projection = Projectors.Projectors(vertexTable, 250, vertexTable.EdgeTable, offset)      
        
        # Draw new frame
        projection.DrawShape((255, 255, 255), screen)
        
        # Update the canvas
        pygame.display.update()
        pygame.time.Clock().tick(30)
    pygame.quit

launchWindow()