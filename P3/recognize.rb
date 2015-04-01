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
	# puts "#{t}"
	if t == 1
		puts "#{@pi[state] * @b[state][obsSeq[0]]}"
		puts "STATE: #{state}"
		puts "pi: #{@pi[state]}"
		return @pi[state] * @b[state][obsSeq[0]]
	else
		sum = 0
		@states.each_with_index do |i, ind|
			sum += alpha(t - 1, i, obsSeq) * @a[@states[ind]][state]
		end

		return sum * @b[state][@vocab[t]]
	end
end


getMatrices(hmmLines, obsLines)
pp @a
pp @b
pp @pi

@o.each_with_index do |obsSeq|
	bigT = obsSeq.length

	sum = 0
	@states.each do |state|
		puts "CALLING: alpha(#{bigT}, #{state}, #{obsSeq}"
		# puts "#{sum}"
		sum += alpha(1, state, obsSeq)
	end

	puts sum
end


























