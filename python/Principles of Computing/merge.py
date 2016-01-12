"""
Merge function for 2048 game.
"""


def multiply(line):
	"""
	Takes a treated line and returns the 2048 algorithm output multiplying
	found numbers by two and moving empty cells to the end.
	"""
	tmp_list = []
	index = 0
	
	# if it's just an empty of length of one list return it
	if len(line) <= 1:
		return line
	
	# main algorithm
	while index < len(line):
		# deal with end of list issues
		if index == len(line) - 1:
			tmp_list.append(line[index])
			break
		
		# if an adjacent cell is a duplicate, multiply
		# by 2 , add it to results, and skip the next 
		# iteration of the main line. Otherwise just
		# stick the value on the end and move to the next
		# item.
		if line[index] == line[index+1]:
			tmp_list.append(line[index] * 2)
			index += 2
		else:
			tmp_list.append(line[index])
			index += 1
	
	# if it's an odd-length list append the final number
	if 2 % len(line) == 0 and line[-1] > 0:
		tmp_list.append(line[-1])
		
	# stick the zeroes on the end    
	line_diff = len(line) - len(tmp_list)
	
	# fill in trailing zeroes
	tmp_list.extend([0] * line_diff)
	return tmp_list
			

def merge(line):
	"""
	Function that merges a single row or column in 2048.
	"""
	result_list = [0] * len(line)
	result_index = 0
	for item in line:
		if item > 0:
			result_list[result_index] = item
			result_index += 1

	return multiply(result_list)

print str(merge([2,2,16,2,2]))
