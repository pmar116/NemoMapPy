"""
    test driver 
    tests for graph creation and methods
"""

from GraphProcessor import GraphProcessor

fileName = "exampleGraph.txt"

'''Create GraphProcessor'''
myGP = GraphProcessor()
myGraph = myGP.loadGraph(fileName)
print("Graph Created!")

'''Get edge list from graph to test creation of graph class'''
print("TEST GET EDGE LIST\n")
list = myGraph.testEdgeList()
for item in list:
    print(item)


'''Get vertex list'''
print("\nTEST MAKING VERTEX LIST\n")
list = myGraph.testVertexList()
#for key, value in list.items():
    #print(key)
    #print(value)


'''test get edge'''
print("\nTEST GET EDGE\n")
edge1 = ['1081', '339']
edge2 = ['10396', '9914']
edge3 = ['9', '9']
'''true'''
print(str(myGraph.tryGetEdge(edge1)))
'''true'''
print(str(myGraph.tryGetEdge(edge2)))
'''false'''
print(str(myGraph.tryGetEdge(edge3)))


'''test getNeighbor'''
print("\nTEST GET NEIGHBOR\n")
list = myGraph.getNeighbors(47887)
print("Get Neighbor of 47887:")
print(list)
list = myGraph.getNeighbors(35933)
print("\nGet Neighbor of 35933:")
print(list)
list = myGraph.getNeighbors(47836)
print("\nGet Neighbor of 47836:")
print(list)
list = myGraph.getNeighbors(10)
print("\nGet Neighbor of 10:")
print(list)

'''test getOutDegreee'''
print("\nTEST GET OUT DEGREE\n")
num = myGraph.getOutDegree(47887)
print(num)
num = myGraph.getOutDegree(47836)
print(num)
num = myGraph.getOutDegree(10)
print(num)

print("\nTEST GET DEGREE SEQUENCE\n")
list = myGraph.getDegreeSequence()
print(list)
