#execute in PYTHON shell
#  exec(open('pythonplay.py').read())


class OpNode_Final:
  def __init__(self, val):
    self.value = val
    self.left = None
    self.right = None
    self.level = -10
    self.adjustLevel()

  def adjustLevel(self):
    if (self.value == "+" or self.value == "-"):
      self.level = 10
    elif (self.value == "*" or self.value == "/"):
      self.level = 20
    elif (self.value == "("):
      self.level = 30
    elif (self.value == ")"):
      self.level = 40
    elif (isinstance(self.value, int)):
      self.level = 0
    else:
      print " Undefined object, please check"

  def compute(self):
    #compute the expression
    if isinstance(self.value, str):
      if (self.value == "+"):
        res = self.left.compute() + self.right.compute()
      elif (self.value == "-"):
        res =  (self.left.compute() - self.right.compute())
      elif (self.value == "*"):
        res =  (self.left.compute() * self.right.compute())
      elif (self.value == "/"):
        res =  (self.left.compute() / self.right.compute())
    else:
      res =   self.value

    #print "compute", res
    return res

  def setLeft(self, lft):
    self.left = lft

  def setRight(self, rg):
    self.right = rg

  def show(self):
    if (self.left != None):
      self.left.show()

    print " ", self.value
   
    if (self.right != None):
      self.right.show()

  def showWidthFirst(self):
    print " ", self.value

    if (self.left != None):
      self.left.showWidthFirst()   

    if (self.right != None):
      self.right.showWidthFirst()  

  def retrieveDataWidthFirst(self, dst, level, nodeId = [0]):
    if level == 0:
      print " retrieveData  width first"

    if len(dst) < level + 1:
      dst.append([])
      dst[level].append("L:"+str(level))

    dst[level].append(("N:"+str(nodeId[0]), self.value))
    nodeId[0] += 1

    if (self.left != None):
      self.left.retrieveDataWidthFirst(dst, level+1, nodeId)

    if (self.right != None):
      self.right.retrieveDataWidthFirst(dst, level+1, nodeId)


def doPopRightmost(stk):
  idx = findLastLeftParenthesisPos(stk)
  if idx >= 0:
    # print " last ( is in", idx
    cnt = len(stk) - idx -1
  else:
    idx = 0;
    cnt = len(stk)
  #print " right-most, len", len(stk), " ( pos:", idx, "proc cnt:",cnt

  if cnt == 1:
    return True;
  elif cnt == 3:
    # process "a+b" style
    # watch and wait
    #print " no more process, wait"
    return True   
  elif len(stk) == 5:
    # a+b*c, process
    #print "process 1,", stk[-2].level , stk[-4].level
    if (stk[-2].level > stk[-4].level):
      #print " process: a+b*c"
      p2 = stk.pop()
      op = stk.pop()
      p1 = stk.pop()
      op.setLeft(p1)
      op.setRight(p2)
      stk.append(op)
    return True
  else:
    #print "bad right-most process, check len", len(stk)
    return False


def findLastLeftParenthesisPos(stk):
  idx = len(stk)
  if idx == 0:
    return -1

  idx -= 1
  while (idx >= 0):
    if (stk[idx].value == "("):
      return idx;
    idx -= 1

  return -1

def doPop_Parenthesis(stk):

  idx = findLastLeftParenthesisPos(stk)
  if idx >= 0:
    #print " last ( is in", idx
    pass
  else:
    idx = 0;
    cnt = len(stk)
    #print " left ( is not found, ERROR"
    return

  p = 0
  #pop 3 or 5
  if len(stk) <3:
    #print "bad stack, check len", len(stk)
    return

  if (stk[-3].value == "("):
    # process "(a)" style
    #print " pop style (a)"
    stk.pop()
    op = stk.pop()
    stk.pop()
    stk.append(op)
    p = 1
  elif (stk[-7].value == "("):
    # "(a+b*c)"
    stk.pop()   
    p3 = stk.pop()
    op2 = stk.pop()
    p2 = stk.pop()
    op1 = stk.pop()
    p1 = stk.pop()
    stk.pop()

    if (op2.level > op1.level):
      #print " pop style (a+b*c)"
      # "a+b*c"
      op2.setLeft(p2)
      op2.setRight(p3)
      op1.setLeft(p1)
      op1.setRight(op2)
      stk.append(op1)
    else:
      # "a*b+c" or "a+b-c" or...
      #print " pop style a*b+c or a+b-c"
      op1.setLeft(p1)
      op1.setRight(p2)
      op2.setLeft(op1)
      op2.setRight(p3)
      stk.append(op2)

    p = 1
  elif (stk[-5].value == "("):
    # "(a+b)"
    #print " pop style (a+b)"

    stk.pop()
    p2 = stk.pop()
    op = stk.pop()
    p1 = stk.pop()
    op.setLeft(p1)
    op.setRight(p2)
    stk.pop()

    #push back result 
    stk.append(op)

    p = 1
  else:
    print " ERROR: bad parenthesis"

  if p == 1:
    # processed ")", check again and process
    doPopRightmost(stk)

  if p == 0:
    print " bad stack, check len", len(stk)
    return


def checkStack(stk, t):
  if (len(stk) == 0):
    return

  idx = findLastLeftParenthesisPos(stk)
  if idx >= 0:
    #print " last ( is in", idx
    cnt = len(stk) - idx -1
  else:
    idx = 0;
    cnt = len(stk)
    
  
  if cnt == 3:
    # a+b, a*b...
    if t.level == 10:
      # if it is +/-, just do a pop of left
      #print " pop a lower oper"
      p2 = stk.pop()
      op = stk.pop()
      p1 = stk.pop()
      op.setLeft(p1)
      op.setRight(p2)
      stk.append(op)
    elif t.level == 20:
      # 3*4*  (same level)
      if stk[-2].level == 20:
        #print " pop same level"
        p2 = stk.pop()
        op = stk.pop()
        p1 = stk.pop()
        op.setLeft(p1)
        op.setRight(p2)
        stk.append(op)
      else:
        #print " wait next"
        pass
    
  elif cnt == 5:
    # a+b*c is possible
    # a*b+c is not possible
    # no matter, must pop the right most
    #print " pop the right most"
    p2 = stk.pop()
    op = stk.pop()
    p1 = stk.pop()
    op.setLeft(p1)
    op.setRight(p2)
    stk.append(op)

def popLast(stk):
  #print "pop last", len(stk)
  while (len(stk) >= 3):
    if len(stk) == 3:
      p2 = stk.pop()
      op = stk.pop()
      p1 = stk.pop()
      op.setLeft(p1)
      op.setRight(p2)
      stk.append(op)    
    elif  len(stk) == 5:
      # a+b*c is possible
      # a*b+c is not possible
      # no matter, must pop the right most
      p2 = stk.pop()
      op = stk.pop()
      p1 = stk.pop()
      op.setLeft(p1)
      op.setRight(p2)
      stk.append(op)  
      #print " pop the right most, after, len", len(stk)

def parseFullExpressLast(expr):
  stk = []
  x = 0
  print expr
  pos = 0

  for x in expr:
    #print "len", len(stk), " :", x
    # put into stack
    t = OpNode_Final(x)

    if t.level == 40:
      # ")"    
      stk.append(t)
      #print "push :", x
      doPop_Parenthesis(stk)
    elif t.level == 30:
      # "("
      stk.append(t)
      #print "push :", x
    elif t.level == 0:
      stk.append(t)
      #print "push int:", x
    elif t.level == 10 or t.level == 20:
      # put into stack
      
      # check whether poper
      checkStack(stk, t)
      
      stk.append(t)
      #print "push:", x
    else:
      print "bad input, check", x

    #let pos move one
    pos +=1

  #check last
  popLast(stk)
  return stk.pop()



#use a string to generate a list of operation
def generateList(ss):
  pos = 0
  x = 0
  out = []
  print ss
  ss=ss.replace(" ","")
  print ss
  while (x < len(ss)):
    if not (ss[x] >='0' and ss[x] <='9'):
      if (pos < x):
        out.append(int(ss[pos: x])) #convert them to int
        pos = x+1;
      out.append(ss[x])
      pos = x+1
    x += 1
  
  # the last
  if (pos < x):
    out.append(int(ss[pos: x]))

  return out

res = parseFullExpressLast(generateList("3 +(5*(4/2)*3-2)+(1+2)*(6-4)+( 5)"))
if (res is None):
  print "bad result"
else:
  print " >>>> depth first"
  res.show()

  print " >>>> width first" 
  val = []
  res.retrieveDataWidthFirst(val, 0)
  for x in val:
    print x
  
  
  print "the last result is", res.compute()
