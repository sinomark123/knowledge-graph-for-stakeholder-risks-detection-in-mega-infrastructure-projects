from csv import reader
from collections import defaultdict, Counter, OrderedDict
from itertools import chain, combinations
from typing import Any
from multipledispatch import dispatch
import multiprocessing as mp
from typing import *

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
        self.next = None # point to the longest item in next level, does this necessary?
        self.freq = 1 # not total frequency but that in the same level

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.itemName

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

def freqCounter(itemSetList: list[list[str]]):
    """
    count the frequency of each item in the itemset
    """
    itemList = list(chain(*itemSetList))
    freq = Counter(itemList)
    return OrderedDict(freq.most_common())

def itemSort(itemSetList: list[list[str]], freq: dict[str, int]):
    """
    sort the item in the itemset by frequency
    """
    for item in itemSetList:
        item.sort(key=lambda x: freq[x], reverse=True)
    return itemSetList

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
        p = mp.Process(target=simlarity_compute, args=(target, rest))
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

def listItemCheck(key_list: list[list[SycNode]]):
    for outlier in key_list:
        print(" ".join([val() for val in outlier]), " ")
        print("\n")

def dict_update(dict1: dict[list[SycNode]], dict2: dict[list[SycNode]], update_node: SycNode):
    """
    update dict1 with dict2, if dict2 has the same key with dict1, update the value
    """
    for k,v in dict2.items():
        if k in dict1.keys():
            dict1[k] += v
        else:
            dict1[k] = v
        for item in v:
            item.parent = update_node
        # should I add this?
        dict2[k] = None
    return dict1

def treeBuilder(itemList, headerTable):
    """
    outside treeBuilder, should assign a loop for value 
    itemList = construcTree(itemSetList)
    """
    # assume get multiple list from construcTree
    # --------- temperary optimize option ---------
    longest_len = list(headerTable.keys())
    key_list: list[list[SycNode]] = itemList
    # --------- temperary optimize option ---------
    for col in range(len(longest_len)):
        horizontal_pointer = headerTable[longest_len[col]]
        for knum in range(len(key_list)):
            if not len(key_list[knum]) or key_list[knum][0].itemName != longest_len[col]:
                continue
            # headtable corresponding element total frequency add 1
            parent_node = key_list[knum][0].parent
            children_list = parent_node.children[key_list[knum][0].itemName]
            if len(children_list)>1 and (key_list[knum][0] != children_list[0]):
                if key_list[knum][0] not in children_list:
                    raise ValueError("Logic Error, Node not in the children list")
                the_only_one = children_list[0]
                # combine the two node
                the_only_one.freq += 1
                # combine the children
                """
                Why not dict.update? becuase dict.update will not extend list, but overwrite the list
                Can I overwrite 'update' so it can update both children node and parent node?
                """
                the_only_one.children = dict_update(the_only_one.children, key_list[knum][0].children, the_only_one)
                # combine finished
                # update itemlist and parent node children list
                children_list.remove(key_list[knum][0])
                key_list[knum].pop(0)
                continue
            
            if horizontal_pointer[1]!=None:
                horizontal_pointer[1].next = key_list[knum][0]
            elif horizontal_pointer[1]==None:
                horizontal_pointer.append(key_list[knum][0])
            horizontal_pointer[1] = key_list[knum][0]
            # to clean the list, ensure sorted linkedlist only need to check the first element
            key_list[knum].pop(0)
    return headerTable


def linkedListInitiallizer(itemList: list, order: list[str]):
    """
    we requrie the item in list is already sorted in frequency decending order
    """
    firstStep = list(set(itemList).intersection(set(order)))
    if len(firstStep) <= 1:
        return []
    itemList = sorted(firstStep, key=lambda x: order.index(x))
    root = SycNode(itemList[0], None)
    parentNode, linked_list = root, [root]
    for item in itemList[1:]:
        currentNode = SycNode(item, parentNode)
        # children is a dict, key is the item name, value is a list of node
        parentNode.children[item] = [currentNode]
        parentNode = currentNode
        linked_list.append(currentNode)
    return linked_list

@dispatch(list)
def constructTree(itemset_list: list):
    """
    itemset_list: list of list of items
    """
    pool = mp.Pool(process=2)
    res = pool.map(linkedListInitiallizer, itemset_list)
    pool.close()
    pool.join()
    return res

resultList: list[list[SycNode]] = []
def logReesult(result):
    resultList.append(result)

def general_call(itemList: list[list[str]], minSup: int, root: SycNode):
    # a step may need optimzed
    global resultList
    headerTable: dict[str, int] = {k:[v,None] for k, v in freqCounter(itemList).items() if v>=minSup}
    itemOrder = list(headerTable.keys())

    print("The length of resultList before put in is:", len(itemList))
    pool = mp.Pool()
    for subItem in itemList:
        pool.apply_async(linkedListInitiallizer, args=(subItem, itemOrder), callback=logReesult)
    pool.close()
    pool.join()

    print("The length of resultList is:", len(resultList))

    for items in resultList:
        if not items: continue
        items[0].parent = root
        if items[0]() in root.children.keys():
            root.children[items[0].itemName].append(items[0])
        else:
            root.children[items[0].itemName] = [items[0]]

    headerTable = treeBuilder(resultList, headerTable)

    return headerTable, root

def conditionTree():
    ...

def patternRetrieve():
    ...
# ---------------------------------------------------------------------------------------

@dispatch(list, list, float)
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
    """
    Most time costed function, why recursion used here?
    """
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




"""
Old Code used for update FP tree
# ------------------------------------------------
Here is depcreated one since 'next' is left for headertable
trigger = 0
# if current checked Node owns the same parnet node with the previous checked node
for last_item in same_level_list:
    if last_item.parent == key_list[knum][0].parent:
        last_item.freq += 1
        next_node: SycNode = key_list[knum][0].next
        last_item.next = next_node
        next_node.parent, trigger = next_node, 1
        del key_list[knum][0]
        break
if trigger: continue
# ------------------------------------------------
current newly used code, less loop
parent_node = key_list[knum][0].parent
children_list = parent_node.children[key_list[knum][0].itemName]
if children_list>0:
    the_only_one = children_list[0]
    # combine the two node
    the_only_one.freq += 1
    # combine the children
    the_only_one.children.update(key_list[knum][0].children)
    for _,v in key_list[knum][0].children.items():
        v.parent = the_only_one
    # combine finished
    del key_list[knum][0]
    continue
"""