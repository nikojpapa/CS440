numTests = 10
sampleSize = 10
allNums = []

for j in 1..numTests
	sumWins = 0.0
	for i in 1..sampleSize
		output = `java AtroposGame 7 "python npapaPlayer.py"`
		# puts output
		if output.include?("Script has won")
			sumWins += 1
		end
	end

	winP = sumWins / sampleSize * 100
	puts "Win Percentage: #{winP}%"
	allNums << winP
end

puts "Total Win Percentage: #{allNums.reduce(:+) / (numTests * 1.0)}%\nResults: (#{allNums.join(" + ")}) / #{numTests}"