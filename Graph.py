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
    TO_DO: Add other functions
    """
    def __init__(self, edgeList):
        """
        Constructor: create a graph by updating self.edgeList and self.vertexList
            :param edgeList: Contains list of edges to be used to create a graph
        """
        self.edgeList = []
        self.vertexList = []

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
                temp = []
                temp.append(item[0])
                self.vertexList.append(temp)
                temp2 = []
                temp2.append(item[1])
                self.vertexList.append(temp2)
            for i in range(0, len(self.vertexList)):
                if item[0] == self.vertexList[i][0]:
                    found0 = True
                    if item[1] not in self.vertexList[i]:
                         self.vertexList[i].append(item[1])
                if item[1] == self.vertexList[i][0]:
                    found1 = True
                    if item[0] not in self.vertexList[i]:
                        self.vertexList[i].append(item[0])
            if found0 == False:
                temp = []
                temp.append(item[0])
                temp.append(item[1])
                self.vertexList.append(temp)
            if found1 == False:
                temp = []
                temp.append(item[1])
                temp.append(item[0])
                self.vertexList.append(temp)



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

    def test(self):
        return self.edgeList
    def test2(self):
        return self.vertexList