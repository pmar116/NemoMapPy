from GraphProcessor import GraphProcessor

fileName = "exampleGraph.txt"

'''Create GraphProcessor'''
myGP = GraphProcessor()
print("GraphCreated")
myGraph = myGP.loadGraph(fileName)

'''Get edge list from graph to test creation of graph class'''
edge = myGraph.testEdgeList()
vertex = myGraph.testVertexList()
print("\nEdge List")
for item in edge:
    print(item)

print("\nVertex List")
for key in vertex:
    print(key)
    print(vertex[key])

print("\n")
myGraph.testGetters()

print("\nGet Nodes Sorted By Degree")
nodesSorted = myGraph.testGetNodesSortedByDegree(4)
for item in nodesSorted:
    print(item)