require 'pp'

hmmText = IO.binread(ARGV[0]) #getting lines for first .hmm and the .obs
hmmLines = hmmText.split("\n")
obsText = IO.binread(ARGV[1])
obsLines = obsText.split("\n")

def getMatrices(hmm, obs)  #parses .hmm and .obs file and loads the information into hashes
	@a = {}  #transition matrix
	@b = {}  #emission matrix
	@pi = {} #initial prob matrix
	@o = []  #obs matrix

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

def alpha(t, state, obsSeq)   #gets the probability of the partial observation sequence to given state
	if t == 1
		return @pi[state] * @b[state][obsSeq[0]]
	else
		sum = 0
		@states.each_with_index do |i, ind|
			recursion = alpha(t - 1, i, obsSeq)
			sum += recursion * @a[i][state]
		end

		return sum * @b[state][obsSeq[t-1]]
	end
end

def beta(t, state, obsSeq)   #gets the probability of the partial observation sequence from given state
	if t == obsSeq.length
		return 1
	else
		sum = 0
		@states.each_with_index do |j, ind|
			recursion = beta(t + 1, j, obsSeq)
			sum += @a[state][j] * @b[j][obsSeq[t]] * recursion
		end

		return sum
	end
end

def gamma(t, state, obsSeq)  #the probability of being in state
	numerator = alpha(t, state, obsSeq) * beta(t, state, obsSeq)
	denominator = 0
	@states.each do |i|
		denominator += alpha(t, i, obsSeq) * beta(t, i, obsSeq)
	end

	return numerator / denominator
end

def epsilon(t, fromState, toState, obsSeq)  #the probability of being in fromState going to toState
	numerator = alpha(t, fromState, obsSeq) * @a[fromState][toState] * @b[toState][obsSeq[t]] * beta(t+1, toState, obsSeq)
	denominator = 0
	@states.each do |i|
		@states.each do |j|
			denominator += alpha(t, i, obsSeq) * @a[i][j] * @b[j][obsSeq[t]] * beta(t+1, j, obsSeq)
		end
	end
	return numerator / denominator
end	

def terminateAlpha(states, obsSeq)  #gets alpha for the entire obs sequence
	bigT = obsSeq.length

	sum = 0
	@states.each do |state|
		sum += alpha(bigT, state, obsSeq)
	end

	return sum
end

getMatrices(hmmLines, obsLines)

@o.each_with_index do |obsSeq, ind|
	newPi = []
	newA = []
	newB = []
	@states.each do |i|
		newPi << gamma(1, i, obsSeq)   #update pi matrix

		newAi = []                    #update transition matrix
		@states.each do |j|
			numerator = 0
			denominator = 0
			for t in 1..(obsSeq.length - 1)
				numerator += epsilon(t, i, j, obsSeq)
				denominator += gamma(t, i, obsSeq)
			end
			
			if denominator != 0
				newAi << numerator / denominator
			else
				newAi << @a[i][j]
			end
		end
		newA << newAi

		newBi = []                 #update emission matrix
		@vocab.each do |k|
			numerator = 0
			denominator = 0
			for t in 1..obsSeq.length
				numerator += gamma(t, i, obsSeq) if obsSeq[t-1] == k
				denominator += gamma(t, i, obsSeq)
			end

			if denominator != 0
				newBi << numerator / denominator
			else
				newBi << @b[i][k]
			end
		end
		newB << newBi
	end

	outname = "#{ind}-#{ARGV[2]}"               #produce output .hmm
	firstLine = "#{newA.length} #{newB[0].length} #{obsSeq.length}"
	File.open(outname, "w") { |out|

		out << "#{firstLine}\n" << "#{hmmLines[1]}\n" << "#{hmmLines[2]}\n" << "a:\n"
		newA.each do |line|
			out << "#{line.join(" ")}\n"
		end

		out << "b:\n"
		newB.each do |line|
			out << "#{line.join(" ")}\n"
		end

		out << "pi:\n" << "#{newPi.join(" ")}\n"
	}

	before = terminateAlpha(@states, obsSeq)     #output before and after probabilities
	hmm2Text = IO.binread(outname)
	hmm2Lines = hmm2Text.split("\n")
	getMatrices(hmm2Lines, obsLines)
	after = terminateAlpha(@states, obsSeq)

	puts "#{before} #{after}"
end































