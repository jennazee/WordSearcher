#!/usr/bin/python
#word_searcher.py

"""
This program will search through a provided grid for words in a provided list

To run the script, type "python word_searcher.py 'nameOfFile'" into the command line.
Or, you can choose to make it an executable file.
"""

from collections import OrderedDict

def wordsearcher(input):
	"""
	Purpose: To look for a list of given words in a given grid
	and output into the console the start and end coordinates of
	each word in the inputted list

	Input: file 'input' to parse for instructions, wrap flag,
	and word list

	Output: none, technically
	"""

	#parse the input so each line is it's own array
	file = open(input, 'r')
	filelines=[line for line in file.readlines() if line.strip()]
	file.close()
	for i in range(len(filelines)):
		filelines[i]=filelines[i].strip()

	# get grid dimensions
	gridDim = filelines[0].split()
	numRows = int(gridDim[0])
	numCols = int(gridDim[1])

	# make grid, which is lines 1 to height of grid in the inputted document
	grid = []
	for i in range(1,numRows+1):
		grid.append(filelines[i])

	# wrap?
	wrap = not ('NO' in filelines[numRows+1])

	# make word list
	numWords = filelines[numRows+2]
	words = []
	locations = OrderedDict()

	for j in range(numRows+3, len(filelines)):
		words.append(filelines[j])
		locations[filelines[j]]='NOT FOUND'

	sep=''


	# *** HELPER METHODS ***

	def row_search(grid, wrap):
		"""
		Purpose: Look for words in the grid's rows
		Input: grid, wrap boolean
		Output: OrderedDict of word:location pairs
		"""
		tempLoc = OrderedDict()
		for i in range(numRows):
			if wrap:
				row = grid[i] + grid[i]
			else:
				row = grid[i]
			for word in words:
				if len(word) > numCols:
					continue
				if word in row:
					start = row.find(word)
					end = start+len(word)-1
					tempLoc[word]=[[i,start%numCols], [i,end%numCols]]
		return tempLoc
		
	
	# I debated between writing this method and a method that would 
	# transpose the matrix and run row_search on it.
	def col_search(grid, wrap):
		"""
		Purpose: Look for words in the grid's columns
		Input: grid, wrap boolean
		Output: OrderedDict of word:location pairs
		"""
		tempLoc= OrderedDict()
		for i in range(numCols):
			colVector = []
			for j in range(numRows):
				colVector.append(grid[j][i])
				col = sep.join(colVector)
				if wrap:
					col = col + col
			for word in words:
				if len(word) > numRows:
					continue
				if word in col:
					start = col.find(word)
					end = start+len(word)-1
					tempLoc[word] = [[start%numRows,i], [end%numRows,i]]
		return tempLoc

	
	def top_diag_search(grid,wrap):
		"""
		Purpose: Look for words in the grid's diagonals from the top
		Input: grid, wrap boolean
		Output: OrderedDict of word:location pairs
		"""
		tempLoc=OrderedDict()
		for c in range(numCols-1):
			anchor = c
			r = 0
			diagVector = []
			while c <= numCols-1 and r<= numRows-1:
				diagVector.append(grid[r][c])
				r+=1
				c+=1
			diag = sep.join(diagVector)
			#to check for reused letters
			span = len(diag)
			if wrap:
				diag = diag+diag
	  		for word in words:
	  			if len(word) > span:
	  				continue
	  			if word in diag:
	  				start = diag.find(word)
	  				end = start+len(word)-1
	  				tempLoc[word]=[[start%span, (start+anchor)%span], [end%span, (end+anchor)%span]]
	  	return tempLoc

	def left_diag_search(grid, wrap):
		"""
		Purpose: Look for words in the grid's diagonals from the lefthand side
		Input: grid, wrap boolean
		Output: OrderedDict of word:location pairs
		"""
		tempLoc = OrderedDict()
	  	#don't need to repeat the one starting at 0,0
	  	for r in range(1,numRows-1):
	  		anchor = r
	  		c = 0
	  		diagVector = []
	  		while r < numRows and c < numCols:
	  			diagVector.append(grid[r][c])
	  			r+=1
	  			c+=1
	  		diag = sep.join(diagVector)
	  		#to check for reused letters
			span = len(diag)
	  		if wrap:
	  			diag = diag+diag
	  		for word in words:
	  			if len(word) > span:
	  				continue
	  			if word in diag:
	  				start = diag.find(word)
	  				end = start+len(word)-1
	  				tempLoc[word]=[[start%span+anchor, start%span], [end%span+anchor, end%span]]
	  	return tempLoc

	
	# *** SEARCHING THE GRID ***

	# normal grid
	normal = row_search(grid, wrap)
	normal.update(col_search(grid, wrap))
	normal.update(top_diag_search(grid, wrap))
	normal.update(left_diag_search(grid, wrap))
	for k in normal:
		locations[k] = normal[k]

	# grid flipped vertically
	vFlipped = []
	for i in range(numRows, 0, -1):
		vFlipped.append(filelines[i])
	#not all of the searches need to be performed again
	#(which is the purpose of the split-up methods to begin with)
	vertPre = col_search(vFlipped, wrap)
	vertPre.update(top_diag_search(vFlipped, wrap))
	vertPre.update(left_diag_search(vFlipped, wrap))
	for k in vertPre:
		#invert the row coordinates to undo the flip
		v = vertPre[k]
		locations[k] = [[numRows-v[0][0]-1, v[0][1]],[numRows-v[1][0]-1, v[1][1]]]

	# grid flipped horizontally
	hFlipped = []
	for line in grid:
		hFlipped.append(line[::-1])
	horzPre = row_search(hFlipped, wrap)
	horzPre.update(top_diag_search(hFlipped, wrap))
	horzPre.update(left_diag_search(hFlipped, wrap))
	for k in horzPre:
		#invert the column coordinates to undo the flip
		v=horzPre[k]
		locations[k] = [[v[0][0],numCols-v[0][1]-1],[v[1][0], numCols-v[1][1]-1]]

	
	# outputting
	for k in locations:
		v = locations[k]
		if v is not 'NOT FOUND':
			print '('+str(v[0][0])+','+str(v[0][1])+') ('+str(v[1][0])+','+str(v[1][1])+')'
		else:
			print v

import sys
wordsearcher(sys.argv[1])