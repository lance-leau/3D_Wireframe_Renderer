# This project was made by Lancelot

from cmath import isclose
import VertexTable, Projectors
import sys,  pygame
import Button

#create display window
screen = pygame.display.set_mode((1024, 576))
pygame.display.set_caption("3D Wire Frame Renderer")

screen.fill((33, 40, 48))

#load button images
shape1 = pygame.image.load("Images\shape1.png").convert_alpha()
shape2 = pygame.image.load("Images\shape2.png").convert_alpha()
shape3 = pygame.image.load("Images\shape3.png").convert_alpha()
shape4 = pygame.image.load("Images\CustomShape.png").convert_alpha()
nextShape = pygame.image.load("Images/NextShape.png").convert_alpha()
prevShape = pygame.image.load("Images/PrevShape.png").convert_alpha()
RotateXYZ = pygame.image.load("Images/RoateXYZ.png").convert_alpha()
CheckedBox = pygame.image.load("Images/CheckedBox.png").convert_alpha()
UncheckedBox = pygame.image.load("Images/UncheckedBox.png").convert_alpha()
SliderBar = pygame.image.load("Images/SliderBar.png").convert_alpha()
SliderNob = pygame.image.load("Images/SliderNob.png").convert_alpha()

#create button instances
nextShapeButton = Button.Button(178, 43, nextShape, 1)
prevShapeButton = Button.Button(27, 43, prevShape, 1)
ToggleXButton = Button.Check(56, 191, UncheckedBox, CheckedBox, 1)
ToggleYButton = Button.Check(126, 191, UncheckedBox, CheckedBox, 1)
ToggleZButton = Button.Check(197, 191, UncheckedBox, CheckedBox, 1)
SizeSlider = Button.Slider(34, 423, SliderBar, SliderNob, 1)
FOVSlider = Button.Slider(34, 475, SliderBar, SliderNob, 1)
TurnSpeedSlider = Button.Slider(34, 526, SliderBar, SliderNob, 1)
dragPad = Button.Tactile(256, 0, 768, 576)

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
    
    vertexTable = VertexTable.Vertexes(VertexTable.vertexTable, 0)
    projection = Projectors.Projectors(vertexTable, 250, vertexTable.EdgeTable, offset)
    pygame.draw.rect(screen, (69, 74, 79), pygame.Rect(0, 0, 256, 576))
    
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                sys.exit
                
        # Show current shape on top left corner
        if vertexTable.CurrShape == 0:
            screen.blit(shape1, (88, 29))
        if vertexTable.CurrShape == 1:
            screen.blit(shape2, (88, 29))
        if vertexTable.CurrShape == 2:
            screen.blit(shape3, (88, 29))
    
        
        # Draw buttons on window, check if clicked
        if nextShapeButton.draw(screen):
            vertexTable.CurrShape += 1
            if (vertexTable.CurrShape > 2):
                vertexTable.CurrShape = 0
            vertexTable.EdgeTable = vertexTable.GetEdgeTable()
        
        if prevShapeButton.draw(screen):
            vertexTable.CurrShape -= 1
            if (vertexTable.CurrShape < 0):
                vertexTable.CurrShape = 2
            vertexTable.EdgeTable = vertexTable.GetEdgeTable()
        
        if SizeSlider.draw(screen):
            if (SizeSlider.value - 0.5) != prevZoom:
                vertexTable.BetterZoom((SizeSlider.value - 0.5) - prevZoom)
                prevZoom = (SizeSlider.value - 0.5)
        
        if FOVSlider.draw(screen):
            projection.focalLen = (projection.minFocalLen * (1 - FOVSlider.value)) + (projection.maxFocalLen * FOVSlider.value)
            
        if TurnSpeedSlider.draw(screen):
            rotationSpeed = 0 + (vertexTable.MaxTurnSpeed * TurnSpeedSlider.value)
        
        # Earase previous frame
        projection.DrawShape((33, 40, 48), screen)
        
        # Draw the checker button
        screen.blit(RotateXYZ, (21, 136))
        
        # Modify the VertexTable if needed
        if ToggleXButton.draw(screen):
            vertexTable.RotateVertexTableX(rotationSpeed)
        if ToggleYButton.draw(screen):
            vertexTable.RotateVertexTableY(rotationSpeed)
        if ToggleZButton.draw(screen):
            vertexTable.RotateVertexTableZ(rotationSpeed)
        
        
        # If screen drag, rotate shape
        if dragPad.updatePad():
            if dragPad.valueX != prevDragX:
                vertexTable.RotateVertexTableY(3 * (dragPad.valueX - prevDragX))
                prevDragX = dragPad.valueX
        else:
            prevDragX = 0
        if dragPad.updatePad():
            if dragPad.valueY != prevDragY:
                vertexTable.RotateVertexTableX(3 * (dragPad.valueY - prevDragY))
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
            print(deltaX)
            if deltaX > 0:
                vertexTable.RotateVertexTableZ(side * deltaX/(2*vertexTable.size))
            elif deltaX < 0:
                vertexTable.RotateVertexTableZ(side * deltaX/(2*vertexTable.size))
        
        # Update the projection
        projection = Projectors.Projectors(vertexTable, projection.focalLen , vertexTable.EdgeTable, offset)
        
        # Draw new frame
        projection.DrawShape((255, 255, 255), screen)
        # Draw axis on top of everythong
        # pygame.draw.line(screen, (255, 255, 255), (640, 0), (640, 576), 2)
        # pygame.draw.line(screen, (255, 255, 255), (256, 288), (1024, 288), 2)
        # projection.DrawPoints([projection.projectedPoints[4], projection.projectedPoints[22]], screen, (255, 0, 0))
        
        # Update the canvas
        pygame.display.update()
        pygame.time.Clock().tick(30)
    
    pygame.quit

launchWindow()