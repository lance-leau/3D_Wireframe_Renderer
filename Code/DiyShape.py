import pygame
        

class DiyShape():
    def __init__(self, vertexTable):
        self.vertexTable = vertexTable
        self.edgeTable = [[0, 0]]
        self.SelectedA = 0
        self.SelectedB = 0
        self.currPoint = 0
    
    def AddEdge(self):
        self.edgeTable.append([self.SelectedA, self.SelectedB])
    
    def ShowVertices(self, screen, projectedPoints):
        for i in range (len(projectedPoints)):
            if i == self.SelectedA:
                pygame.draw.circle(screen, (255, 0, 0), projectedPoints[i], 3, 6)
            elif i == self.SelectedB:
                pygame.draw.circle(screen, (0, 0, 255), projectedPoints[i], 3, 6)
            else:
                pygame.draw.circle(screen, (255, 255, 255), projectedPoints[i], 3, 6)
                
    def SaveShape(self, file):
        file = open(file, "a+")
        file.write("\n")
        for i in range(1, len(self.edgeTable)):
            file.write(str(self.edgeTable[i][0]) + " " + str(self.edgeTable[i][1]))
            print(str(self.edgeTable[i][0]) + " " + str(self.edgeTable[i][1]), end=" ")
            if i != len(self.edgeTable) -1:
                file.write(" ")
        print()
        file.close()
                
    def DeleteShape(self, file, index):
        if index < 3:
            print("Base shapes can not be deleted")
            return False
        fileReader = open(file, "r")
        lines = fileReader.readlines()
        fileReader.close()
        fileWriter = open(file, "w")
        for i in range(len(lines)):
            if i == 0:
                fileWriter.write(lines[i].strip("\n"))
            elif index != i:
                fileWriter.write("\n" + lines[i].strip("\n"))
        fileWriter.close()
        return True