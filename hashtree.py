candidate_itemsets = [[1,2,4],[1,2,9], [1,3,5], [1,3,9], [1,4,7],[1,5,8],[1,6,7],[1,7,9],[1,8,9],\
                     [2,3,5],[2,4,7],[2,5,6],[2,5,7],[2,5,8],[2,6,7],[2,6,8],[2,6,9],[2,7,8],\
                     [3,4,5],[3,4,7],[3,5,7],[3,5,8],[3,6,8],[3,7,9],[3,8,9],\
                     [4,5,7],[4,5,8],[4,6,7],[4,6,9],[4,7,8],\
                     [5,6,7],[5,7,9],[5,8,9],[6,7,8],[6,7,9]]

class Node(object):
    def __init__(self, itemsets=None):
        '''
        define hashtree node
        :param itemsets: list
        '''
        self.leafnode = True       # bool value, if the node is lead:True  else:False
        self.level = 0             # the level of the node
        self.itemsets = itemsets   # if the node is leaf node store the itemsets
        self.subtree = None        # store the sub node of current node


class HashTree(object):
    '''
    define hashtree
    '''
    def __init__(self):
        self.root = None

    def initTree(self):
        '''
        init the root of tree
        :return:
        '''
        self.root = Node([])

    def putItemsets(self, candidateitemsets):
        '''

        :param candidate_itemsets: list
        :return:
        '''
        for i in range(len(candidateitemsets)):
            self.insertItem(candidateitemsets[i], self.root)
        return 0

    def insertItem(self, itemset, node):
        '''

        :param itemset: list
        :param node: Node
        :return:
        '''
        if node.leafnode == True:
            # if node is leaf node
            if len(node.itemsets) < 3:
                # leaf size smaller than max leaf size
                node.itemsets.append(itemset)
                return 0
            else:
                # exceed max leaf size, split the node
                self.splitNode(node, itemset)
                return 0
        else:
            # if the node isn't leaf node
            # recursion
            # do hash the item(the level+th item in the item set) and insert to the sub node
            self.insertItem(itemset, node.subtree[self.hashfunc(itemset,node.level)])
            return 0

    def splitNode(self, node, itemset):
        # change the mark of leadnode to False
        node.leafnode = False
        # split three child node for current node
        node.subtree = []
        for i in range(3):
            childnode = Node([])
            childnode.level = node.level+1
            node.subtree.append(childnode)
        # insert the itemsets data in current node to sub node
        for i in range(3):
            # by doing hash to decide insert in which sub node
            key = self.hashfunc(node.itemsets[i], node.level)
            self.insertItem(node.itemsets[i], node.subtree[key])
        # insert the new itemset to sub node
        key = self.hashfunc(itemset, node.level)
        self.insertItem(itemset, node.subtree[key])
        # delete the itemsets data of current node
        node.itemsets = None
        return 0

    def hashfunc(self, itemset, level):
        '''
        hash the level+th data in itemset
        :param itemset: list
        :param level: int
        :return:
        '''
        if itemset[level] % 3 == 1:
            return 0
        elif itemset[level] % 3 == 2:
            return 1
        elif itemset[level] % 3 == 0:
            return 2

    def printTree(self):
        print(self.getItem(self.root))
        return 0

    def getItem(self, node):
        treelist = []
        if node.leafnode == True:
            # if the node is leafnode get the itemset and insert to treelist
            if node.itemsets != None:
                if len(node.itemsets) == 1:
                    return node.itemsets[0]
                else:
                    for set in node.itemsets:
                        treelist.append(set)
                return treelist
            else:
                return None
        else:
            # if the node has child node, get the list
            for i in range(3):
                # recursion
                # get the itemset of childnode
                itemlist = self.getItem(node.subtree[i])
                treelist.append(itemlist)
            return treelist
        return treelist


if __name__ == '__main__':
    # instant hashtree
    hashtree = HashTree()
    hashtree.initTree()
    # input the candidate itemsets to build the hash tree
    hashtree.putItemsets(candidate_itemsets)
    # print hash tree according to the given example
    hashtree.printTree()


