import sys
def loadShape(edgeTable):
    file = open("./../EdgeTables/EdgeTables.txt", "a+")
    file.write("\n")
    size = len(sys.argv)
    for i in range(1, len(sys.argv)):
        if i != size-1:
            file.write(str(edgeTable[i]) + " ")    
        else:
            file.write(str(edgeTable[i]))
    file.close()

loadShape(sys.argv)