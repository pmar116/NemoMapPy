from Graph import Graph
from bisect import  bisect_left
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

        :param domain: the current partial mapping of query graph to target graph
        :param queryGraph: the query graph
        :return: int corresponding to most constrained node
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
        constraintRank = [0] * neighborListSize
        for i in range(0, len(constraintRank)):
            constraintRank[i] = [0, 0]

        for i in range(0, neighborListSize):
            constraintRank[i][1] = neighborList[i]
            local = [0] * (queryGraph.getNeighbors(neighborList[i]))
            for loc in local:
                if self.binarySearch(domain[0], domain[-1], loc):
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
        for d in partialMap:
            neighborsOfd = inputGraph.getNeighbors(d[1])
            if d[0] in neighborsOfM:
                if n not in neighborsOfd:
                    return True
            else:
                if n in neighborsOfd:
                    return True
        return False

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
            if not self.isNeighbourIncompatible(inputGraph, n, partialMap, neighborsOfM):
                skip = False
                for condition in symBreakCondition:
                    if not self.checkSymmetryBreak(condition[0], condition[1], partialMap, m, n):
                        skip = True
                        break
                if skip:
                    continue
                newPartialMap = partialMap
                newPartialMap[m] = n

                subList = self.isomorphicExtension(newPartialMap, queryGraph, inputGraph, symBreakCondition)
                listOfIsomorphisms += subList
        return listOfIsomorphisms

    def equalDtoH(self, obj1, obj2):
        """
        Helper function to check if the list of keys of obj1 (D) is equal to obj2 (H)
        Equal if all elements of object 1's keys are present in object 2,
        and the elements don't have to be in the same order between objects
        :param obj1: vectorList of queryGraph
        :param obj2: list of keys
        :return: boolean isEqual
        """
        if len(obj1) != len(obj2):
            return False
        for key in obj1:
            if not key in obj2:
                return False
        return True

    def algorithm2_modified_for_equivalance_class(self, queryGraph, fixedNode):
        """
        Method to find the symmetry-breaking conditions by Grochow-Kellis. It starts by choosing one node to be the anchor point and create conditions from
        :param queryGraph: reference to query graph
        :param fixedNode: the node we choose to be fixed as the anchor for symmetry
        :return: a set of symmetry-breaking conditions for each represented node from each equivalance class
        """
        vertexList = queryGraph.getVertexList()
        h = vertexList[next(iter(vertexList))][0]

        inputGraphDegSeq = queryGraph.getNodesSortedByDegree(queryGraph.getOutDegree(h))
        theMappings = []        #2d list
        f = {}                  #dictionary
        mappedHNodes = []       #list

        for item in inputGraphDegSeq:
            f[h] = item
            mappings = self.isomorphicExtension(f, queryGraph, queryGraph, mappedHNodes)
            #theMappings
        condition = {}          #dictionary
        equivalenceClass = {}   %dict

        return self.findCondition(mappedHNodes, theMappings, condition, equivalenceClass)

    def findCondition(self, mappedHNodes, theMappings, condition, equivalenceClass):
        """
        Method to find the symmetry-breaking cinditions by Grochow-Kellis.
        *****NOTE*****: should combine this with Algorithm2_Modified_For_Equivalence_Class()
        :param mappedHNodes:
        :param theMappings:
        :param condition:
        :param equivalenceClass:
        :return:
        """
        if len(theMappings) == 1:
            return condition

        equivalenceFilter = {}

        for map in theMappings:
            for i in range(0, len(map)):
                equivalenceFilter[int(i)] = [map[i]]

        maxSize = len(equivalenceFilter[0])

        if len(equivalenceClass) == 0:
            temp = equivalenceFilter[int(0)]
        else:
            temp = equivalenceClass[int(0)]

        for entry, value in equivalenceFilter:
            if len(value) > 1:
                equivalenceClass[int(entry)].append(value)
                if len(value) > maxSize:
                    maxSize= len(value)
                    temp = value

        equivalenceClass = {key: val for key, val in equivalenceClass.items() if val != temp}

        sortedTemp = sorted(temp)

        fixedNode = sortedTemp[0]

        condition.append([fixedNode, sortedTemp])

        newMappings = []

        for map in theMappings:
            for i in range(0, len(map)):
                if map[i] == fixedNode and map[i] == mappedHNodes[i]:
                    newMappings.append(map)

        self.findCondition(mappedHNodes, newMappings, condition, equivalenceClass)

        return condition


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
        condition = self.algorithm2_modified_for_equivalance_class(queryGraph, h)
        print("Size condition: %d" % len(condition))

        for con in condition:
            print("%d => " % con[0], end='')
            for value in con[1]:
                print("%d - " % value, end='')
            print("")
        print("")

        inputGraphDegSeq = inputGraph.getNodesSortedByDegree(queryGraph.getOutDegree(h))
        print("h neighbor size: %d" % queryGraph.getNeighbors(h).size())

        f = []
        mappingCount = 0

        for value in inputGraphDegSeq:
            f[h] = value
            mappingCount += self.isomorphicExtension(f, queryGraph, inputGraph, condition)

        return mappingCount
