from Graph import Graph
class GraphProcessor:
    """
        A Class to read a graph from a file.
        File should be formatted:
            'first#ofEdge1 second#ofEdge1
            first#ofEdge2 second#ofEdge2 . . .'

        Methods
        -------
        loadGraph
            reads edges from a text file and stores the values in a 2D list
        """
    def __init__(self):
        pass
    def loadGraph(self, fileName: str) -> Graph:
        """
        loadGraph: reads edges from a text file and stores the values in a 2D list
        :param fileName: The name f the file containing the graph edges
        :return: A graph containing the edges from the file
        """
        edgeList = []
        with open(fileName) as myFile:
            for line in myFile:
                '''edgeList is a 2D list with each index of edgeList
                    containing exactly one edge. edgeList[index][0] is the
                    first number in a pair, edgeList[index][1] is the seccond'''
                edgeList.append(line.split())

        newGraph = Graph(edgeList)
        return newGraph