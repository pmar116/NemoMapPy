from Graph import Graph
class GraphProcessor:
    def __init__(self):
        pass
    def loadGraph(self, fileName):
        newGraph = Graph()
        edgeList = []
        with open(fileName) as myFile:
            for line in myFile:
                print(line)



'''2D List
 a = []
>>> for i in xrange(3):
...     a.append([])
...     for j in xrange(3):
...             a[i].append(i+j)
'''