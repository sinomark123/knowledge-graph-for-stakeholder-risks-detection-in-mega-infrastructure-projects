from csv import reader
from collections import defaultdict
from itertools import chain, combinations
from multipledispatch import dispatch
import multiprocessing
from typing import *

dispatcher=dispatch()

class Node:
    def __init__(self, itemName, frequency, parentNode):
        self.itemName = itemName
        self.count = frequency
        self.parent = parentNode
        self.children = {}
        self.next = None

    def increment(self, frequency):
        self.count += frequency

    def display(self, ind=1):
        print('  ' * ind, self.itemName, ' ', self.count)
        for child in list(self.children.values()):
            child.display(ind+1)

class SycNode:
    def __init__(self, itemName, parentNode):
        self.itemName = itemName
        self.parent = parentNode
        self.children = {}
        self.next = None
        self.freq = 0

    # def __getitem__(self):
    #     return self

    def increment(self, frequency):
        self.freq += frequency

    def def_freq(self, frequency):
        self.freq = frequency

    def display(self, ind=1):
        print('  ' * ind, self.itemName, ' ', self.count)
        for child in list(self.children.values()):
            child.display(ind+1)

def getFromFile(fname):
    itemSetList = []
    frequency = []
    
    with open(fname, 'r') as file:
        csv_reader = reader(file)
        for line in csv_reader:
            line = list(filter(None, line))
            itemSetList.append(line)
            frequency.append(1)

    return itemSetList, frequency

# ---------------------------------------------------------------------------------------

def simlarity(item1: object, item2: object):
    """
    simlarity of two short phrases, use cosine to compute on vector
    """

    return 0

def simlarity_compute(obj: object, obj_vector: list[object]):
    """
    simlarity of a single short phrase with entire corpus
    item is expected to be wrapped in a certain class, prepare to be put in multi-processing
    """
    sim = [(simlarity(obj, item), item) for item in obj_vector]
    sim.sort(key=lambda x: x[0], reverse=True)
    for idx, exam in enumerate(sim):
        if exam[0] <= 0.91:
            return sim[:idx] if idx else [(0, False)]

def sparse_vector(vector: dict[object, int]):
    """
    convert a list of object into a sparse vector
    """
    samples = list(vector.keys())
    grocery = []
    for idx in range(len(samples)):
        # add to multi-processing pool, remember to copy the original one
        temp_samples = samples.copy()
        target, rest = temp_samples[idx], temp_samples[:idx] + temp_samples[idx+1:]
        p = multiprocessing.Process(target=simlarity_compute, args=(target, rest))
        grocery.append(p)
    for item in grocery:
        item.start()
        # item.join()
    for item in grocery:
        item.join()
    return vector

@overload
def treeBuilder(item, forwardNode):
    """
    try to use tree shape to build the linkedlist, be noticed at this stage
    item is passed for next node
    """
    current = SycNode(item, forwardNode)
    forwardNode.children[item] = current
    current.next = treeBuilder(item, current)
    return current

def treeBuilder(item, forwardNode):
    """
    outside treeBuilder, should assign a loop for value 
    """
    ...

def linkedListInitiallizer(itemList: list):
    """
    we requrie the item in list is already sorted in frequency decending order
    """
    root = SycNode(itemList[0], None)
    parentNode = root
    for item in itemList[1:]:
        currentNode = SycNode(item, parentNode)
        parentNode.children[item] = currentNode
        parentNode.next = currentNode
        parentNode = currentNode
    return root

@dispatch.register
def constructTree(itemset_list: list):
    """
    itemset_list: list of list of items
    """
    pool = multiprocessing.Pool(process=2)
    res = pool.map(linkedListInitiallizer, itemset_list)
    pool.close()
    pool.join()

    return res

def listDistinction(linkedList: List[List[str]], freq: Dict[str, int]):
    """
    now build header table and linked with head element
    be remind to change the pointer after Node combination
    """
    headerList: Dict[str, SycNode] = OrderedDict(freq, None)
    for freq_str, idx in freq.items():
        for item in linkedList:
            if not headerList[item[idx]]:
                headerList[item[idx]].freq+=1
            else:
                headerList[item[idx]] = SycNode(item[idx], None)
        ...
    ...

# ---------------------------------------------------------------------------------------

@dispatch.register
def constructTree(itemSetList, frequency, minSup):
    headerTable = defaultdict(int)
    # Counting frequency and create header table
    for idx, itemSet in enumerate(itemSetList): ## supposed to be optimzed..?
        for item in itemSet:
            headerTable[item] += frequency[idx] # 1

    # Deleting items below minSup
    headerTable = dict((item, sup) for item, sup in headerTable.items() if sup >= minSup)
    if(len(headerTable) == 0):
        return None, None

    # HeaderTable column [Item: [frequency, headNode]]
    for item in headerTable:
        headerTable[item] = [headerTable[item], None]

    # Init Null head node
    fpTree = Node('Null', 1, None)
    # Update FP tree for each cleaned and sorted itemSet
    for idx, itemSet in enumerate(itemSetList):
        itemSet = [item for item in itemSet if item in headerTable]
        itemSet.sort(key=lambda item: headerTable[item][0], reverse=True)
        # Traverse from root to leaf, update tree with given item
        currentNode = fpTree
        for item in itemSet:
            currentNode = updateTree(item, currentNode, headerTable, frequency[idx])

    return fpTree, headerTable

def updateHeaderTable(item, targetNode, headerTable):
    if(headerTable[item][1] == None):
        headerTable[item][1] = targetNode
    else:
        currentNode = headerTable[item][1]
        # Traverse to the last node then link it to the target
        while currentNode.next != None:
            currentNode = currentNode.next
        currentNode.next = targetNode

def updateTree(item, treeNode, headerTable, frequency):
    if item in treeNode.children:
        # If the item already exists, increment the count
        treeNode.children[item].increment(frequency)
    else:
        # Create a new branch
        newItemNode = Node(item, frequency, treeNode)
        treeNode.children[item] = newItemNode
        # Link the new branch to header table
        updateHeaderTable(item, newItemNode, headerTable)

    return treeNode.children[item]

def ascendFPtree(node, prefixPath):
    if node.parent != None:
        prefixPath.append(node.itemName)
        ascendFPtree(node.parent, prefixPath)

def findPrefixPath(basePat, headerTable):
    # First node in linked list
    treeNode = headerTable[basePat][1] 
    condPats = []
    frequency = []
    while treeNode != None:
        prefixPath = []
        # From leaf node all the way to root
        ascendFPtree(treeNode, prefixPath)  
        if len(prefixPath) > 1:
            # Storing the prefix path and it's corresponding count
            condPats.append(prefixPath[1:])
            frequency.append(treeNode.count)

        # Go to next node
        treeNode = treeNode.next  
    return condPats, frequency

def mineTree(headerTable, minSup, preFix, freqItemList):
    # Sort the items with frequency and create a list
    sortedItemList = [item[0] for item in sorted(list(headerTable.items()), key=lambda p:p[1][0])] 
    # Start with the lowest frequency
    for item in sortedItemList:  
        # Pattern growth is achieved by the concatenation of suffix pattern with frequent patterns generated from conditional FP-tree
        newFreqSet = preFix.copy()
        newFreqSet.add(item)
        freqItemList.append(newFreqSet)
        # Find all prefix path, constrcut conditional pattern base
        conditionalPattBase, frequency = findPrefixPath(item, headerTable) 
        # Construct conditonal FP Tree with conditional pattern base
        conditionalTree, newHeaderTable = constructTree(conditionalPattBase, frequency, minSup) 
        if newHeaderTable != None:
            # Mining recursively on the tree
            mineTree(newHeaderTable, minSup,
                       newFreqSet, freqItemList)

def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))

def getSupport(testSet, itemSetList):
    count = 0
    for itemSet in itemSetList:
        if(set(testSet).issubset(itemSet)):
            count += 1
    return count

def associationRule(freqItemSet, itemSetList, minConf):
    rules = []
    for itemSet in freqItemSet:
        subsets = powerset(itemSet)
        itemSetSup = getSupport(itemSet, itemSetList)
        for s in subsets:
            confidence = float(itemSetSup / getSupport(s, itemSetList))
            if(confidence > minConf):
                rules.append([set(s), set(itemSet.difference(s)), confidence])
    return rules

def getFrequencyFromList(itemSetList):
    frequency = [1 for _ in range(len(itemSetList))]
    return frequency