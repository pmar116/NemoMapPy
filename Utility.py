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

    isNeighborIncompatible
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
                if loc in usedRange:
                    neightborList.append(loc)
        neightborList.sort()
        neightborList = list(set(neightborList))
        return neightborList

    def isNeighbourIncompatible(self, inputGraph, n, partialMap, neighborsOfM):
        """
        Method to check if a neighbor node n of the target graph could be mapped to a node m of the query graph
        :param inputGraph: target graph
        :param n: ID of the node n in the target graph
        :param partialMap: the current partial mapping from query graph to target graph
        :param neighborsOfM: the list of neighbors of node m to the query graph
        :return: boolean True if node n can be mapped to node m, otherwise false
        """
        return True

    def checkSymmetryBreak(self, fixed, nodesToCheck, partialMap, m, n):
        """
        Method to check if a mapping from node m of query graph to node n of target graph satisfy the symmetry-breaking conditions
        :param fixed: the representative node from each equivalence class
        :param nodesToCheck: the symmetry-breaking conditions
        :param partialMap: the current partial mapping from query graph to target graph
        :param m: ID number of node m of query graph
        :param n: ID number of node n of target graph
        :return: True if the symmetry-breaking condition is satisfied and the mapping is okay, False == mapping not okay
        """
        if m not in nodesToCheck or ((m != fixed) and partialMap.index(fixed)==partialMap[-1]):
            return True

        fixedLabel = 0
        if m == fixed:
            fixedLabel = n
        else:
            fixedLabel = partialMap[fixed]

        if m == fixed:
            for node in nodesToCheck:
                if partialMap.index(node) != partialMap[-1]:
                    if partialMap[node] < fixedLabel:
                        return False
            return True
        else:
            return n >= fixedLabel

    def isomorphicExtension(self, partialMap, queryGraph, inputGraph, symBreakCondition):
        """
        Method to count all of the isomorphic extensions (no duplicates) of a partial map between the query graph and the target graph
        :param partialMap: the current partial mapping from query graph to target graph
        :param queryGraph: reference to the query graph
        :param inputGraph: reference to the target graph
        :param symBreakCondition: set of symmetry-breaking conditions
        :return: int representing the count of all the isomorphic extensions
        """
        listOfIsomorphisms = 0;
        partialMapValvuesG = []
        partialMapKeysH = []
        for item in partialMap:
            partialMapValvuesG = item[1]
            partialMapKeysH = item[0]

        mapValueOriginal = partialMapValvuesG
        mapKeyOriginal = partialMapKeysH

        partialMapValvuesG.sort()
        partialMapKeysH.sort()

        if self.equalDtoH(queryGraph.getVertexList(), partialMapKeysH):
            return 1

        m = self.getMostConstrainedNeighbour(partialMapKeysH, queryGraph)
        if m < 0:
            return 0

        neighborsOfM = queryGraph.getNeighbors(m)
        bestMappedNeighborOfM = -1
        for neighbor in neighborsOfM:
            if partialMap.index(neighbor) != partialMap[-1]:
                bestMappedNeighborOfM = neighbor
                break

        possibleMappingNodes = []
        for node in inputGraph.GetNeighbors(partialMap[bestMappedNeighborOfM]):
            if node in partialMapValvuesG:
                possibleMappingNodes.append(node)

        partialMapKeysHSize = len(partialMapKeysH)
        for i in range(0,partialMapKeysHSize):
            neighborsOfMappedGNode = (inputGraph.getNeighbors(mapValueOriginal[i]))
            temp = []
            if mapKeyOriginal[i] in neighborsOfM:
                for node in possibleMappingNodes:
                    if node in neighborsOfMappedGNode:
                        temp.append(node)
                possibleMappingNodes = temp
            else:
                for node in possibleMappingNodes:
                    if node in neighborsOfMappedGNode:
                        temp.append(node)
                possibleMappingNodes = temp

        for n in possibleMappingNodes:
            if self.isNeighbourIncompatible(inputGraph, n, partialMap, neighborsOfM == False):
                skip = False
                for condition in symBreakCondition:
                    if self.checkSymmetryBreak(condition[0], condition[1], partialMap, m, n) == False:
                        skip = True
                        break
                if(skip):
                    continue
                newPartialMap = partialMap
                newPartialMap[m] = n

                subList = self.isomorphicExtension(newPartialMap, queryGraph, inputGraph, symBreakCondition)
                listOfIsomorphisms += subList
        return listOfIsomorphisms


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