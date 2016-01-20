"""
Merge function for 2048 game.
"""
def right_zeros(line):
	""" Move all non-zero values to the front and append zeroes to the end"""
	list_zero = [_ for _ in line if _ == 0 ]
	list_copy = [_ for _ in line if _ > 0 ]
	list_copy.extend(list_zero)
	return list_copy
	
def merge(line):
	"""
	Function that merges a single row or column in 2048.
	"""
	tmp_list = []
	working_list = right_zeros(line[:])
	for index, item in enumerate(working_list):
		if index < len(working_list)-1: #in the list and not at the end of the list
			if item == working_list[index + 1]:
				tmp_list.append(item * 2)
				working_list[index+1]=0 # append matched * 2 and change next item to 0
			else:
				tmp_list.append(item) # append nonzero non matched
		else: 
			tmp_list.append(item) # append last item
			
	return right_zeros(tmp_list)

print merge([8,8])