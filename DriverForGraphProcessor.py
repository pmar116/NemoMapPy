import time
from GraphProcessor import GraphProcessor
from Utility import Utility

'''Get File names and see if they can be opened'''
inputName = input("Input Graph: ")
queryName = input("Query Graph: ")

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

    
    """
    '''TESTING'''
    edge = inputGraph.testEdgeList()
    vertex = inputGraph.testVertexList()
    print("\nEdge List")
    for item in edge:
        print(item)
    print("\nVertex List")
    for key in vertex:
        print(key)
        print(vertex[key])
    print("\n")
    inputGraph.testGetters()
    print("\nGet Nodes Sorted By Degree")
    nodesSorted = inputGraph.testGetNodesSortedByDegree(4)
    for item in nodesSorted:
        print(item)
    """


    """
    main output
    print stats
    """
    print("\n\n")
    print("Input Graph: Nodes - %d; Edges - %d" % (inputGraph.getNumberofVertices(), inputGraph.getNumberofEdges()))
    print("Query Graph: Nodes - %d; Edges - %d" % (queryGraph.getNumberofVertices(), queryGraph.getNumberofEdges()))

    print("\nQuery Graph (sub-graph) Edges: ")
    for item in queryGraph.getEdgeList():
        print(item)

    h = queryGraph.getNodesSortedByDegree(0)
    print("\nH node = [ %d ]" % h[-1])

    timeStart = time.time()
    totalMappings = Utility.algorithm2_modified(queryGraph, inputGraph, h[-1])
    timeEnd = time.time()
    print("Time taken: %s seconds" % (timeEnd-timeStart))

    print("\nMapping: %d" % totalMappings)
else:
    exit()
