from typing import Dict, List
class Graph:
    """
    A Class to represent a network

    Attributes
    ----------
    edgeList: contains all unique edges in the graph
    vertexList: contains all unique vertex in the graph

    Methods
    -------
    addEdge: add a edge and its corresponding vertices to the graph

    getNumberofVertices: returns the number of vertices in the graph

    getNumberofEdges: return the number of edges in the graph

    tryEdge: test if sn edge is is the graph

    getNeighbors: get list of neighbors for requested vertex

    getNodesSortedByDegree: left list of verteces that have at least x amount of connected nodes

    getEdgeList: return the 2d edge list

    getVertexList: return the dictionary vertex list

    getDegreeSequence: degree sequence of all vertices in descending order

    getOutDegree: get out degree of a vertex

    """
    def __init__(self):
        pass

    def __init__(self, passedList: List[List[int]]):
        """
        Constructor: create a graph by updating self.edgeList and self.vertexList
            :param edgeList: Contains list of edges to be used to create a graph
            :Result: edgeList and vertexList are created and filled to represent
                    the graph
        """
        self.edgeList = []
        self.vertexList = {}

        for item in passedList:
            source = item[0]
            target = item[1]
            if source not in self.vertexList:
                self.vertexList[source] = []
            if target in self.vertexList[source]:
                continue
            else:
                self.vertexList[source].append(target)
                self.vertexList[source].sort()

            if target not in self.vertexList:
                self.vertexList[target] = []
            self.vertexList[target].append(source)
            self.vertexList[target].sort()

            self.edgeList.append(item)

        """
        for item in passedList:
            source = item[0]
            target = item[1]

            '''start vertexList'''
            if len(self.vertexList) == 0:
                self.vertexList[source] = []
                self.vertexList[target] = []
            '''insert source-target pair'''
            if source in self.vertexList:
                if target not in self.vertexList[source]:
                    self.vertexList[source].append(target)
                    self.vertexList[source].sort()
                else:
                    '''skip repeated item'''
                    print("SKIPPED")
                    continue
            else:
                self.vertexList[source] = []
                self.vertexList[source].append(target)
            '''insert target-source pair'''
            if target in self.vertexList:
                self.vertexList[target].append(source)
                self.vertexList[target].sort()
            else:
                self.vertexList[target] = []
                self.vertexList[target].append(source)

            self.edgeList.append(item)
            """

    def addEdge(self, edge: List[int]) -> bool:
        """
        addEdge: add a edge and its corresponding vertices to the graph
        :param edge: the edge to be added
        :return: true if edge is added. false if edge is not added
        """
        if edge not in self.edgeList:
            '''check if the edge from the other direction is in the list'''
            list2 = []
            list2.append(edge[1])
            list2.append(edge[0])
            if list2 not in self.edgeList:
                self.edgeList.append(edge)
                '''add vertex to vertex list'''
                if int(edge[0]) in self.vertexList:
                    if edge[1] not in self.vertexList[int(edge[0])]:
                        self.vertexList[int(edge[0])].append(edge[1])
                else:
                    self.vertexList[int(edge[0])] = []
                    self.vertexList[int(edge[0])].append(edge[1])
                if int(edge[1]) in self.vertexList:
                    if edge[0] not in self.vertexList[int(edge[1])]:
                        self.vertexList[int(edge[1])].append(edge[0])
                else:
                    self.vertexList[int(edge[1])] = []
                    self.vertexList[int(edge[1])].append(edge[0])
                return True
        return False

    def getNumberofVertices(self):
        """
        "return: the number of vertexs in graph
        """
        return len(self.vertexList)

    def getNumberofEdges(self):
        """
        :return: the number of edges in graph
        """
        return len(self.edgeList)

    def getNodesSortedByDegree(self, degreeCutOff: int) -> List[int]:
        """
        GetNodesSortedByDegree: get a list of vertices sorted by their degree sequence 
        :param degreeCutOff: the threshold of out degree that we want to check
        :return: list of nodes IDs sorted by out degree in ascending order
        """
        degreeOfNode = []   # <vertexDegree,vertexID>
        result = []         # <vertexID>
        '''get all verteces that have at least degreeCutOff # nodes'''
        for vertex in self.vertexList:
            if len(self.vertexList[vertex]) >= degreeCutOff:
                list2 = [len(self.vertexList[vertex]), vertex]
                degreeOfNode.append(list2)
        
        '''sort DegreeOfNode in ascending order'''
        degreeOfNode.sort(key=lambda x: x[0])
        '''get the vertexID sorted by degree'''
        for vertex in degreeOfNode:
            result.append(vertex[1])
        return result

    def tryGetEdge(self, edge: List[int]) -> bool:
        """
        tryGetEdge: check if an edge exist in the graph
        :param edge: the edge we are trying to find
        :return:true if edge exist, false otherwise
        """

        edgeReverse = []
        edgeReverse.append(edge[1])
        edgeReverse.append(edge[0])
        if edge in self.edgeList:
            return True
        if edgeReverse in self.edgeList:
            return True
        return False

    def getNeighbors(self, source: int) -> List[int]:
        """
        getNeighbors: return the neighbors of the source
        :param source: the vertex we are finding the neighbors of
        :return: list containing the neighbors of source
        """
        neighborList = self.vertexList.get(source, -1).copy()
        neighborList.sort()
        return neighborList

    def getDegreeSequence(self) -> List[int]:
        """
        get degree sequence of all vertices in descending order
        :return: degree sequence of all vertices in descending order
        """
        result = []
        for key in self.vertexList:
            result.append(len(self.vertexList[key]))
        return sorted(result, key = int, reverse=True)

    def getEdgeList(self) -> List[List[int]]:
        """
        :return: the 2d list of edges
        """
        return self.edgeList

    def getVertexList(self) -> Dict[int, List[int]]:
        """
        :return: the dictionary containing the vertex list
        """
        return self.vertexList

    def getOutDegree(self, source: int) -> int:
        """
        get out degree of a vertex
        :param source: vertex whose degree you want to find
        :return: int degree of the vertex if exists, -1 if doesn't exist
        """
        if source in self.vertexList:
            return len(self.vertexList[int(source)])
        else:
            return -1    

    """
    *   Testing methods
    *   mostly returns dicts and prints out data
    """
    def testEdgeList(self):
        return self.edgeList
    def testVertexList(self):
        return self.vertexList
    def testGetters(self):
        print("Number of Vertices: %d" % self.getNumberofVertices())
        print("Number of Edges: %d" % self.getNumberofEdges())
    def testGetNodesSortedByDegree(self, num):
        return self.getNodesSortedByDegree(num)
    def cm_moreGetters(self):
        list = self.getEdgeList()
        for item in list:
            print(item)
        dict = self.getVertexList()
        for key in dict:
            print(key)
