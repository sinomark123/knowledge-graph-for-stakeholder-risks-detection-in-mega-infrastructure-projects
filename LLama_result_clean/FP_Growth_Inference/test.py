import my_fpgrowth as fp
from utils import *
import copy
import time

# Test the fpgrowth algorithm

test_list = [
    ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
    ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
    ['b', 'f', 'h', 'j', 'o'],
    ['b', 'c', 'k', 's', 'p'],
    ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n'],
    ['f', 'c','g','s']
]

itemsetList = [
    ["f", "c", "a", "m", "p"],
    ["f", "b" ],
    ["c", "b", "p"],
    ["f", "c", "a", "b", "m"],
]

headerTable = {
    "f": [0, None],
    "c": [0, None],
    "a": [0, None],
    "b": [0, None],
    "m": [0, None],
    "p": [0, None]
}

def innerTreeHook(root: SycNode):
    print("Root: ", root())
    print("Childs are:", " ".join([x[0]() for x in root.children.values()]))
    for kc, vc in root.children.items():
        for vcc in vc:
            innerTreeHook(vcc)
        # innerTreeHook(vc)

def innerHeaderTableHook(headerTable):
    presented = headerTable.copy()
    for k, v in presented.items():
        print(k, v[0], v[1](), v[2]())
        temp = copy.deepcopy(v[2])
        while temp.next:
            temp = temp.next
            print(temp(), temp.next)


if __name__ == "__main__":
    # r1, r2 = fp.fpgrowth(test_list, 0.5, 0.5)
    # time1 = time.time()
    # root = SycNode("root", None)
    # headerTable, root = general_call(itemList=itemsetList, minSup=2, root=root)
    # innerTreeHook(root)
    # print("The Computation Time is:", time.time() - time1)

    time2 = time.time()
    itemset, val1 = fp.fpgrowth(itemSetList=test_list, minSupRatio=0.5, minConf=0.5)
    print("Original Computation Time is:", time.time() - time2)
    # innerTreeHook(root)
    innerHeaderTableHook(headerTable)

    """
    root, newItemList = SycNode("root", None), []
    for itemset in itemsetList:
        every_point = linkedListInitiallizer(itemset)
        every_point[0].parent = root
        # if list not null: do append else create new list
        if every_point[0].itemName in root.children:
            root.children[every_point[0].itemName].append(every_point[0])
        else:
            root.children[every_point[0].itemName] = [every_point[0]]
        # root.children[every_point[0].itemName].append(every_point[0])
        newItemList.append(every_point)
    # Test the tree builder
    headerTable = treeBuilder(newItemList, [None], headerTable)
    innerTreeHook(root)
    innerHeaderTableHook(headerTable)
    """