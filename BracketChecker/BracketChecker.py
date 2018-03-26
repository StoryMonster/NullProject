import sys

def Error(str):
    print '\033[40;31m',str,'\033[0m'

def Success(str):
    print '\033[40;36m',str,'\033[0m'

class LineNumberStack(object):
    def __init__(self):
        self.container = []

    def push(self, element):
        self.container.append(element)

    def pop(self):
        return self.container.pop()
    
    def size(self):
        return len(self.container)

if __name__ == '__main__':
    assert len(sys.argv) > 1 and len(sys.argv) < 5, Error('wrong command line parameters')
    fileName = sys.argv[1]
    startLine = 1
    endLine = 0xFFFF
    if len(sys.argv) == 4:
        startLine = int(sys.argv[2])
        endLine = int(sys.argv[3])
    elif len(sys.argv) == 3:
        startLine = int(sys.argv[2])
    else: pass

    lines = []
    with open(fileName, 'r') as fd:
        lines = fd.readlines()
	fileLineCount = len(lines)
	if endLine > fileLineCount:
	    endLine = fileLineCount
    
    assert startLine < endLine, Error('end line is smaller than start line')
    sBracket = LineNumberStack()
    mBracket = LineNumberStack()
    lBracket = LineNumberStack()
    for row in range(startLine, endLine+1):
        line = lines[row-1]
        for col in range(0, len(line)):
            if '(' == line[col]:
	        sBracket.push((row, col + 1))
	    elif ')' == line[col]:
	        if sBracket.size() > 0:
	            left = sBracket.pop()
	            Success("(small bracket)    (%d, %d) match (%d, %d)" % (left[0], left[1], row, col + 1 ))
	        else:
	            Error( "(small bracket)    (*, *) dismatch (%d, %d)" % (row, col + 1 ))
	    elif '[' == line[col]:
	        mBracket.push((row, col + 1))
	    elif ']' == line[col]:
	        if mBracket.size() > 0:
	            left = mBracket.pop()
	            Success("[middle bracket]   (%d, %d) match (%d, %d)" % (left[0], left[1], row, col + 1 ))
	        else:
	            Error( "[middle bracket]   (*, *) dismatch (%d, %d)" % (row, col + 1 ))
	    elif '{' == line[col]:
	        lBracket.push((row, col + 1))
	    elif '}' == line[col]:
	        if lBracket.size() > 0:
	            left = lBracket.pop()
	            Success("{big bracket}      (%d, %d) match (%d, %d)" % (left[0], left[1], row, col + 1 ))
	        else:
	            Error( "{big bracket}      (*, *) dismatch (%d, %d)" % (row, col + 1 ))
	    else: pass

    while sBracket.size() > 0:
        left = sBracket.pop()
        Error("(small bracket)    (%d, %d) dismatch (*, *)" % (left[0], left[1]))

    while mBracket.size() > 0:
        left = mBracket.pop()
        Error("[middle bracket]    (%d, %d) dismatch (*, *)" % (left[0], left[1]))

    while lBracket.size() > 0:
        left = lBracket.pop()
        Error("{big bracket}       (%d, %d) dismatch (*, *)" % (left[0], left[1]))

