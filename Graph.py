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

    TO_DO: Add other functions
    """
    def __init__(self, edgeList):
        """
        Constructor: create a graph by updating self.edgeList and self.vertexList
            :param edgeList: Contains list of edges to be used to create a graph
            :Result: edgeList and vertexList are created and filled to represent
                    the graph
        """
        self.edgeList = []
        self.vertexList = {}

        for item in edgeList:
            '''used fro adding verticies to vertex list'''
            found0 = False
            found1 = False
            '''check if item is in the list'''
            if item not in self.edgeList:
                '''check if the edge from the other direction is in the list'''
                list2 = []
                list2.append(item[1])
                list2.append(item[0])
                if list2 not in self.edgeList:
                    self.edgeList.append(item)

            '''add vertex to vertex list'''
            if len(self.vertexList) == 0:
                self.vertexList[int(item[0])] = []
                self.vertexList[int(item[1])] = []
            if int(item[0]) in self.vertexList:
                if item[1] not in self.vertexList[int(item[0])]:
                    self.vertexList[int(item[0])].append(item[1])
            else:
                self.vertexList[int(item[0])] = []
                self.vertexList[int(item[0])].append(item[1])
            if int(item[1]) in self.vertexList:
                if item[0] not in self.vertexList[int(item[1])]:
                    self.vertexList[int(item[1])].append(item[0])
            else:
                self.vertexList[int(item[1])] = []
                self.vertexList[int(item[1])].append(item[0])



    def addEdge(self, edge):
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
                if edge[0] not in self.vertexList:
                    self.vertexList.append(edge[0])
                if edge[1] not in self.vertexList:
                    self.vertexList.append(edge[1])
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
    
    def don_getsize(self,input):
        """
        __TODO__ idk if this works or not, but it is to help sort degreeOfNode
        don_getsize: method to help sort degreeOfNode in method GetNodesSortedByDegree
            sorts by 
        """
        return input[0]

    def GetNodesSortedByDegree(self, degreeCutOff):
        """
        GetNodesSortedByDegree: get a list of vertices sorted by their degree sequence 
        :param degreeCutOff: the threshold of out degree that we want to check
        :return: list of nodes IDs sorted by out degree in ascending order
        """
        vertexCount = self.getNumberofVertices()
        degreeOfNode = []   # <vertexDegree,vertexID>
        result = []         # <vertexID>

        #vertex.getFirst - get id of verteces list
        #vertex.getSecond - get List of verteces 
        for vertex in self.vertexList:
            # if(vertex.getSecond.size() >= degreeCutOff):
            #   vertexList = [vertex.getSecond.size(), vertex.getFirst()] 
            #   degreeOfNode.append(vertexList)
            print("this is to remove error")
        
        #sort by degree, ascending order
        degreeOfNode.sort(key=self.don_getsize(degreeOfNode))
        #get sorted vertexID sorted by degree
        for vertex in degreeOfNode:
            #result.append(vertex.getSecond)
            print("this is to remove error")
        return result

    def tryGetEdge(self, edge):
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

    def getNeighbors(self, source):
        """
        getNeighbors: return the neighbors of the source
        :param source: the vertex we are finding the neighbors of
        :return: list containing the neighbors of source
        """
        return self.vertexList.get(int(source), -1)



    def test(self):
        return self.edgeList
    def test2(self):
        return self.vertexList