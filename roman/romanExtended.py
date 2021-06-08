__version__ = "0.1"
__autoor__  = "Jian Wang, w13915984028@gmail.com"

from roman import TreeNode
from roman import RomanCompute
from roman import doMain

# With extended rule for roman numeral
#  those rules are not fully agreed, but used in fact
class RomanComputeExtended(RomanCompute):
    def __init__(self):
        RomanCompute.__init__(self)
        self.ruleTree.addNode("IIII",   4, 1)
        self.ruleTree.addNode("XXXX",  40, 2)
        self.ruleTree.addNode("CCCC", 400, 3)

if __name__ == "__main__":
    doMain(RomanComputeExtended)