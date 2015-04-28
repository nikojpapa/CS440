lookAheadDepth = 5

import sys
import re
import pprint
pp = pprint.PrettyPrinter(indent=4)
inf = float("inf")
negInf = float("-inf")

#parse the input string, i.e., argv[1]
inp = sys.argv[1].replace("[", "").split("]")
lastPlay = inp.pop(len(inp)-1).replace("LastPlay:", "")
size = len(inp) - 2  #board size
remove = re.compile('(LastPlay:|\(|\))')
lastPlay = remove.sub("", lastPlay).split(",")
if lastPlay[0] == "null":
	None
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

def numSpotsOnBoard(boardSize):
	if boardSize % 2 == 1:
		return size * (float(size / 2) + 0.5)
	else:
		return size * (float(size / 2))

def listAdjacents(board, lastPlay, avail):  #gets spots adjacent to last play in a clockwise list
	upPos = lastPlay[1]
	rightPos = lastPlay[2]

	adj = []
	if upPos > 1:
		adj = [(upPos+1, rightPos-1), (upPos+1, rightPos), (upPos, rightPos+1), (upPos-1, rightPos+1), (upPos-1, rightPos), (upPos, rightPos-1)]
	else:
		adj = [(upPos+1, rightPos-1), (upPos+1, rightPos), (upPos, rightPos+1), (upPos-1, rightPos), (upPos-1, rightPos-1), (upPos, rightPos-1)]

	if avail=="all":
		return adj  #returns all adjacent spots, available or not
	else:
		avails = []
		unavails = []
		for (up, right) in adj:
			if board[up][right] == 0:
				avails.append((up, right))  #spot is available
			else:
				unavails.append((up, right))
		if avail:
			return avails  #return available, adjacent spots
		else:
			return unavails  #return unavailable, adjacent spots


def moveLoses(board, move):  #returns true if the move will produce a three colored triangle
	if move[0] == "null":
		return False

	color = move[0]
	adjacents = listAdjacents(board, move, "all")

	for ind, (up, right) in enumerate(adjacents):  #go through each pair of neighboring, adjacent spots
		colors = []
		colors.append(color)  #mark color of move
		if board[up][right] != 0:
			colors.append(board[up][right])  #mark color of one spot

		(up2, right2) = adjacents[(ind+1)%len(adjacents)]
		if board[up2][right2] != 0:
			colors.append(board[up2][right2])  #mark color of other spot

		if len(set(colors)) == 3:
			return True  #if all three colors are present, move loses

	return False

def getAllAvails(board):  #get all available spots on the board
	avails = []
	for rowNum, row in enumerate(board):
		for colNum, spot in enumerate(row):
			if spot == 0:
				avails.append((rowNum, colNum))
	return avails

def boundedAvails(board, spot, alreadySaw):  #get all available spots within the boundary of colored spots that spot is in
	avails = listAdjacents(board, spot, True)
	unseenAvails = set(avails) - alreadySaw
	myName = set([(spot[1], spot[2])])
	nameList = alreadySaw | unseenAvails | myName  #add spot to list and every available spot next to spot to if they haven't already been added

	for (up, right) in unseenAvails:  #call this function on all recently added spots
		newNames = boundedAvails(board, [0, up, right, size+2-up-right], nameList)
		nameList = nameList | newNames  #add reported names to list

	return nameList

def scoreThis(board, lastPlay, isMax):  #static evaluation function
	totalScore = 0

	if moveLoses(board, lastPlay):  #if the move loses, return worst score
		if not isMax:
			return (negInf, lastPlay)
		else:
			return (inf, lastPlay)

	#adds good score if move creates traps for opponent
	trapScore = 0
	avails = listAdjacents(board, lastPlay, True)
	madeBounds = set()
	oddBounds = 0
	evenBounds = 0
	for (up, right) in avails:
		if (up, right) not in madeBounds:  #for each unique group next to lastPlay
			bounded = boundedAvails(board, [0,up,right,size+2-up-right], set())
			madeBounds = madeBounds | bounded
			if len(bounded) % 2 == 0:
				evenBounds += 1
			else:
				oddBounds += 1
	if isMax:  #scale trapScore so colorScore does not effect position
		trapScore += (oddBounds - evenBounds)
	else:
		trapScore += (oddBounds - evenBounds)

	#adds good score if opponent will likely end up with only one option
	board[lastPlay[1]][lastPlay[2]] = 0
	thisBound = boundedAvails(board, lastPlay, set())
	board[lastPlay[1]][lastPlay[2]] = lastPlay[0]
	if len(thisBound) % 2 == 0:  #if the group of available spots + this move is an even number, opponent will make last move in the group if all spots are eventually filled
		skewScore = (numSpotsOnBoard(size)-len(thisBound)) / (oddBounds+evenBounds) if oddBounds+evenBounds != 0 else 1
		if isMax:
			trapScore += skewScore
		else:
			trapScore -= skewScore

	#determines color by agreeing with the color that is most shown around it
	colorScore = 0
	color = lastPlay[0]
	unavailAdjacents = listAdjacents(board, lastPlay, False)
	scores = [0, 0, 0, 0]
	for (up, right) in unavailAdjacents:
		if isMax:
			scores[board[up][right]] += (trapScore / 7)
		else:
			scores[board[up][right]] -= (trapScore / 7)
	colorScore = trapScore - scores[color]

	totalScore = trapScore + colorScore
	return (totalScore, lastPlay)

def alphaBeta(board, lastPlay, depth, isMax, alpha, beta):  #minimax with alpha-beta pruning
	if lastPlay[0] == "null":
		return (0, [3, size, 1, 1])  #if first move, make it at the top

	if depth == 0 or moveLoses(board, lastPlay):
		return scoreThis(board, lastPlay, isMax)
	else:
		children = listAdjacents(board, lastPlay, True)
		if not children:
			children = getAllAvails(board)
		if isMax:
			score = (negInf, [])
			for (up, right) in children:
				for color in range(1, 4):  #for each child							
					board[up][right] = color
					move = [color, up, right, size+2-up-right]
					childScore = alphaBeta(board, move, depth-1, False, alpha, beta)
					board[up][right] = 0
					if childScore[0] >= score[0]:
						score = (childScore[0], move)
					if score[0] > alpha:
						alpha = score[0]
					if beta <= alpha:
						break
			return score
		else:
			score = (inf, [])

			for (up, right) in children:
				for color in range(1, 4):  #for each child							
					board[up][right] = color
					move = [color, up, right, size+2-up-right]
					childScore = alphaBeta(board, move, depth-1, True, alpha, beta)
					board[up][right] = 0
					if childScore[0] <= score[0]:
						score = (childScore[0], move)
					if score[0] < beta:
						beta = score[0]
					if beta <= alpha:
						break
			return score

#find the "best" move and parse it into a readable format for AtroposGame
bestMove = alphaBeta(board, lastPlay, lookAheadDepth, True, negInf, inf)
nextMove = map(str, bestMove[1])
makeMove = ",".join(nextMove) 
				

#print to stdout for AtroposGame
sys.stdout.write("(" + makeMove + ")");





















