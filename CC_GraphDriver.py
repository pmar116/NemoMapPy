from GraphProcessor import GraphProcessor

fileName = "addEdgeTest.txt"

'''Create GraphProcessor'''
myGP = GraphProcessor()
print("GraphCreated")
myGraph = myGP.loadGraph(fileName)

'''Get edge list from graph to test creation of graph class'''
print(" ")
list = myGraph.test()
for item in list:
    print(item)

print(" ")
"Test making vertex list"
list = myGraph.test2()
for item in list:
    print(item)


"Test tryGetEdge"
print(" ")
edge1 = ['1', '2']
edge2 = ['8', '7']
edge3 = ['9', '9']
'''true'''
print(str(myGraph.tryGetEdge(edge1)))
'''true'''
print(str(myGraph.tryGetEdge(edge2)))
'''false'''
print(str(myGraph.tryGetEdge(edge3)))