#__all__     = []
__version__ = "0.1"
__author__  = "Jian Wang w13915984028@gmail.com"

import sys

# Tree for roman numeral matching
class TreeNode:
    def __init__(self, roman = "", key ="", value = 0, digit = 0):
        # whole roman, like "VII", for debug usage
        self.roman = roman 

        # key of this node, single, like "I", "V", "M"
        self.key = key

        # value in base 10 format, like (M) is 1000, (VII) is 7
        self.value = value 

        # digit (level) of current node
        # single is 1, tens is 2, hunders is 3, thounsands is 4
        self.digit = digit

        # child list
        # e.g: "VII" has root node  .roman = "V", .name = "V"
        #  it has a child node:     .roman = "I", .name = "VI"
        #  child of child node:     .roman = "I", .name = "VII"
        # it could be searched via VII
        self.child = dict() # child list
    
    # get value of current node
    def getValue(self):
        return self.value

    # get roman of current node
    def getRoman(self):
        return self.roman

    # get digit of current node
    def getDigit(self):
        return self.digit

    # add a new node, representing a rule, like (VII, 7)
    #  roman: e.g VII, M, CCC
    #  value: corresponding value of it
    #  digit: node digit level (10 base), 1~9=1 10~99=2 ...
    #  idx: use for looping of the same node, unti the end
    # return: true/false
    #  if false, means tree building error:
    #    duplicate, or invalid order, e.g.: add "VII" before add "VI"
    def addNode(self, roman, value, digit, idx = 0):
        if idx == len(roman):
            return False

        created = False
        key = roman[idx]
        #if len(rom) == 1:
        nd = self.child.get(key)
        if nd is None:
            # node must be added step by step
            if idx + 1 != len(roman):
                print("add root node of {} first".format(roman))
                return False

            # new root node, e.g. I=1; V =5
            nd = TreeNode(roman, key, value, digit)
            # add root node
            self.child[key] = nd
            created = True # really create a new node

        # continue, unti end
        return created or nd.addNode(roman, value, digit, idx+1)

    # dump the tree, for debug usage
    def dumpTree(self):
        # root node has value of 0
        if self.value > 0:
            print("{}, {}".format(self.roman, self.value))
        for _, v in self.child.items():
            v.dumpTree()

    # match the longest possible
    #  retrun
    #   (1) value of the match, if no matching, is None
    #   (2) right index of the match
    # eg getLongestMatch("MMI", 0): return the node in "MM" first
    def _getLongestMatchNode(self, roman, idx):
        # get current       
        nd = self.child.get(roman[idx])
        # not find
        if nd is None:
            return None
        
        # check child
        if idx + 1 < len(roman):
            # get child
            child = nd._getLongestMatchNode(roman, idx+1)
            if not child is None:
                # return child node
                return child

        # return current node
        return nd

    # check if a valid roman numeral
    def _checkDigits(self, digits, digit):
        # alreay has in this digit
        if digits[digit] is True:
            return False
        
        # new one, avoid low digit in front of high
        #  e.g.  IM (1001) is invalid
        i = digit - 1
        while i > 0:
            if digits[i] is True:
                # print("digit {} comes before {}".format(i, digit))
                return False
            i -= 1

        # valid
        return True

    # compute a roman numeral
    # return int when success; otherwise, an error string
    def computeRoman(self, roman):
        i = 0
        val = 0
        # represents if each digit is already computed
        #  [0] is not used
        digits = [False]*5
        while i < len(roman):
            v = self._getLongestMatchNode(roman, i)
            if v is None:
                val ="{:15}: is not a valid roman numeral".format(roman)
                break

            if self._checkDigits(digits, v.digit) is True:
                val += v.getValue()
                # move ahead a couple of steps
                i   += len(v.getRoman())
                digits[v.digit] = True
            else:
                err = "{:15}: is not a valid roman numeral, at index:{}"
                val = err.format(roman, i+1)
                break

        return val

# Wrap class for computing from given input file/input array
class RomanCompute:
    def __init__(self):
        self.romans = []
        self.output = []
        self.ruleTree = TreeNode()
        self.buildRomanRuleTree()

    # read the input from file
    # input:
    #  fname: filename, with path
    # output:
    #  (1) True/False
    #  (2) None/Error message when False
    def readInputFromFile(self, fname):
        self.romans = []
        try:
            with open(fname) as f:
                for line in f.readlines():
                    roman = line.rstrip().rstrip()
                    if len(roman) > 0:
                        self.romans.append(roman)
        except:
            msg = "input file: {} is not existing/open error, CHECK"
            return False, msg.format(fname)

        # if file is full of empty line, we also report error
        if len(self.romans) == 0:
            return False, "input file: {} is empty, CHECK".format(fname)
        
        return True, None

    # use already existing romans as compute input
    #  input romans should be an array
    def setInput(self, romans):
        self.romans = romans

    # use the ruleTree to compute each romans
    #  the result is put in output
    def computeRomans(self):
        self.output = []
        for rom in self.romans:
            self.output.append(self.ruleTree.computeRoman(rom))

    # only output the results
    def outputResult(self):
        for x in self.output:
            print(x)

    # output the results with input together in one line
    def outputResultWithInput(self):
        i = 0
        while i < len(self.output):
            if isinstance(self.output[i], int):
                print("{:15}:{:10}".format(self.romans[i], self.output[i]))
            else:
                # output is composed of input and error message
                print(self.output[i])
            i += 1

    # Roman numeral converting rules
    def buildRomanRuleTree(self):
        # single
        s = dict()
        s["I"]    = 1
        s["II"]   = 2
        s["III"]  = 3
        s["IV"]   = 4
        s["V"]    = 5
        s["VI"]   = 6
        s["VII"]  = 7
        s["VIII"] = 8
        s["IX"]   = 9

        # ten
        t = dict()
        t["X"]    = 10
        t["XX"]   = 20
        t["XXX"]  = 30
        t["XL"]   = 40
        t["L"]    = 50
        t["LX"]   = 60
        t["LXX"]  = 70
        t["LXXX"] = 80
        t["XC"]   = 90

        # hundert
        h = dict()           
        h["C"]     = 100
        h["CC"]    = 200
        h["CCC"]   = 300
        h["CD"]    = 400
        h["D"]     = 500
        h["DC"]    = 600
        h["DCC"]   = 700
        h["DCCC"]  = 800
        h["CM"]    = 900

        # thound, with K
        k = dict()
        k["M"]     = 1000
        k["MM"]    = 2000
        k["MMM"]   = 3000

        for key, val in s.items():
            self.ruleTree.addNode(key, val, 1)

        for key, val in t.items():
            self.ruleTree.addNode(key, val, 2)

        for key, val in h.items():
            self.ruleTree.addNode(key, val, 3)

        for key, val in k.items():
            self.ruleTree.addNode(key, val, 4)

        #self.ruleTree.dumpTree()

# use given roman class name to create object and then compute
def doMain(RomanClassName):
    fname = "roman_numeral_test.txt"
    fmt = None
    ln = len(sys.argv)
    if ln > 1:
        fname = sys.argv[1]
        if ln > 2:
            fmt = sys.argv[2]

    # output flag
    fmtFlag = True
    if fmt is None or fmt != "-f":
        fmtFlag = False

    # create a compute class object
    #  e.g. rc = RomanCompute()
    rc = RomanClassName()
    ok, msg = rc.readInputFromFile(fname)
    if not ok:
        print(msg)
        return

    # do computing
    rc.computeRomans()

    # output
    if fmtFlag:
        rc.outputResultWithInput()
    else:
        rc.outputResult()

# for quick local test, any format could be tested here
def doQuickTest(RomanClassName):
    rc = RomanClassName()
    romans = ["VII", "I", "MMMM", "VXXV"]
    rc.setInput(romans)
    rc.computeRomans()
    rc.outputResultWithInput()

# usage:
#  python3 roman.py roman_numeral_test.txt  -f
#  param 1: 
#   file name like: a.txt: used as input file
#   if not given, use roman_numeral_test.txt as default
#  param 2:
#   -f: with it, output is composed of input and output
#       without, output is only numbers/error message
if __name__ == "__main__":
    doMain(RomanCompute)
