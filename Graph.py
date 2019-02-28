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
                if item[0] not in self.vertexList:
                    self.vertexList.append(item[0])
                if item[1] not in self.vertexList:
                    self.vertexList.append(item[1])

        pass
    def addVerticesAndEdgeRange(self, edgeList):
        """TO_DO: Implement"""
        pass
    def test(self):
        return self.edgeList
    def test2(self):
        return self.vertexList