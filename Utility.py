from Graph import Graph
from typing import Dict, List
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

    def getMostConstrainedNeighbour(self, domain: List[int],
                                    queryGraph: Graph) -> int:
        """
        Method to find the most constrained neighboring node of mapped nodes in the query graph.

        :param domain: the current partial mapping of query graph to target graph
        :param queryGraph: the query graph
        :return: int corresponding to most constrained node
        """
        "get all neoghbors of already mapped nodes"
        "NO Duplicates"
        #print("------ GET MOST CONSTRAINED NEIGHBOR DEBUG --------")
        neighborList = []
        self.chooseNeightboursOfRange(domain, queryGraph, neighborList)

        neighborListSize = len(neighborList)

        if neighborListSize == 1:
            print("neighbor return %d" % neighborList[0])
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

    def chooseNeightboursOfRange(self, usedRange: List[int],
                                 inputGraph: Graph,
                                 neightborList: List[int]):
        """
        Method to get all neighbors of a set of nodes in a graph (no duplicate neighbors allowed)
            :param   usedRange: the IDs of the target set of nodes
            :param   inputGraph: the graph to be searched for motif
            :param   neightborList: the reference to the return list of neighbors
            :return:  modified neighborList
        """
        #print("----- CHOOSE NEIGHBOR OF RANGE DEBUG ------")
        for range in usedRange:
            local = inputGraph.getNeighbors(range)
            for loc in local:
                if int(loc) not in usedRange:
                    neightborList.append(int(loc))
        neightborList.sort()
        neightborList[:] = list(set(neightborList))

        return neightborList

    def isNeighbourIncompatible(self, inputGraph: Graph,
                                n: int,
                                partialMap: Dict[int, int],
                                neighborsOfM: List[int]) -> bool:
        """
        Method to check if a neighbor node n of the target graph could be mapped to a node m of the query graph
        :param inputGraph: target graph
        :param n: ID of the node n in the target graph
        :param partialMap: the current partial mapping from query graph to target graph #dit
        :param neighborsOfM: the list of neighbors of node m to the query graph
        :return: boolean True if node n can be mapped to node m, otherwise false
        """
        for d in partialMap:
            print("D is %d" %d)
            neighborsOfd: List[int] = inputGraph.getNeighbors(partialMap[d])
            if d in neighborsOfM:
                print("d is in neighborsOfM")
                if n not in neighborsOfd:
                    print("--n is not in neighborsOfD")
                    return True
            else:
                if n in neighborsOfd:
                    print("n is in neighborsOfD")
                    return True
        return False

    def checkSymmetryBreak(self, fixed: int,
                           nodesToCheck: List[int],
                           partialMap: Dict[int, int],
                           m: int,
                           n: int) -> bool:
        """
        Method to check if a mapping from node m of query graph to node n of target graph satisfy the symmetry-breaking conditions
        :param fixed: the representative node from each equivalence class
        :param nodesToCheck: the symmetry-breaking conditions
        :param partialMap: the current partial mapping from query graph to target graph
        :param m: ID number of node m of query graph
        :param n: ID number of node n of target graph
        :return: True if the symmetry-breaking condition is satisfied and the mapping is okay, False == mapping not okay
        """
        if m not in nodesToCheck or (m != fixed):   # and partialMap.index(fixed)== partialMap[-1]):
            return True

        fixedLabel = 0
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

    def equalDtoH(self, obj1: List[int],
                  obj2:List[int]) -> bool:
        """
        Helper function to check if the list of keys of obj1 (D) is equal to obj2 (H)
        Equal if all elements of object 1's keys are present in object 2,
        and the elements don't have to be in the same order between objects
        :param obj1: vectorList of queryGraph
        :param obj2: list of keys
        :return: boolean isEqual
        """
        temp = []
        if len(obj1) != len(obj2):
            return False
        for key in obj1:
            temp.append(int(key))
            if temp.sort() != obj2.sort():
                return False
        return True

    def findCondition(self, mappedHNodes: List[int],
                      theMappings: List[List[int]],
                      condition: Dict[int, List[int]],
                      equivalenceClass) -> Dict[int, List[int]]:
        """
        Method to find the symmetry-breaking cinditions by Grochow-Kellis.
        *****NOTE*****: should combine this with Algorithm2_Modified_For_Equivalence_Class()
        :param mappedHNodes: List
        :param theMappings: 2D list
        :param condition: Dictionary
        :param equivalenceClass: Dictionary
        :return:
        """
        print("----Find conditon Debug----")
        if len(theMappings) == 1:
            print("find condtion base case")
            return condition

        equivalenceFilter = {}
        for i in range(0, len(mappedHNodes)):
            equivalenceFilter[i] = set()

        for maps in theMappings:
            print("print theMappings")
            for i in range(0, len(maps)):
                equivalenceFilter[i].add(maps[i])
                print("    i: %d maps[i]: %d" % (i, maps[i]))

        filterkey = next(iter(equivalenceFilter))
        maxSize = len(equivalenceFilter[filterkey])
        print("Max size - %d" % maxSize)

        if len(equivalenceClass) == 0:
            temp = set(equivalenceFilter[filterkey])
        else:
            classitem = next(iter(equivalenceClass))
            temp = set(equivalenceClass[classitem])

        #entry is a reference to a set
        for entry in equivalenceFilter:
            print("found entry")
            if len(equivalenceFilter[entry]) > 1:
                print("    has more than 1 entry: %d" % len(equivalenceFilter[entry]))
                if len(equivalenceFilter[entry]) > maxSize:
                    maxSize = len(equivalenceFilter[entry])
                    temp = set(equivalenceFilter[entry])
                    print("    update max size %d" % maxSize)

        equivalenceClass.discard(temp)
        sortedTemp = sorted(temp)
        fixedNode = sortedTemp[0]
        print("fixed node is: %d" % fixedNode)

        if fixedNode in condition:
            condition[fixedNode].append(sortedTemp)
        else:
            condition[fixedNode] = [sortedTemp]

        newMappings = []

        for maps in theMappings:
            for i in range(0, len(maps)):
                if maps[i] == fixedNode and maps[i] == mappedHNodes[i]:
                    print("map[%d] - %d" % (i, maps[i]))
                    newMappings.append(maps)
        print("find condition Recursive call")
        self.findCondition(mappedHNodes, newMappings, condition, equivalenceClass)
        print("end of find condition")
        return condition

    def isomorphicExtension(self, partialMap: Dict[int, int],
                            queryGraph: Graph,
                            inputGraph: Graph,
                            symBreakCondition: Dict[int, List[int]]) -> int:
        """
        Method to count all of the isomorphic extensions (no duplicates) of a partial map between the query graph and the target graph
        :param partialMap: the current partial mapping from query graph to target graph #is a dictionary
        :param queryGraph: reference to the query graph
        :param inputGraph: reference to the target graph
        :param symBreakCondition: set of symmetry-breaking conditions
        :return: int representing the count of all the isomorphic extensions
        """
        print("----ISOMORPHIC EXTENSION DEBUG ------")
        listOfIsomorphisms = 0  #tracks number of isomorphisms
        partialMapValuesG: List[int] = []  # list
        partialMapKeysH: List[int] = []  # list

        '''extract list of keys and list values from paritalMap'''
        for maps in partialMap:
            print("Keys: %d Values: %d" % (maps, partialMap[maps]))
            partialMapValuesG.append(int(partialMap[maps]))
            partialMapKeysH.append(int(maps))

        mapValueOriginal: List[int] = list(partialMapValuesG)
        mapKeyOriginal: List[int] = list(partialMapKeysH)
        partialMapValuesG.sort()
        partialMapKeysH.sort()

        if self.equalDtoH(queryGraph.getVertexList(), partialMapKeysH):
            print("************ EQUAL DtoH - base case - FOUND ISOMORPHISM ************")
            return 1

        m: int = self.getMostConstrainedNeighbour(partialMapKeysH, queryGraph)
        if m < 0:
            print("m less than 0 - base case")
            return 0

        neighborsOfM: List[int] = queryGraph.getNeighbors(m)
        bestMappedNeighborOfM: int = 0
        for neighbor in neighborsOfM:
            print("best mapped neighbor of m: %d" % neighbor)
            bestMappedNeighborOfM: int = neighbor
            break

        possibleMappingNodes: List[int] = []
        for node in inputGraph.getNeighbors(partialMap[bestMappedNeighborOfM]):
            if node not in partialMapValuesG:
                print("found node: %d" % node)
                possibleMappingNodes.append(int(node))

        partialMapKeysHSize: int = len(partialMapKeysH)
        for i in range(0, partialMapKeysHSize):
            neighborsOfMappedGNode: List[int] = (inputGraph.getNeighbors(mapValueOriginal[i]))
            temp: List[int] = []
            if int(mapKeyOriginal[i]) in neighborsOfM:
                for node in possibleMappingNodes:
                    if node in neighborsOfMappedGNode:
                        print("update possible Mapping node: %d" % node)
                        temp.append(int(node))
                possibleMappingNodes = temp.copy()
            else:
                for node in possibleMappingNodes:
                    if node not in neighborsOfMappedGNode:
                        print("update possible mapping node: %d" % node)
                        temp.append(int(node))
                possibleMappingNodes = temp.copy()

        for n in possibleMappingNodes:
            print("possibleMappingNode is %d" % n)
            if not self.isNeighbourIncompatible(inputGraph, n, partialMap, neighborsOfM):
                print("neighbor: %d is incompatible" % n)
                skip = False
                for condition in symBreakCondition:
                    print("condition is: %d" % condition)
                    if not self.checkSymmetryBreak(symBreakCondition[condition][0][0], symBreakCondition[condition][0], partialMap, m, n):
                        print("symmetry break condition is FALSE: %d, %d" % (condition, n))
                        skip = True
                        break
                if skip:
                    continue
                newPartialMap = partialMap.copy()  # dict of pairs
                newPartialMap[m] = n

                print("isomorphic recursive call")
                subList = self.isomorphicExtension(newPartialMap, queryGraph, inputGraph, symBreakCondition)
                print("end of isomorphic recursive call")
                listOfIsomorphisms += subList

        return listOfIsomorphisms

    def isomorphicExtensionForEquivalenceClass(self, partialMap: Dict[int, int],
                                               queryGraph: Graph,
                                               inputGraph: Graph,
                                               mappedHNodes: List[int]) -> List[List[int]]:
        """
        Helper method to find all of the isomorphic extensions of a partial map between the query graph and itself
        :param partialMap: dictionary
        :param queryGraph: Graph
        :param inputGraph: Graph - same as query graph
        :param mappedHNodes: List
        :return:
        """
        print("-----Isomorphic Extension for Equivilance Class DEBUG ------")

        result = []                 #2d list
        listOfIsomorphisms = []     #2d list
        partialMapValuesG = []      #list
        partialMapKeysH = []        #list

        '''extract list of keys and list of values from partialMap'''
        for maps in partialMap:
            print("Map key - %d Map value - %d" % (maps, partialMap[maps]))
            partialMapValuesG.append(int(partialMap[maps]))
            partialMapKeysH.append(maps)

        mapValueOriginal = list(partialMapValuesG)
        mapKeyOriginal = list(partialMapKeysH)

        partialMapValuesG.sort()
        partialMapKeysH.sort()

        if self.equalDtoH(queryGraph.getVertexList(), partialMapKeysH) == True:
            print("D to H is true")
            mappedHNodes[:] = list(mapKeyOriginal)
            result.append(mapValueOriginal)
            return result

        m = int(self.getMostConstrainedNeighbour(partialMapKeysH, queryGraph))
        print("Most constrained neighbor is: %d" % m)
        if m < 0:
            return listOfIsomorphisms
        
        neighbourRange = []     #list
        neighbourRange = self.chooseNeightboursOfRange(partialMapValuesG, inputGraph, neighbourRange)

        neighborsOfM = queryGraph.getNeighbors(m)

        for n in neighbourRange:
            print("neighborRange: %d" % n)
            if not self.isNeighbourIncompatible(inputGraph, n, partialMap, neighborsOfM):
                print("    neighbor is compatible")
                newPartialMap = partialMap.copy()
                print("    %d - %d" % (m, n))
                newPartialMap[m] = int(n)
                print("recursive call - isomorphic extension for equivalence")
                subList = self.isomorphicExtensionForEquivalenceClass(newPartialMap, queryGraph, inputGraph, mappedHNodes)
                for item in subList:
                    listOfIsomorphisms.append(item)
        return listOfIsomorphisms

    def algorithm2_modified_for_equivalance_class(self, queryGraph: Graph,
                                                  inputGraph: Graph,
                                                  fixedNode: int) -> Dict[int, List[int]]:
        """
        Method to find the symmetry-breaking conditions by Grochow-Kellis. It starts by choosing one node to be the anchor point and create conditions from
        :param queryGraph: reference to query graph
        :param fixedNode: the node we choose to be fixed as the anchor for symmetry
        :return: a set of symmetry-breaking conditions for each represented node from each equivalance class
        """
        print("-----Alg2_modifiedforequivlanceclass DEBUG-----")
        vertexList = queryGraph.getVertexList()
        h = next(iter(vertexList))

        print("h for inputDegSeq is: %d" % h)
        print(queryGraph.getOutDegree(h))

        inputGraphDegSeq = inputGraph.getNodesSortedByDegree(queryGraph.getOutDegree(h))
        theMappings = []        #2d list
        mappedHNodes = []       #list

        i = 0
        print("inputGraphDegSeq items:")
        for item in inputGraphDegSeq:
            print(item)

        for item in inputGraphDegSeq:
            print("\nh is %d. Element %d of inputGraphDegSeq %d" % (h, i, item))
            i+=1
            f = {}  # dictionary of pairs
            f[h] = int(item)
            mappings = self.isomorphicExtensionForEquivalenceClass(f, queryGraph, queryGraph, mappedHNodes)
            #theMappings
            for maps in mappings:
                theMappings.append(maps)

        condition = {}          #dict
        #TODO might change to set
        equivalenceClass = set()

        return self.findCondition(mappedHNodes, theMappings, condition, equivalenceClass)

    def algorithm2_modified(self, queryGraph: Graph,
                            inputGraph: Graph,
                            h: int) -> int:
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

        print("############ DEBUG CONDITION ######################")
        condition = self.algorithm2_modified_for_equivalance_class(queryGraph, queryGraph, h)
        print("############ FINISH FINDING CONDITION ######################")

        print("\nSize condition: %d" % len(condition))
        for con in condition:
            print(str(con) + " => " + str(condition[con][0]), end='')
            print("")

        inputGraphDegSeq = inputGraph.getNodesSortedByDegree(queryGraph.getOutDegree(h))
        print("h neighbor size: %d" % len(queryGraph.getNeighbors(h)))

        mappingCount = 0
        print("----- ALG2_Modified DEBUG -----")
        f: Dict[int, int] = {}
        i = 0
        for value in inputGraphDegSeq:
            print("\nh is: %d. Element %d of inputGraphDegSeq[i] = %d" % (h, i, value))
            i+=1

            f[h] = value
            mappingCount += self.isomorphicExtension(f, queryGraph, inputGraph, condition)

        return mappingCount
