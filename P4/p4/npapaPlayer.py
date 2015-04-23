import sys
import re
import pprint
pp = pprint.PrettyPrinter(indent=4)
# print to stderr for debugging purposes
# remove all debugging statements before submitting your code
msg = "Given board " + sys.argv[1] + "\n"
sys.stderr.write(msg)

#parse the input string, i.e., argv[1]
inp = sys.argv[1].replace("[", "").split("]")
lastPlay = inp.pop(len(inp)-1).replace("LastPlay:", "")
remove = re.compile('(LastPlay:|\(|\))')
lastPlay = remove.sub("", lastPlay).split(",")
for num in lastPlay:
	num = int(num)
size = len(inp)
board = []
for row in reversed(inp):
	thisRow = []
	for num in list(row):
		thisRow.append(int(num))
	board.append(thisRow)


#perform intelligent search to determine the next move
def getPoss(board, lastPlay):
	upPos = lastPlay[1]
	rightPos = lastPlay[2]
	leftPos = size+2 - rightPos - upPos
	possTop = upPos+1 if upPos+1 <= size else upPos
	possBottom = upPos-1 if upPos-1 >= 1 else upPos
	possRight = rightPos+1 if rightPos+1 <= size else rightPos
	possLeft = rightPos-1 if rightPos-1 >= 1 else rightPos

	return (upPos, rightPos, leftPos, possTop, possBottom, possRight, possLeft)


def score(board, lastPlay):
	possible = getPoss(board, lastPlay)
	possTop = possible[3]
	possBottom = possible[4]
	possRight = possible[5]
	possLeft = possible[6]

	numAvail = 0
	for i in possTop..possBottom:
		for j in possRight..possLeft:
			if board[i][j] != "0"
				numAvail += 1

	return 6 - numAvail


def alphaBeta(board, lastPlay, depth, turn, alpha, beta):
	possible = getPoss(board, lastPlay)
	upPos = possible[0]
	rightPos = possible[1]
	leftPos = possible[2]
	possTop = possible[3]
	possBottom = possible[4]
	possRight = possible[5]
	possLeft = possible[6]

	if depth == 0:  #or node = terminal node
		return score(board, lastPlay)
	else:
		if turn is "max":
			score = float("-inf")

			for i in possTop..possBottom:  #for each child
				for j in possRight..possLeft:
					if board[i][j] != 0:
						continue #(skip if move not available)
					child = 
					childScore = score(board, lastPlay)


				

#print to stdout for AtroposGame
sys.stdout.write("(3,2,2,2)");
# As you can see Zook's algorithm is not very intelligent. He 
# will be disqualified.





















