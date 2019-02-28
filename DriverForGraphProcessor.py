from GraphProcessor import GraphProcessor

fileName = "exampleGraph.txt"

'''Create GraphProcessor'''
myGP = GraphProcessor()
print("GraphCreated")
myGraph = myGP.loadGraph(fileName)

'''Get edge list from graph to test creation of graph class'''
list = myGraph.test()
for item in list:
    print(item)