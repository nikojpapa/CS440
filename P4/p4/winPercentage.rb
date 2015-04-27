sampleSize = 20
sumWins = 0.0

for i in 1..sampleSize
	output = `java AtroposGame 7 "python npapaPlayer.py"`
	# puts output
	if output.include?("Script has won")
		sumWins += 1
	end
end

puts "Win Percentage: #{sumWins / sampleSize * 100}%"