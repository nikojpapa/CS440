require 'pp'

hmmText = IO.binread(ARGV[0])
hmmLines = hmmText.split("\n")
obsText = IO.binread(ARGV[1])
obsLines = obsText.split("\n")

@states = []
@vocab = []
@a = {}
@b = {}
@pi = {}
@o = []

def getMatrices(hmm, obs)
	@states = hmm[1].split(" ")
	@vocab = hmm[2].split(" ")

	currentMatrix = nil
	hmm.each do |line|
		if line == "a:"
			currentMatrix = "a"
			next
		elsif line == "b:"
			currentMatrix = "b"
			next
		elsif line == "pi:"
			currentMatrix = "pi"
			next
		end

		currentLine = line.split(" ")
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

	for lineNum in 1..Integer(obs[0])
		@o << obs[lineNum * 2].split(" ")
	end
end

def alpha(t, state, obsSeq)
	# puts "Obs: #{obsSeq}"
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

def beta(t, state, obsSeq)
	if t == obsSeq.length
		return 1
	else
		sum = 0
		@states.each_with_index do |j, ind|
			recursion = beta(t + 1, j, obsSeq)
			sum += @a[state][j] * @b[j][obsSeq[t]]
		end

		return sum
	end
end

def gamma(t, state, obsSeq)
	numerator = alpha(t, state, obsSeq) * beta(t, state, obsSeq)
	denominator = 0
	@states.each do |i|
		denominator += alpha(t, i, obsSeq) * beta(t, i, obsSeq)
	end

	return numerator / denominator
end

def epsilon(t, fromState, toState, obsSeq)
	numerator = alpha(t, fromState, obsSeq) * @a[fromState][toState] * @b[toState][obsSeq[t]] * beta(t+1, toState, obsSeq)
	denominator = 0
	@states.each do |i|
		@states.each do |j|
			denominator += alpha(t, i, obsSeq) * @a[i][j] * @b[j][obsSeq[t]] * beta(t+1, j, obsSeq)
		end
	end

	return numerator / denominator
end	

getMatrices(hmmLines, obsLines)

@o.each_with_index do |obsSeq|
	newPi = []
	newA = []
	newB = []
	@states.each do |i|
		newPi << gamma(1, i, obsSeq)

		newAi = []
		@states.each do |j|
			numerator = 0
			denominator = 0
			for t in (obsSeq.length - 1)
				numerator += epsilon(t, i, j, obsSeq)
				denominator += gamma(t, i, obsSeq)
			end
			newAi << numerator / denominator
		end
		newA << newAi

		newBi = []
		@vocab.each do |k|
			numerator = 0
			denominator = 0
			for t in obsSeq.length
				if obsSeq[t] == k
					numerator += gamma(t, i, obsSeq)
				end
				denominator += gamma(t, i, obsSeq)
			end
			newBi << numerator / denominator
		end
		newB << newBi
	end

	# bigT = obsSeq.length

	# # puts "#{gamma(1, @states[2], obsSeq)}"
	# sum = 0
	# @states.each do |state|
	# 	sum += epsilon(2, @states[3], state, obsSeq)
	# end

	# # puts sum

	# puts "#{gamma(2, @states[3], obsSeq)} = #{sum}"
end































