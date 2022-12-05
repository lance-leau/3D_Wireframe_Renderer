import math
import numpy

class Vertexes():
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
            temp1.append(VertexTable[i][0] -1 + offset[0])
            temp1.append(VertexTable[i][1] -1 + offset[1])
            temp1.append(VertexTable[i][2] -1 + offset[2])
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
            temp1.append(VertexTable[i][2] * -ShapeSize)
            temp1.append(VertexTable[i][1] * ShapeSize)
            temp2.append(temp1)
        return temp2
    
    def __init__(self, VertexTable, shape = 0, size = 50):
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
        self.CurrShape = shape
        self.EdgeTable = self.GetEdgeTable()
        
    def GetEdgeTable(self):
        """
        Summary:
            returns a stored edge table for different shapes
        Args:
            self.shape - int : shape indexes:
                i = 0 : tetradecahedron (14 faces)
                i = 1 : square based pyramide (5 faces)
                i = 0 : cube (6 faces)
        Returns:
            int[int] : the chosen edge table
        """
        if self.CurrShape == 0:
            return [[11,  5], [5,  17], [17,  7], [7, 15], [25, 21], [15,  3],
                    [19, 21], [3,   9], [25, 23], [1,  3], [23, 19], [1,   5],
                    [19, 11], [5,   7], [11, 23], [7,  3], [23, 17], [17, 25],
                    [25, 15], [15, 21], [21,  9], [9, 19], [9,   1], [1,  11]]
        elif self.CurrShape == 1:
            return [[0, 6], [6, 8], [8, 2], [2, 0], [0, 22], [6, 22], [2, 22], [8, 22]]
        elif self.CurrShape == 2:
            return [[0, 6], [6, 8], [8, 26], [26, 20], [20, 18], [18, 0], [18, 24], [24, 6], [24, 26], [2, 0], [2, 8], [2, 20]]
        else:
            return [[]]
        
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

    def RotateVertexTableX(self, turnSpeed = 0.01):
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

    def RotateVertexTableY(self, turnSpeed = 0.01):
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

    def RotateVertexTableZ(self, turnSpeed = 0.01):
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
    
# Standart Vertex Table
vertexTable = [ (0, 0, 0), (0, 1, 0), (0, 2, 0),
                (1, 0, 0), (1, 1, 0), (1, 2, 0),
                (2, 0, 0), (2, 1, 0), (2, 2, 0),
                (0, 0, 1), (0, 1, 1), (0, 2, 1),
                (1, 0, 1), (1, 1, 1), (1, 2, 1),
                (2, 0, 1), (2, 1, 1), (2, 2, 1), 
                (0, 0, 2), (0, 1, 2), (0, 2, 2),
                (1, 0, 2), (1, 1, 2), (1, 2, 2),
                (2, 0, 2), (2, 1, 2), (2, 2, 2)]