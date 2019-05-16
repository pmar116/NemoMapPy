"""
    test driver 
    tests for graph creation and methods
"""

from GraphProcessor import GraphProcessor

fileName = "queryGraph.txt"

'''Create GraphProcessor'''
myGP = GraphProcessor()
myGraph = myGP.loadGraph(fileName)

'''Get edge list from graph to test creation of graph class'''
"""
print("TEST GET EDGE LIST\n")
list = myGraph.testEdgeList()
for item in list:
    print(item)
"""

'''Get vertex list'''
print("\nTEST MAKING VERTEX LIST")
list = myGraph.testVertexList()
for key, value in list.items():
    print(key)
    print(value)
print("VERTEXES")
for item in list:
    print(item)


'''test get edge'''
print("\nTEST GET EDGE")
edge1 = [1, 3]
edge2 = [2, 1]
edge3 = [4, 2]
'''true'''
print(str(myGraph.tryGetEdge(edge1)))
'''true'''
print(str(myGraph.tryGetEdge(edge2)))
'''false'''
print(str(myGraph.tryGetEdge(edge3)))


'''test getNeighbor'''
print("\nTEST GET NEIGHBOR")
list = myGraph.getNeighbors(1)
print("Get Neighbor of 1:")
print(list)
list = myGraph.getNeighbors(2)
print("Get Neighbor of 2:")
print(list)
list = myGraph.getNeighbors(3)
print("Get Neighbor of 3:")
print(list)
list = myGraph.getNeighbors(4)
print("Get Neighbor of 4:")
print(list)

'''test getOutDegreee'''
print("\nTEST GET OUT DEGREE")
num = myGraph.getOutDegree(1)
print("edges connected to node 1: %d" % num)
num = myGraph.getOutDegree(2)
print("edges connected to node 2: %d" % num)
num = myGraph.getOutDegree(3)
print("edges connected to node 3: %d" % num)

print("\nTEST GET DEGREE SEQUENCE")
degseq = myGraph.getDegreeSequence()
print(degseq)
