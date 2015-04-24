import sys
import re
import pprint
pp = pprint.PrettyPrinter(indent=4)
inf = float("inf")
negInf = float("-inf")

# print to stderr for debugging purposes
# remove all debugging statements before submitting your code
msg = "Given board " + sys.argv[1] + "\n\n"
sys.stderr.write(msg)

#parse the input string, i.e., argv[1]
inp = sys.argv[1].replace("[", "").split("]")
lastPlay = inp.pop(len(inp)-1).replace("LastPlay:", "")
remove = re.compile('(LastPlay:|\(|\))')
lastPlay = remove.sub("", lastPlay).split(",")
if lastPlay[0] == "null":
	lastPlay =  "first move"
else:
	for ind, num in enumerate(lastPlay):
		lastPlay[ind] = int(num)
size = len(inp) - 2
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


def scoreThis(board, lastPlay):
	possible = getPoss(board, lastPlay)
	possTop = possible[3]
	possBottom = possible[4]
	possRight = possible[5]
	possLeft = possible[6]

	numAvail = 0
	for i in range(possBottom, possTop+1):
		for j in range(possLeft, possRight+1):
			if j < len(board[i]):
				if board[i][j] != 0:
					numAvail += 1

	return (numAvail, lastPlay)

def copyBoard(curentBoard):
	newBoard = []
	for i in curentBoard:
		thisCol = []
		for j in i:
			thisCol.append(j)
		newBoard.append(thisCol)
	return newBoard


def alphaBeta(board, lastPlay, depth, isMax, alpha, beta):
	possible = getPoss(board, lastPlay)
	upPos = possible[0]
	rightPos = possible[1]
	leftPos = possible[2]
	possTop = possible[3]
	possBottom = possible[4]
	possRight = possible[5]
	possLeft = possible[6]

	if depth == 0:  #or node = terminal node
		return scoreThis(board, lastPlay)
	else:
		if isMax:
			score = (negInf, [])

			for i in range(possBottom, possTop+1):  #for each child
				for j in range(possLeft, possRight+1):
					if j < len(board[i]):
						if board[i][j] != 0:
							continue #(skip if move not available)
						for color in range(1, 3):  #for each color
							board[i][j] = color
							childScore = alphaBeta(board, [color, i, j, size+2-i-j], depth-1, False, alpha, beta)
							board[i][j] = 0
							if childScore[0] > score[0]:
								score = childScore
							if score[0] > alpha:
								alpha = score[0]
							if beta <= alpha:
								break
						if beta <= alpha:
							break
				if beta <= alpha:
					break
			return score
		else:
			score = (inf, [])

			for i in range(possBottom, possTop+1):  #for each child
				for j in range(possLeft, possRight+1):
					if j < len(board[i]):
						if board[i][j] != 0:
							continue #(skip if move not available)
						for color in range(1, 3):  #for each color
							board[i][j] = color
							childScore = alphaBeta(board, [color, i, j, size+2-i-j], depth-1, True, alpha, beta)
							board[i][j] = 0
							if childScore[0] < score[0]:
								score = childScore
							if score[0] < beta:
								beta = score
							if beta <= alpha:
								break
						if beta <= alpha:
							break
				if beta <= alpha:
					break
			return score


bestMove = alphaBeta(board, lastPlay, 6, True, negInf, inf)
nextMove = map(str, bestMove[1])
makeMove = ",".join(nextMove)
				

#print to stdout for AtroposGame
sys.stdout.write("(" + makeMove + ")");





















