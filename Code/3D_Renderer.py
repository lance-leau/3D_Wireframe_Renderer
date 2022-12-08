# This project was made by Lancelot

from cmath import isclose
import VertexTable, Projectors
import sys,  pygame
import Button

#create display window
screen = pygame.display.set_mode((1024, 576))
pygame.display.set_caption("3D Wire Frame Renderer")

import DiyShape

screen.fill((33, 40, 48))
#load button images "C:\Users\lance\OneDrive\Documents\Python\3D_Renderer\Images\shape1.png"
shape1 = pygame.image.load("./../Images/shape1.png").convert_alpha()
shape2 = pygame.image.load("./../Images/shape2.png").convert_alpha()
shape3 = pygame.image.load("./../Images/shape3.png").convert_alpha()
shape4 = pygame.image.load("./../Images/CustomShape.png").convert_alpha()
nextShape = pygame.image.load("./../Images/NextShape.png").convert_alpha()
prevShape = pygame.image.load("./../Images/PrevShape.png").convert_alpha()
RotateXYZ = pygame.image.load("./../Images/RotateXY.png").convert_alpha()
CheckedBox = pygame.image.load("./../Images/PointToggleSelected.png").convert_alpha()
UncheckedBox = pygame.image.load("./../Images/PointToggleUnselected.png").convert_alpha()
SliderBar = pygame.image.load("./../Images/SliderBar.png").convert_alpha()
SliderNob = pygame.image.load("./../Images/SliderNob.png").convert_alpha()
CustomShapeUI = pygame.image.load("./../Images/CustomShapeUI.png").convert_alpha()
AddEdge = pygame.image.load("./../Images/AddEdge.png").convert_alpha()
UndoButton = pygame.image.load("./../Images/Undo.png").convert_alpha()
SliderLegend = pygame.image.load("./../Images/SliderLegends.png").convert_alpha()


#create button instances
nextShapeButton = Button.Button(178, 29, nextShape, 1)
prevShapeButton = Button.Button(27, 29, prevShape, 1)
ToggleXButton = Button.Check(84, 175, UncheckedBox, CheckedBox, 1)
ToggleYButton = Button.Check(171, 175, UncheckedBox, CheckedBox, 1)
SizeSlider = Button.Slider(355, 549, SliderBar, SliderNob)
FOVSlider = Button.Slider(559, 549, SliderBar, SliderNob)
TurnSpeedSlider = Button.Slider(767, 549, SliderBar, SliderNob)
dragPad = Button.Tactile(256, 0, 768, 511)
nextVertex = Button.Button(144, 305, nextShape, 1)
prevVertex = Button.Button(61, 305, prevShape, 1)
AddEdge = Button.Button(35, 461, AddEdge, 1)
UndoButton = Button.Button(35, 513, UndoButton, 1)
CustomShapePointA = Button.Check(168, 376, UncheckedBox, CheckedBox, 1, True)
CustomShapePointB = Button.Check(168, 417, UncheckedBox, CheckedBox, 1)


# Launch the projection
def launchWindow():
    # Set default rotation speed
    rotationSpeed = 0.015
    
    # Temp
    prevZoom = 0
    prevDragX = 0
    prevDragY = 0
    prevDragZ = 0
        
    # Set offset
    offset = (640, 288)
    
    vertexTable = VertexTable.Vertices(VertexTable.vertexTable, 0)
    projection = Projectors.Projectors(vertexTable, 250, vertexTable.EdgeTable, offset)
    pygame.draw.rect(screen, (69, 74, 79), pygame.Rect(0, 0, 256, 576))
    diyShape = DiyShape.DiyShape(vertexTable)
    
    # Main loop
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                sys.exit
                
        # Earase previous frame ------------------------------------------------------------------------------------------------------------
        pygame.draw.rect(screen, (33, 40, 48), pygame.Rect(256, 0, 768, 576))
        pygame.draw.rect(screen, (69, 74, 79), pygame.Rect(0, 0, 256, 576))
        # Add Shape ------------------------------------------------------------------------------------------------------------------------
        # Add UI ---------------------------------------------------------------------------------------------------------------------------
        # Show current shape on top left corner
        makeYourOwnShape = False
        if vertexTable.CurrShape == 0:
            screen.blit(shape1, (88, 15))
        elif vertexTable.CurrShape == 1:
            screen.blit(shape2, (88, 15))
        elif vertexTable.CurrShape == 2:
            screen.blit(shape3, (88, 15))
        elif vertexTable.CurrShape == 3:
            makeYourOwnShape = True
        else:
            makeYourOwnShape = True
        
        # If designing a new shape, open UI
        if makeYourOwnShape:
            screen.blit(CustomShapeUI, (20, 247))
            if CustomShapePointA.draw(screen):
                CustomShapePointB.state = False
                diyShape.currPoint = 0
            if CustomShapePointB.draw(screen):
                CustomShapePointA.state = False
                diyShape.currPoint = 1
            if prevVertex.draw(screen):
                if diyShape.currPoint == 0:
                    diyShape.SelectedA -= 1
                    if diyShape.SelectedA < 0:
                        diyShape.SelectedA = 26
                else:
                    diyShape.SelectedB -= 1
                    if diyShape.SelectedB < 0:
                        diyShape.SelectedB = 26
            if nextVertex.draw(screen):
                if diyShape.currPoint == 0:
                    diyShape.SelectedA += 1
                    if diyShape.SelectedA > 26:
                        diyShape.SelectedA = 0
                else:
                    diyShape.SelectedB += 1
                    if diyShape.SelectedB > 26:
                        diyShape.SelectedB = 0
            if AddEdge.draw(screen):
                diyShape.AddEdge(vertexTable.EdgeTable)
            if UndoButton.draw(screen):
                if len(projection.EdgeTable) != 0:
                    projection.EdgeTable.pop()
        
        # Draw buttons on window, check if clicked
        if nextShapeButton.draw(screen):
            vertexTable.CurrShape += 1
            if (vertexTable.CurrShape > 3):
                vertexTable.CurrShape = 0
            vertexTable.EdgeTable = vertexTable.GetEdgeTable()
        
        if prevShapeButton.draw(screen):
            vertexTable.CurrShape -= 1
            if (vertexTable.CurrShape < 0):
                vertexTable.CurrShape = 3
            vertexTable.EdgeTable = vertexTable.GetEdgeTable()
        
        
        # Update sliders
        screen.blit(SliderLegend, (355, 511))
        if SizeSlider.draw(screen):
            if (SizeSlider.value - 0.5) != prevZoom:
                vertexTable.BetterZoom((SizeSlider.value - 0.5) - prevZoom)
                prevZoom = (SizeSlider.value - 0.5)
        
        if FOVSlider.draw(screen):
            projection.focalLen = (projection.minFocalLen * (1 - FOVSlider.value)) + (projection.maxFocalLen * FOVSlider.value)
            
        if TurnSpeedSlider.draw(screen):
            rotationSpeed = 0 + (vertexTable.MaxTurnSpeed * TurnSpeedSlider.value)
        
        # Draw the checker button
        screen.blit(RotateXYZ, (21, 114))
        # Modify the VertexTable if needed
        if ToggleXButton.draw(screen):
            ToggleYButton.state = False
            vertexTable.RotateVertexTableX(rotationSpeed)
        if ToggleYButton.draw(screen):
            ToggleXButton.state = False
            vertexTable.RotateVertexTableY(rotationSpeed)
        
        
        # If screen drag, rotate shape
        if dragPad.updatePad():
            if dragPad.valueX != prevDragX:
                vertexTable.RotateVertexTableY(5 * (dragPad.valueX - prevDragX))
                prevDragX = dragPad.valueX
        else:
            prevDragX = 0
        if dragPad.updatePad():
            if dragPad.valueY != prevDragY:
                vertexTable.RotateVertexTableX(5 * (dragPad.valueY - prevDragY))
                prevDragY = dragPad.valueY
        else:
            prevDragY = 0
        
        # Rotate alog Z axis to keepshape centered on the Y axis
        deltaX = projection.projectedPoints[4][0] - projection.projectedPoints[22][0]
        deltaY = projection.projectedPoints[4][1] - projection.projectedPoints[22][1]
        if deltaY > 0:
            side = 1
        else:
            side = -1
        if deltaX < -1 or 1 < deltaX:
            if deltaX > 0:
                vertexTable.RotateVertexTableZ(side * deltaX/(2*vertexTable.size))
            elif deltaX < 0:
                vertexTable.RotateVertexTableZ(side * deltaX/(2*vertexTable.size))
        
        # Update the projection
        projection = Projectors.Projectors(vertexTable, projection.focalLen , vertexTable.EdgeTable, offset)
        
        # Draw new frame
        projection.DrawShape((255, 255, 255), screen)
        
        # Draw points
        if makeYourOwnShape:
            diyShape.ShowVertices(screen, projection.projectedPoints)
        
        # Update the canvas
        pygame.display.update()
        pygame.time.Clock().tick(30)
    
    pygame.quit

launchWindow()