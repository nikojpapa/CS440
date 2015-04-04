require 'pp'

hmmText = IO.binread(ARGV[0])
hmmLines = hmmText.split("\n")
obsText = IO.binread(ARGV[1])
obsLines = obsText.split("\n")

@states = []
@vocab = []
@a = {}  #transition matrix
@b = {}  #emission matrix
@pi = {} #initial prob matrix
@o = []  #obs matrix

def getMatrices(hmm, obs)
	@states = hmm[1].split(" ")
	@vocab = hmm[2].split(" ")

	currentMatrix = nil
	hmm.each do |line|
		if line == "a:"          #which matrix we are looking at
			currentMatrix = "a"
			next
		elsif line == "b:"
			currentMatrix = "b"
			next
		elsif line == "pi:"
			currentMatrix = "pi"
			next
		end

		currentLine = line.split(" ")   #loads line into corresponding matrix
		if currentMatrix == "a"
			fromState = @states[@a.length]

			toState = {}
			currentLine.each_with_index do |prob, state|
				toState[@states[state]] = prob.to_f
			end
			@a[fromState] = toState

		elsif currentMatrix == "b"
			fromState = @states[@b.length]

			toWord = {}
			currentLine.each_with_index do |prob, word|
				toWord[@vocab[word]] = prob.to_f
			end
			@b[fromState] = toWord

		elsif currentMatrix == "pi"
			currentLine.each_with_index do |prob, state|
				@pi[@states[state]] = prob.to_f
			end
		end
	end

	for lineNum in 1..Integer(obs[0])   #loads output into obs matrix
		@o << obs[lineNum * 2].split(" ")
	end
end

def delta(t, state, obsSeq)    #highest probability along a single path
	if t == 1
		return [@pi[state] * @b[state][obsSeq[0]], state]  #returns probability along with its state
	else
		max = 0
		maxState = []
		@states.each_with_index do |i, ind|
			recursion = delta(t - 1, i, obsSeq)
			possibleMax = recursion[0] * @a[i][state] * @b[state][obsSeq[t-1]]

			if possibleMax > max
				max = possibleMax
				maxState << recursion[1]
			end
		end

		return [max, maxState << state]
	end
end

getMatrices(hmmLines, obsLines)

@o.each_with_index do |obsSeq|
	bigT = obsSeq.length       #gets max delta for the entire obs sequence

	max = 0
	maxState = []
	@states.each do |state|
		possibleMax = delta(bigT, state, obsSeq)

		if possibleMax[0] > max
			max = possibleMax[0]
			maxState = possibleMax[1]
		end
	end

	puts "#{max} #{maxState.join(" ")}"
end































