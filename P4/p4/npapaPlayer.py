import sys
import re
import pprint
pp = pprint.PrettyPrinter(indent=4)
inf = float("inf")
negInf = float("-inf")

#parse the input string, i.e., argv[1]
inp = sys.argv[1].replace("[", "").split("]")
lastPlay = inp.pop(len(inp)-1).replace("LastPlay:", "")
size = len(inp) - 2
remove = re.compile('(LastPlay:|\(|\))')
lastPlay = remove.sub("", lastPlay).split(",")
if lastPlay[0] == "null":
	lastPlay =  [1,1,1,size+2]
else:
	for ind, num in enumerate(lastPlay):
		lastPlay[ind] = int(num)
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
	leftPos = lastPlay[3]
	possTop = upPos+1 if upPos+1 <= size else upPos
	possBottom = upPos-1 if upPos-1 >= 1 else upPos
	possRight = rightPos+1 if rightPos+1 <= size else rightPos
	possLeft = rightPos-1 if rightPos-1 >= 1 else rightPos

	return (upPos, rightPos, leftPos, possTop, possBottom, possRight, possLeft)

def listAdjacents(board, lastPlay, avail):
	upPos = lastPlay[1]
	rightPos = lastPlay[2]
	adj = []
	if upPos > 1:
		adj = [(upPos+1, rightPos-1), (upPos+1, rightPos), (upPos, rightPos+1), (upPos-1, rightPos+1), (upPos-1, rightPos), (upPos, rightPos-1)]
	else:
		adj = [(upPos+1, rightPos-1), (upPos+1, rightPos), (upPos, rightPos+1), (upPos-1, rightPos), (upPos-1, rightPos-1), (upPos, rightPos-1)]

	if avail:
		avails = []
		for (up, right) in adj:
			if board[up][right] == 0:
				avails.append((up, right))
		# pp.pprint(avails)
		return avails
	else:
		return adj

def isAdjacent(lastPlay, newPlay):

	lastUp = lastPlay[1]
	lastRight = lastPlay[2]
	lastLeft = lastPlay[3]
	newColor = newPlay[0]
	newUp = newPlay[1]
	newRight = newPlay[2]
	newLeft = newPlay[3]
	# pp.pprint(lastPlay)
	# pp.pprint(newPlay)

	heightDist = newUp - lastUp
	rightDist = newRight - lastRight
	# pp.pprint(str(heightDist) + ", " + str(rightDist))

	if abs(heightDist) > 1:
		return False
	elif heightDist==1 and (rightDist < -1 or rightDist > 0):
		return False
	elif heightDist==0 and (rightDist < -1 or rightDist == 0 or rightDist > 1):
		return False
	elif heightDist==-1 and (rightDist < 0 or rightDist > 1):
		return False
	else:
		return True


def moveLoses(board, move):
	# pp.pprint(board)
	color = move[0]
	adjacents = listAdjacents(board, move, False)
	# pp.pprint(adjacents)

	for ind, (up, right) in enumerate(adjacents):
		colors = []
		colors.append(color)
		if board[up][right] != 0:
			colors.append(board[up][right])

		(up2, right2) = adjacents[(ind+1)%len(adjacents)]
		if board[up2][right2] != 0:
			colors.append(board[up2][right2])

		# pp.pprint(colors)
		if len(set(colors)) == 3:
			# pp.pprint(str((up, right)) + " = " + str(board[up][right]) + ", " + str((up2, right2)) + " = " + str(board[up2][right2]))
			return True
	return False

def scoreThis(board, lastPlay):

	if moveLoses(board, lastPlay):
		return (0, lastPlay)

	numAvail = len(listAdjacents(board, lastPlay, True))

	if numAvail==0:
		return (1, lastPlay)
	else:
		return (8 - numAvail, lastPlay)

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

	if depth == 0 or moveLoses(board, lastPlay):
		# pp.pprint("hi")
		return scoreThis(board, lastPlay)
	else:
		if isMax:
			score = (negInf, [])
			# pp.pprint("hi")
			# pp.pprint(listAdjacents(board, lastPlay, True))
			for (up, right) in listAdjacents(board, lastPlay, True):
				# pp.pprint("hi")
				for color in range(1, 3):  #for each color							
					board[up][right] = color
					move = [color, up, right, size+2-up-right]
					childScore = alphaBeta(board, move, depth-1, False, alpha, beta)
					# pp.pprint(childScore)
					board[up][right] = 0
					if childScore[0] > score[0]:
						score = (childScore[0], move)
					if score[0] > alpha:
						alpha = score[0]
					if beta <= alpha:
						break
			return score
		else:
			# pp.pprint("hey")

			score = (inf, [])

			for (up, right) in listAdjacents(board, lastPlay, True):
				for color in range(1, 3):  #for each color							
					board[up][right] = color
					move = [color, up, right, size+2-up-right]
					childScore = alphaBeta(board, move, depth-1, True, alpha, beta)
					board[up][right] = 0
					if childScore[0] < score[0]:
						score = (childScore[0], move)
					if score[0] < beta:
						beta = score[0]
					if beta <= alpha:
						break
			return score


bestMove = alphaBeta(board, lastPlay, 2, True, negInf, inf)
nextMove = map(str, bestMove[1])
makeMove = ",".join(nextMove)
				

#print to stdout for AtroposGame
sys.stdout.write("(" + makeMove + ")");





















