from Graph import Graph
from bisect import bisect_left


# noinspection PyPep8Naming
class Utility:
    """
    A Class to help do Motif-based search computations

    Methods
    -------
    algorithm2_modified: runs the motif-based search

    algorithm2_modified_for_equivalence_class:

    findCondition:

    isomorphicExtension

    equalDtoH

    getMostConstrainedNeightbor

    chooseNeighboursOfRange

    isNeighborIncompatible
    """

    def __init__(self):
        pass

    def binarySearch(self, a, x, lo=0, hi=None):
        hi = hi if hi is not None else len(a)  # hi defaults to len(a)
        pos = bisect_left(a, x, lo, hi)  # find insertion position
        return pos if pos != hi and a[pos] == x else -1

    def getMostConstrainedNeighbour(self, domain, queryGraph):
        """
        Method to find the most constrained neighboring node of mapped nodes in the query graph.

        :param domain:List[int] - the current partial mapping of query graph to target graph
        :param queryGraph:Graph - the query graph
        :return: int - number corresponding to most constrained node
        """
        "get all neoghbors of already mapped nodes"
        "NO Duplicates"
        neighborList = []
        self.chooseNeightboursOfRange(domain, queryGraph, neighborList)

        neighborListSize = len(neighborList)

        if neighborListSize == 1:
            return neighborList[0]
        elif neighborListSize == 0:
            return -1

        "2D list to create pairs"
        constraintRank = []
        for i in range(0, neighborListSize):
            constraintRank.append([0, 0])

        for i in range(0, neighborListSize):
            constraintRank[i][1] = neighborList[i]
            local = queryGraph.getNeighbors(neighborList[i])
            for loc in local:
                if int(loc) in domain:
                    constraintRank[i][0] += 1

        "Rank neighbor nodes with most already-mapped neighbors"
        constraintRankBegin = iter(constraintRank)
        constraintRank = sorted(constraintRankBegin, key=list, reverse=True)

        highestNeighborMapped = constraintRank[0][0]
        count = neighborListSize
        for i in range(1, neighborListSize):
            if constraintRank[i][0] < highestNeighborMapped:
                if i == 1:
                    return constraintRank[0][1]
                count = i
                break

        "Rank neighbor nodes with highest degree"
        for i in range(0, count):
            constraintRank[i][0] = queryGraph.getOutDegree(constraintRank[i][1])

        constraintRank = sorted(constraintRank[:count], key=list, reverse=True)

        highestDegree = constraintRank[0][0]
        for i in range(1, count):
            if constraintRank[i][0] < highestDegree:
                if i == 1:
                    return constraintRank[0][1]
                count = i
                break

        "rank neighbor nodes wth largest neighbor degree sequence"
        for i in range(0, count):
            temp = 0
            for neighborOfPotential in queryGraph.getNeighbors(constraintRank[i][1]):
                temp += queryGraph.getOutDegree(neighborOfPotential)
            constraintRank[i][0] = temp

        largestNeighborDegree = constraintRank[0][0]
        for i in range(1, count):
            if constraintRank[i][0] < largestNeighborDegree:
                if i == 1:
                    return constraintRank[0][1]
                break

        return constraintRank[0][1]

    def chooseNeightboursOfRange(self, usedRange, inputGraph, neightborList):
        """
        Method to get all neighbors of a set of nodes in a graph (no duplicate neighbors allowed)
            :param   usedRange:List[int] - the IDs of the target set of nodes
            :param   inputGraph:Graph - the graph to be searched for motif
            :param   neightborList:List[int[ - the reference to the return list of neighbors
            :return: List[int] - modified neighborList
        """
        for range in usedRange:
            local = inputGraph.getNeighbors(range)
            for loc in local:
                if int(loc) not in usedRange:
                    neightborList.append(int(loc))
        neightborList.sort()
        neightborList[:] = list(set(neightborList))

        return neightborList

    def isNeighbourIncompatible(self, inputGraph, n, partialMap, neighborsOfM):
        """
        Method to check if a neighbor node n of the target graph could be mapped to a node m of the query graph
        :param inputGraph:Graph - target graph
        :param n:int - ID of the node n in the target graph
        :param partialMap:Dict[int, int] - the current partial mapping from query graph to target graph #dit
        :param neighborsOfM:List[int] - the list of neighbors of node m to the query graph
        :return: boolean - True if node n can be mapped to node m, otherwise false
        """
        for d in partialMap:
            neighborsOfd = inputGraph.getNeighbors(partialMap[d])
            if d in neighborsOfM:
                if n not in neighborsOfd:
                    return True
            else:
                if n in neighborsOfd:
                    return True
        return False

    def checkSymmetryBreak(self, fixed, nodesToCheck, partialMap, m, n):
        """
        Method to check if a mapping from node m of query graph to node n of target graph satisfy the symmetry-breaking conditions
        :param fixed:int - the representative node from each equivalence class
        :param nodesToCheck:List[int] - the symmetry-breaking conditions
        :param partialMap:Dict[int, int] - the current partial mapping from query graph to target graph
        :param m:int - ID number of node m of query graph
        :param n:int - ID number of node n of target graph
        :return: boolean - True if the symmetry-breaking condition is satisfied and the mapping is okay, False == mapping not okay
        """
        if m not in nodesToCheck or (m != fixed):   # and partialMap.index(fixed)== partialMap[-1]):
            return True

        if m == fixed:
            fixedLabel = n
        else:
            fixedLabel = partialMap[fixed]

        if m == fixed:
            for node in nodesToCheck:
                if node in partialMap.keys():
                    if partialMap[node] < fixedLabel:
                        return False
            return True
        else:
            return n >= fixedLabel

    def equalDtoH(self, obj1, obj2):
        """
        Helper function to check if the list of keys of obj1 (D) is equal to obj2 (H)
        Equal if all elements of object 1's keys are present in object 2,
        and the elements don't have to be in the same order between objects
        :param obj1:List[int] - vectorList of queryGraph
        :param obj2:List[int] - list of keys
        :return: boolean - isEqual
        """
        temp = []
        if len(obj1) != len(obj2):
            return False
        for key in obj1:
            temp.append(int(key))
            if temp.sort() != obj2.sort():
                return False
        return True

    def findCondition(self, mappedHNodes, theMappings, condition, equivalenceClass):
        """
        Method to find the symmetry-breaking cinditions by Grochow-Kellis.
        *****NOTE*****: should combine this with Algorithm2_Modified_For_Equivalence_Class()
        :param mappedHNodes:List[int] - the mapped nodes from vertex H
        :param theMappings:List[List[int]] -
        :param condition:Dict[int, List[int]] - the symmetry break condition that we are testing in this iteration
        :param equivalenceClass: Dict[int, set[int]) -
        :return: Dict[int, List[int]] - returns the symmetry break condition that was found
        """
        if len(theMappings) == 1:
            return condition

        equivalenceFilter = {}
        for i in range(0, len(mappedHNodes)):
            equivalenceFilter[i] = set()

        for maps in theMappings:
            for i in range(0, len(maps)):
                equivalenceFilter[i].add(maps[i])

        filterkey = next(iter(equivalenceFilter))
        maxSize = len(equivalenceFilter[filterkey])

        if len(equivalenceClass) == 0:
            temp = set(equivalenceFilter[filterkey])
        else:
            classitem = next(iter(equivalenceClass))
            temp = set(equivalenceClass[classitem])

        for entry in equivalenceFilter:
            if len(equivalenceFilter[entry]) > 1:
                if len(equivalenceFilter[entry]) > maxSize:
                    maxSize = len(equivalenceFilter[entry])
                    temp = set(equivalenceFilter[entry])

        equivalenceClass.discard(temp)
        sortedTemp = sorted(temp)
        fixedNode = sortedTemp[0]

        if fixedNode in condition:
            condition[fixedNode].append(sortedTemp)
        else:
            condition[fixedNode] = [sortedTemp]

        newMappings = []

        for maps in theMappings:
            for i in range(0, len(maps)):
                if maps[i] == fixedNode and maps[i] == mappedHNodes[i]:
                    newMappings.append(maps)
        self.findCondition(mappedHNodes, newMappings, condition, equivalenceClass)
        return condition

    def isomorphicExtension(self, partialMap, queryGraph, inputGraph, symBreakCondition):
        """
        Method to count all of the isomorphic extensions (no duplicates) of a partial map between the query graph and the target graph
        :param partialMap:Dict[int, int] - the current partial mapping from query graph to target graph #is a dictionary
        :param queryGraph:Graph - reference to the query graph
        :param inputGraph:Graph - reference to the target graph
        :param symBreakCondition:Dict[int, List[int] - set of symmetry-breaking conditions
        :return: int - representing the count of all the isomorphic extensions
        """
        listOfIsomorphisms = 0  # tracks number of isomorphisms
        partialMapValuesG = []  # list
        partialMapKeysH = []  # list

        '''extract list of keys and list values from paritalMap'''
        for maps in partialMap:
            partialMapValuesG.append(int(partialMap[maps]))
            partialMapKeysH.append(int(maps))

        mapValueOriginal = list(partialMapValuesG)
        mapKeyOriginal = list(partialMapKeysH)
        partialMapValuesG.sort()
        partialMapKeysH.sort()

        if self.equalDtoH(queryGraph.getVertexList(), partialMapKeysH):
            return 1

        m = self.getMostConstrainedNeighbour(partialMapKeysH, queryGraph)
        if m < 0:
            return 0
        neighborsOfM = queryGraph.getNeighbors(m)
        bestMappedNeighborOfM = 0
        for neighbor in neighborsOfM:
            if neighbor in partialMap.keys():
                bestMappedNeighborOfM = neighbor
                break

        possibleMappingNodes = []
        for node in inputGraph.getNeighbors(partialMap[bestMappedNeighborOfM]):
            if node not in partialMapValuesG:
                possibleMappingNodes.append(int(node))

        partialMapKeysHSize = len(partialMapKeysH)
        for i in range(0, partialMapKeysHSize):
            neighborsOfMappedGNode = (inputGraph.getNeighbors(mapValueOriginal[i]))
            temp = []
            if int(mapKeyOriginal[i]) in neighborsOfM:
                for node in possibleMappingNodes:
                    if node in neighborsOfMappedGNode:
                        temp.append(int(node))
                possibleMappingNodes = temp.copy()
            else:
                for node in possibleMappingNodes:
                    if node not in neighborsOfMappedGNode:
                        temp.append(int(node))
                possibleMappingNodes = temp.copy()

        for n in possibleMappingNodes:
            if not self.isNeighbourIncompatible(inputGraph, n, partialMap, neighborsOfM):
                skip = False
                for condition in symBreakCondition:
                    if not self.checkSymmetryBreak(symBreakCondition[condition][0][0], symBreakCondition[condition][0], partialMap, m, n):
                        skip = True
                        break
                if skip:
                    continue
                newPartialMap = partialMap.copy()  # dict of pairs
                newPartialMap[m] = n

                subList = self.isomorphicExtension(newPartialMap, queryGraph, inputGraph, symBreakCondition)
                listOfIsomorphisms += subList

        return listOfIsomorphisms

    def isomorphicExtensionForEquivalenceClass(self, partialMap, queryGraph, inputGraph, mappedHNodes):
        """
        Helper method to find all of the isomorphic extensions of a partial map between the query graph and itself
        :param partialMap:dict[int, int] - a partial map
        :param queryGraph:Graph
        :param inputGraph:Graph - same as query graph
        :param mappedHNodes:List[int] -
        :return: List[List[int]] -
        """

        result = []                 #2d list
        listOfIsomorphisms = []     #2d list
        partialMapValuesG = []      #list
        partialMapKeysH = []        #list

        '''extract list of keys and list of values from partialMap'''
        for maps in partialMap:
            partialMapValuesG.append(int(partialMap[maps]))
            partialMapKeysH.append(maps)

        mapValueOriginal = list(partialMapValuesG)
        mapKeyOriginal = list(partialMapKeysH)

        partialMapValuesG.sort()
        partialMapKeysH.sort()

        if self.equalDtoH(queryGraph.getVertexList(), partialMapKeysH) == True:
            mappedHNodes[:] = list(mapKeyOriginal)
            result.append(mapValueOriginal)
            return result

        m = int(self.getMostConstrainedNeighbour(partialMapKeysH, queryGraph))
        if m < 0:
            return listOfIsomorphisms
        
        neighbourRange = []     # list
        neighbourRange = self.chooseNeightboursOfRange(partialMapValuesG, inputGraph, neighbourRange)

        neighborsOfM = queryGraph.getNeighbors(m)

        for n in neighbourRange:
            if not self.isNeighbourIncompatible(inputGraph, n, partialMap, neighborsOfM):
                newPartialMap = partialMap.copy()
                newPartialMap[m] = int(n)
                subList = self.isomorphicExtensionForEquivalenceClass(newPartialMap, queryGraph, inputGraph, mappedHNodes)
                for item in subList:
                    listOfIsomorphisms.append(item)
        return listOfIsomorphisms

    def algorithm2_modified_for_equivalance_class(self, queryGraph, inputGraph, fixedNode):
        """
        Method to find the symmetry-breaking conditions by Grochow-Kellis. It starts by choosing one node to be the anchor point and create conditions from
        :param queryGraph:Graph - reference to query graph
        :param inputGraph:Graph - reference to input graph
        :param fixedNode:int - the node we choose to be fixed as the anchor for symmetry (might not be needed??)
        :return: Dict[int, List[int]] - a set of symmetry-breaking conditions for each represented node from each equivalance class
        """
        vertexList = queryGraph.getVertexList()
        h = next(iter(vertexList))

        inputGraphDegSeq = inputGraph.getNodesSortedByDegree(queryGraph.getOutDegree(h))
        theMappings = []        #2d list
        mappedHNodes = []       #list

        for item in inputGraphDegSeq:
            f = {}  # dictionary of pairs
            f[h] = int(item)
            mappings = self.isomorphicExtensionForEquivalenceClass(f, queryGraph, queryGraph, mappedHNodes)
            for maps in mappings:
                theMappings.append(maps)

        condition = {}          #dict
        equivalenceClass = set()

        return self.findCondition(mappedHNodes, theMappings, condition, equivalenceClass)

    def algorithm2_modified(self, queryGraph, inputGraph, h):
        """
        Method to use NemoMap algorithm (i.e. Algorithm 5 from the NemoMap paper)
            ***Modified from Grochow-Kelis algorithm***
            Implemented in C++ by Tien Huynh
        For more information please see the research paper of NemoMap and/or Grochow-Kellis' paper
        "Network Motif Discovery Using Subgraph Enumeration and Symmetry-Breaking"

        :param queryGraph:Graph - reference to query graph
        :param inputGraph:Graph - reference to input graph
        :param h:int - the starting node h of query graph -
            (should be the most constrained node of H -> first rank by out-degree; second rank by neighbor degree sequence)
        :return: int - The count of all of possible mappings of the query graph to the target graph
        """

        condition = self.algorithm2_modified_for_equivalance_class(queryGraph, queryGraph, h)

        for con in condition:
            print(str(con) + " => " + str(condition[con][0]), end='')
            print("")

        inputGraphDegSeq = inputGraph.getNodesSortedByDegree(queryGraph.getOutDegree(h))

        mappingCount = 0
        f = {}
        for value in inputGraphDegSeq:
            f[h] = value
            mappingCount += self.isomorphicExtension(f, queryGraph, inputGraph, condition)

        return mappingCount
