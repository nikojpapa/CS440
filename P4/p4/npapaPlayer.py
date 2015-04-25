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


def copyBoard(curentBoard):
	newBoard = []
	for i in curentBoard:
		thisCol = []
		for j in i:
			thisCol.append(j)
		newBoard.append(thisCol)
	return newBoard


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


def listAdjacents(board, lastPlay, avail):
	upPos = lastPlay[1]
	rightPos = lastPlay[2]
	adj = []
	if upPos > 1:
		adj = [(upPos+1, rightPos-1), (upPos+1, rightPos), (upPos, rightPos+1), (upPos-1, rightPos+1), (upPos-1, rightPos), (upPos, rightPos-1)]
	else:
		adj = [(upPos+1, rightPos-1), (upPos+1, rightPos), (upPos, rightPos+1), (upPos-1, rightPos), (upPos-1, rightPos-1), (upPos, rightPos-1)]

	if avail=="all":
		return adj
	else:
		avails = []
		unavails = []
		for (up, right) in adj:
			if board[up][right] == 0:
				avails.append((up, right))
			else:
				unavails.append((up, right))
		# pp.pprint(avails)
		if avail:
			return avails
		else:
			return unavails


def moveLoses(board, move):
	# pp.pprint(board)
	color = move[0]
	adjacents = listAdjacents(board, move, "all")
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

def leastPopulated(board, lastPlay):
	unavailAdjacents = listAdjacents(board, lastPlay, False)

def scoreThis(board, lastPlay, isMax):

	if moveLoses(board, lastPlay):
		if not isMax:
			return (0, lastPlay)
		else:
			return (8, lastPlay)

	color = lastPlay[0]
	unavailAdjacents = listAdjacents(board, lastPlay, False)
	if isMax:
		scores = [0, 6, 6, 6]
		for (up, right) in unavailAdjacents:
			scores[board[up][right]] -= 1
			unPopScore = scores[color]
			return (unPopScore, lastPlay)
	else:
		scores = [8, 0, 0, 0]
		for (up, right) in unavailAdjacents:
			scores[board[up][right]] += 1
			unPopScore = scores[color]
			return (unPopScore, lastPlay)

	# numAvail = len(listAdjacents(board, lastPlay, True))
	# if numAvail==0:
	# 	if not isMax:
	# 		return (1+unPopScore, lastPlay)
	# 	else:
	# 		return (7, lastPlay)
	# else:
	# 	# pp.pprint(8 - numAvail)
	# 	if not isMax:
	# 		return (8+unPopScore - numAvail, lastPlay)
	# 	else:
	# 		return (0 + numAvail, lastPlay)


def alphaBeta(board, lastPlay, depth, isMax, alpha, beta):

	if depth == 0 or moveLoses(board, lastPlay) or len(listAdjacents(board, lastPlay, True)) == 0:
		# pp.pprint("hi")
		return scoreThis(board, lastPlay, isMax)
	else:
		if isMax:
			# pp.pprint("MAXIMIZER::: " + str(depth))
			score = (negInf, [])
			# pp.pprint("hi")
			# pp.pprint(listAdjacents(board, lastPlay, True))
			for (up, right) in listAdjacents(board, lastPlay, True):
				# pp.pprint("hi")
				for color in range(1, 4):  #for each color							
					board[up][right] = color
					move = [color, up, right, size+2-up-right]
					# pp.pprint("MAX MOVE: " + str(move))
					childScore = alphaBeta(board, move, depth-1, False, alpha, beta)
					# pp.pprint("MAX: " + str(childScore[0]) + ", " + str(move))
					# pp.pprint("CHILDSCORE: " + str(childScore))
					board[up][right] = 0
					if childScore[0] > score[0]:
						# pp.pprint(str(depth) + " :: " + str(childScore[0]) + " > " + str(score[0]))
						score = (childScore[0], move)
					if score[0] > alpha:
						alpha = score[0]
					if beta <= alpha:
						break
			return score
		else:
			# pp.pprint("MINIMIZER::: " + str(depth))

			score = (inf, [])

			for (up, right) in listAdjacents(board, lastPlay, True):
				for color in range(1, 4):  #for each color							
					board[up][right] = color
					move = [color, up, right, size+2-up-right]
					# pp.pprint("MIN MOVE: " + str(move))
					childScore = alphaBeta(board, move, depth-1, True, alpha, beta)
					# pp.pprint("MIN: " + str(childScore[0]) + ", " + str(move))
					# pp.pprint(childScore)
					board[up][right] = 0
					if childScore[0] < score[0]:
						# pp.pprint(str(depth) + " :: " + str(childScore[0]) + " < " + str(score[0]))
						score = (childScore[0], move)
					if score[0] < beta:
						beta = score[0]
					if beta <= alpha:
						break
			return score


bestMove = alphaBeta(board, lastPlay, 7, True, negInf, inf)
nextMove = map(str, bestMove[1])
makeMove = ",".join(nextMove)
				

#print to stdout for AtroposGame
sys.stdout.write("(" + makeMove + ")");





















