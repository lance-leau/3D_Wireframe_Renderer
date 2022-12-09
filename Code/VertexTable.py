import math
import numpy

class Vertices():
    def lowerShape(self, VertexTable, offset = (0, 0, 0)):
        """
        Summery:
            Makes the shape centered around the point at (0, 0, 0)
            Otherwise it turns arount the bottom left corner
        Args:
            VertexTable - (int, int, int) : the table it modifies
            offset      - (int, int, int) : the offset is added to every point in the table
        """
        temp2 = []
        for i in range(len(VertexTable)):
            temp1 = []
            temp1.append(VertexTable[i][0] + offset[0])
            temp1.append(VertexTable[i][1] + offset[1])
            temp1.append(VertexTable[i][2] + offset[2])
            temp2.append(temp1)
        return temp2
    
    def setSize(self, VertexTable, ShapeSize):
        """
        Summary:
            Does two things:
                - flip the y and z coords as my code has a mistake somewhere
                - set the size of the shape
        Args:
            VertexTable - ([int][int]) : the vertex table
            ShapeSize   - int : the length between two adjacent points in the table
        """
        # flip around and set size
        temp2 = []
        for i in range(len(VertexTable)):
            temp1 = []
            temp1.append(VertexTable[i][0] * ShapeSize)
            temp1.append(VertexTable[i][1] * ShapeSize)
            temp1.append(VertexTable[i][2] * ShapeSize)
            temp2.append(temp1)
        return temp2
    
    def __init__(self, VertexTable, currShape = 0, size = 50):
        """
        Summary:
            A vertex table is a matrix of 3D points represented as a list of list
        Args:
            VertexTable - [int, int, int] : the table itself
            shape       - int : the stored edge table for different shapes
            sixe        - int " the size of the shape
        Attributes:
            EdgeTable - a list of [int, int] representing the edges of the shape from point 1 to point 2 in the VertexTable
        """
        VertexTable = self.lowerShape(VertexTable)
        VertexTable = self.setSize(VertexTable, size)
        self.VertexTable = VertexTable
        self.CurrShape = currShape
        self.EdgeTable = self.GetEdgeTable()
        self.MaxTurnSpeed = 0.05
        self.size = size
        self.ShapeNumber = self.GetFileLen()
    
    def GetFileLen(self):
        file = open("./../EdgeTables/EdgeTables.txt", "r")
        x = len(file.readlines())
        file.close()
        return x
    
    def GetEdgeTable(self):
        """
        Summary: No longer works like that
            returns a stored edge table for different shapes
        Args:
            self.shape - int : shape indexes:
                i = 0 : tetradecahedron (14 faces)
                i = 1 : square based pyramide (5 faces)
                i = 0 : cube (6 faces)
        Returns:
            int[int] : the chosen edge table
        """
        file = open("./../EdgeTables/EdgeTables.txt", "r")
        ret = []
        for i in range(self.CurrShape + 1):
            string = file.readline()
        i = 0
        num = ""
        temp = True
        size = len(string)
        while i < size:
            while i < size and string[i] != " " and string[i] != "":
                num = num + string[i]
                i += 1
            if temp:
                num1 = int(num)
                temp = False
                num = ""
            else:
                num2 = int(num)
                ret.append([num1, num2])
                num = ""
                temp = True
            i += 1
            
        file.close()
        return ret

        
    def Zoom(self, zoom = 0.005):
        """
        Summary
            makes shape bigger over time
        Args:
            zoom - float : Defaults to 0.005
        """
        for i in range(len(self.VertexTable)):
            temp = []
            for j in range(3):
                temp.append(self.VertexTable[i][j] * (1 + zoom))
            self.VertexTable[i] = temp
    
    def BetterZoom(self, zoomFacor):
        """
        Summary
            multiply each vertex by the zoom transform matrix
        Args:
            zoom - float : Defaults to 0.005
        """
        zoomFacor += 1
        ZoomMatrixX = [[zoomFacor,         0,          0],
                       [        0, zoomFacor,          0],
                       [        0,         0,  zoomFacor]]
        zoomMat = numpy.array(ZoomMatrixX)
        for i in range(len(self.VertexTable)):
            point = numpy.array(self.VertexTable[i])
            rPoint = numpy.dot(zoomMat, point)
            self.VertexTable[i] = rPoint

    def RotateVertexTableX(self, turnSpeed = 0.015):
        """
        Summary:
            rotates the shape along the X axis
        Args:
            turnSpeed - float : default turn speed is 0.01
        """
        
        RotateMatrixX = [[               1,                   0,                   0 ],
                         [               0, math.cos(turnSpeed), -math.sin(turnSpeed)],
                         [               0, math.sin(turnSpeed),  math.cos(turnSpeed)]]
        
        rotMat = numpy.array(RotateMatrixX)
        for i in range(len(self.VertexTable)):
            point = numpy.array(self.VertexTable[i])
            rPoint = numpy.dot(rotMat, point)
            self.VertexTable[i] = rPoint

    def RotateVertexTableY(self, turnSpeed = 0.015):
        """
        Summary:
            rotates the shape along the Y axis
        Args:
            turnSpeed - float : default turn speed is 0.01
        """
        
        RotateMatrixY = [[ math.cos(turnSpeed),               0, math.sin(turnSpeed)],
                         [                   0,               1,                   0],
                         [-math.sin(turnSpeed),               0, math.cos(turnSpeed)]]
        
        rotMat = numpy.array(RotateMatrixY)
        for i in range(len(self.VertexTable)):
            point = numpy.array(self.VertexTable[i])
            rPoint = numpy.dot(rotMat, point)
            self.VertexTable[i] = rPoint

    def RotateVertexTableZ(self, turnSpeed = 0.015):
        """
        Summary:
            rotates the shape along the Z axis
        Args:
            turnSpeed - float : default turn speed is 0.01
        """
        
        RotateMatrixZ = [[ math.cos(turnSpeed), -math.sin(turnSpeed),               0],
                         [ math.sin(turnSpeed),  math.cos(turnSpeed),               0],
                         [                   0,                    0,               1]]
        
        rotMat = numpy.array(RotateMatrixZ)
        for i in range(len(self.VertexTable)):
            point = numpy.array(self.VertexTable[i])
            rPoint = numpy.dot(rotMat, point)
            self.VertexTable[i] = rPoint
     
    def MoveShape(self, Offset):
        """
        Summary:
            moves the shape along the given vector
        Args:
            Offset - (float, float, float) : the vector along wich the shape moves
        """
        
        temp2 = []
        for i in range(len(self.VertexTable)):
            temp1 = []
            temp1.append(self.VertexTable[i][0] -1 + Offset[0])
            temp1.append(self.VertexTable[i][1] -1 + Offset[1])
            temp1.append(self.VertexTable[i][2] -1 + Offset[2])
            temp2.append(temp1)
        self.VertexTable = temp2
    
# Standard Vertex Table of dim:
x = 5
y = 5
z = 5
vertexTable = []
for x in range(-1, 2):
    for y in range(-1, 2):
        for z in range(-1, 2):
            vertexTable.append((x, y, z))


# vertexTable = [ (0, 0, 0), (0, 1, 0), (0, 2, 0),
#                 (1, 0, 0), (1, 1, 0), (1, 2, 0),
#                 (2, 0, 0), (2, 1, 0), (2, 2, 0),
#                 (0, 0, 1), (0, 1, 1), (0, 2, 1),
#                 (1, 0, 1), (1, 1, 1), (1, 2, 1),
#                 (2, 0, 1), (2, 1, 1), (2, 2, 1),
#                 (0, 0, 2), (0, 1, 2), (0, 2, 2),
#                 (1, 0, 2), (1, 1, 2), (1, 2, 2),
#                 (2, 0, 2), (2, 1, 2), (2, 2, 2)]