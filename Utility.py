class Utility:
    """
    A Class to help do Motif-based search computations

    Methods
    -------
    algorithm2_modified: runs the motif-based search

    isomorphicExtension

    equalDtoH

    getMostConstrainedNeightbor

    chooseNeighboursOfRange
    """

    def getMostConstrainedNeighbour(self, domain, queryGraph):
        """
        Method to find the most constrained neighboring node of mapped nodes in the query graph.

        :param domain: the current partial mapping of query graph to target graph
        :param queryGraph: the query graph
        :return: int corresponding to most constrained node
        """

    def chooseNeightboursOfRange(self, usedRange, inputGraph, neightborList):
        """
        Method to get all neighbors of a set of nodes in a graph (no duplicate neighbors allowed)
            :param   usedRange: the IDs of the target set of nodes
            :param   inputGraph: the graph to be searched for motif
            :param   neightborList: the reference to the return list of neighbors
            :return:  modified neighborList

            TODO: confirm if this works or not
        """
        for range in usedRange:
            local = inputGraph.getNeighbors(range)
            for loc in local:
                if(loc in usedRange):
                    neightborList.append(loc)
        neightborList.sort()
        neightborList = list(set(neightborList))
        return neightborList

    def isomorphicExtension(self, partialMap, queryGraph, inputGraph, symBreakCondition):
        """
        Method to count all of the isomorphic extensions (no duplicates) of a partial map between the query graph and the target graph
        :param partialMap: the current partial mapping from query graph to target graph
        :param queryGraph: reference to the query graph
        :param inputGraph: reference to the target graph
        :param symBreakCondition: set of symmetry-breaking conditions
        :return: int representing the count of all the isomorphic extensions
        """

    def equalDtoH(self, map):
        """
        Helper function to check if the list of keys of obj1 (D) is equal to obj2 (H)
        Equal if all elements of object 1's keys are present in object 2,
        and the elements don't have to be in the same order between objects
        :param map: map containing obj1 and obj2
        :return: boolean isEqual
        """

    def algorithm2_modified(self, queryGraph, inputGraph, h):
        """
        Method to use NemoMap algorithm (i.e. Algorithm 5 from the NemoMap paper)
            ***Modified from Grochow-Kelis algorithm***
            Implemented in C++ by Tien Huynh
        For more information please see the research paper of NemoMap and/or Grochow-Kellis' paper
        "Network Motif Discovery Using Subgraph Enumeration and Symmetry-Breaking"

        :param queryGraph: reference to query graph
        :param inputGraph: reference to input graph
        :param h: the starting node h of query graph -
            (should be the most constrained node of H -> first rank by out-degree; second rank by neighbor degree sequence)
        :return: The count of all of possible mappings of the query graph to the target graph
        """