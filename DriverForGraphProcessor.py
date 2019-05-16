import time
from GraphProcessor import GraphProcessor
from Utility import Utility

'''Get File names and see if they can be opened'''
#inputName = input("Input Graph: ")
#queryName = input("Query Graph: ")
'''Testing input'''
inputName = "inputGraph.txt"
queryName = "queryGraph.txt"

goodInput = True
try:
    open(inputName, "r")
except IOError:
    print("Input File Error - check spelling and that file exists")
    goodInput = False
try:
    open(queryName, "r")
except IOError:
    print("Query File Error -  check spelling and that file exists")
    goodInput = False

if goodInput:
    '''Create Graphs'''
    myGP = GraphProcessor()
    inputGraph = myGP.loadGraph(inputName)
    queryGraph = myGP.loadGraph(queryName)
    myUtility = Utility()

    """
    main output
    print stats
    """
    print("\n")
    print("Input Graph: Nodes - %d; Edges - %d" % (inputGraph.getNumberofVertices(), inputGraph.getNumberofEdges()))
    print("Query Graph: Nodes - %d; Edges - %d" % (queryGraph.getNumberofVertices(), queryGraph.getNumberofEdges()))

    print("\nQuery Graph (sub-graph) Edges: ")
    for item in queryGraph.getEdgeList():
        print(item)

    h = queryGraph.getNodesSortedByDegree(0)
    h1 = h[-1]
    print("\nH node = [ %d ]" % h1)

    '''run the nemomap alg'''
    timeStart = time.time()
    totalMappings = myUtility.algorithm2_modified(queryGraph, inputGraph, h1)
    timeEnd = time.time()

    print("\nMapping: %d" % totalMappings)
    print("Time taken: %s seconds" % (timeEnd-timeStart))

else:
    exit()
