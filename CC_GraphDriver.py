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
list = myGraph.test2()
for item in list:
    print(item)