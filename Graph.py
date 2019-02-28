class Graph:
    """
    A Class to represent a network

    Attributes
    ----------
    edgeList: contains all unique edges in the graph
    vertexList: contains all unique vertex in the graph

    Methods
    -------
    addVerticesAndEdgeRange
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
            '''check if item is in the list'''
            if item not in self.edgeList:
                '''check if the edge from the other direction is in the list'''
                list2 = []
                list2.append(item[1])
                list2.append(item[0])
                if list2 not in self.edgeList:
                    self.edgeList.append(item)
                    '''add vertex to vertex list'''
                    if item[0] not in self.vertexList:
                        self.vertexList.append(item[0])
                    if item[1] not in self.vertexList:
                        self.vertexList.append(item[1])

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




    def test(self):
        return self.edgeList
    def test2(self):
        return self.vertexList