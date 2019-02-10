class TreeNode:
    def __init__(self, namevalue, occrtimes, parentnode):
        self.name = namevalue
        self.times = occrtimes
        self.nextNode = None
        self.parent = parentnode
        self.subNode = {}


class FpTree:
    '''
    the structure of FpTree:
    rootNode: root node of fptree
    header: a table to store the haed of node link
    '''
    def __init__(self):
        self.rootNode = TreeNode('Null Set', 1, None)
        self.header = None

    def build_tree(self, itemsets, minsupport):
        '''
        use this function to build a fptree
        :param itemsets: dataset
        :param minsupport: minimum support
        :return:
        '''
        # create the table of head node link
        self.create_header(itemsets, minsupport)
        # construct the fptree
        self.create_tree(self.header, itemsets)

    def get_fptree(self):
        return self.rootNode

    def get_header(self):
        return self.header

    def create_header(self, itemsets, minsupport):
        '''
        create the table of head node link
        :param itemsets:
        :param minSup: minimum support
        :return:
        '''
        # scan the data for the first time
        headerTable = {}
        # get the appearent time of each item
        for trans in itemsets:
            for item in trans:
                if item in headerTable:
                    headerTable[item] = headerTable[item] + itemsets[trans]
                else:
                    headerTable[item] = itemsets[trans]
        # store the item whose appeared times > min support
        newheader = {}
        for key in headerTable.keys():
            if headerTable[key] >= minsupport:
                newheader[key] = [headerTable[key], None]
        # if no item reach the min support, return none
        if len(newheader) == 0:
            return None
        self.header = newheader

    def create_tree(self, header, dataset):
        '''
        create fp tree
        :param header:
        :param dataset:
        :return:
        '''
        # if header is none, do not need to build tree
        if header is None:
            return None
        freqItemSet = set(header.keys())
        # create root of fptree
        rootNode = TreeNode('Null Set', 1, None)  # 根节点
        # scan the data for second time
        # deduce the ordered frequent items
        for tranSet, count in dataset.items():
            itemset = {}  # one set of items
            for item in tranSet:
                # filter the items not in freqItemSet
                # only keep the items whose appeared time reach min support
                if item in freqItemSet:
                    # record the occurred frequency
                    itemset[item] = header[item][0]
            if len(itemset) > 0:
                # sort the itemsets according to occurred frequency
                ordereditemset = sorted(itemset.items(), key=lambda p: p[1], reverse=True)
                ordereditems =[]
                for item in ordereditemset:
                    ordereditems.append(item[0])
                # insert data to fptree, update fptree
                self.insert_item(ordereditems, rootNode, header, count, 0)
        self.rootNode = rootNode

    def insert_item(self, itemset, treenode, treeheader, count, num):
        '''
        insert data to fptree, update fptree
        :param itemset:
        :param treenode:
        :param treeheader:
        :param count:
        :param num: to record the num+th item in itemset
        :return:
        '''
        if itemset[num] in treenode.subNode:
            # if this item is in the child nodes of current node
            # increase the times of node
            treenode.subNode[itemset[num]].times += count
        else:
            # if the item not in child nodes
            # else create a new node
            treenode.subNode[itemset[num]] = TreeNode(itemset[num], count, treenode)
            # update the node list
            if treeheader[itemset[num]][1] is None:
                # if head of node link is none
                # link this node as head node
                treeheader[itemset[num]][1] = treenode.subNode[itemset[num]]
            else:
                # else find the last one in node list then link this node
                self.set_nextNode(treeheader[itemset[num]][1], treenode.subNode[itemset[num]])
        if len(itemset) > num + 1:
            # recursion
            # inset the rest data in items to tree
            self.insert_item(itemset, treenode.subNode[itemset[num]], treeheader, count, num+1)

    def set_nextNode(self, node, nextnode):
        '''

        :param node:
        :param nextnode:
        :return:
        '''
        # find the last one in node link
        while node.nextNode is not None:
            node = node.nextNode
        # add this node at the end of link
        node.nextNode = nextnode

    def printTreeList(self, node):
        '''

        :param node:
        :return:
        '''
        printlist = []
        printlist.append(str(node.name) + ':' + str(node.times))
        # if current node has child node
        if len(node.subNode) != 0:
            # insert the child node list to the printlist
            for keys in node.subNode:
                # recursion
                sublist = self.printTreeList(node.subNode[keys])
                printlist.append(sublist)
            return printlist
        else:
            return printlist

    def treeDisplay(self):
        '''
        print the tree
        store the tree in a list
        :return:
        '''
        # get the root node of fptree
        root = self.get_fptree()
        treedisplay = list([])
        # append the root node to the list
        treedisplay.append('Null set:1')
        #  traversal the child node
        for childnode in root.subNode:
            treedisplay.append(self.printTreeList(root.subNode[childnode]))
        print(treedisplay)

def prePath(node, prefixpath):
    '''
    add items to a prefix path ,update the prefix path
    :param node:
    :param prefixPath:
    :return:
    '''
    if node.parent is not None:
        # add a item to prepath update the prepath
        prefixpath.append(node.name)
        # recursion
        prePath(node.parent, prefixpath)

def findCondtionData(treeNode):
    '''
        find the data to build a conditional fptree
     by finding the prefix path of the node
    :param treeNode:
    :return:
    '''
    condPath = {}
    # find all the prefix path through node link
    while treeNode is not None:
        prepath = []
        prePath(treeNode, prepath)
        if len(prepath) > 1:
            # the occurred times of items in a path is decided by the times of final node
            condPath[frozenset(prepath[1:])] = treeNode.times
        # get next node in node link
        treeNode = treeNode.nextNode
    return condPath


def buildCondTree(headertable, minsupport, preitem, freqItemList):
    '''
    build a conditional fp tree
    :param headertable:
    :param minsupport:
    :param preitem:  record which item's condtional tree
    :param freqItemList: record the frequent item sets
    :return:
    '''
    condpatternitems = sorted(headertable.items(), key=lambda p: p[0])
    for item in condpatternitems:
        basePatitem = item[0]
        # record the pre item
        newFreqSet = preitem.copy()
        # add current item to the set
        newFreqSet.add(basePatitem)
        freqItemList.append(newFreqSet)
        # get the conditional itemsets by findind the prefix Path
        condPattBases = findCondtionData(headertable[basePatitem][1])
        # use the conditional itemsets to construct condtional tree
        contree = FpTree()
        contree.build_tree(condPattBases, minsupport)
        # get the header of condtional tree
        conheader = contree.get_header()
        if conheader is not None:
            buildCondTree(conheader, minsupport, newFreqSet, freqItemList)
            # print the condtional tree whose height is larger than 1
            # ------question (b)-----
            contree.treeDisplay()
