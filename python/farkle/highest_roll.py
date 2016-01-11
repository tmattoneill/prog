"""
	written and tested in Python 3.3.6
"""

from random import randint
import collections

def score(my_roll, sides=6):
	"""
		Calculate a Farkle score using the traditional scoring method, which is:
			4 1s:     2,000 points
			3 1s:     1,000 points
			Single 1: 100 points
			Single 5: 50 points
			Triple of any non-1 number:    100 x number showing
			Quadruple of any non-1 number: Double the triple score
			
		Notes:
			- Doubles score nothing (unless a 1 or a 5) as above
			- All scoring dice must be rolled in a single turn (i.e. they
			are not additive over turns)
			- Rolling all 6 will be two sets and scored accordingly
				[4] + [2]
				[3] + [3]
				[2] + [2] + [2]
				
		Examples:
			1,1,1,5,5,5 ==> 1250 (1000 for 1s + 250 for 3 5s)
			1,1,1,1,6,6 ==> 2000 (2000 for 4 1s)
			5,3,6,5,3,3 ==> 400 (300 for 3 3s + 100 for 2 5s)
			1,2,2,3,3,5 ==> 150 (100 for a 1 and 50 for a 5)
	"""
	#create a table to hold the count of each die roll
	dice_array = [0] * sides
	score = 0
	counts = collections.Counter(my_roll)
	print(counts)
	#add up the number appearances of each die roll and store it in the table
	
	for dice in my_roll:
		dice_array[dice-1] += 1

	"""
		based on the above scoring, determine the MAXIMUM score; in actual Farkle the
		player would choose which die to 'bank' and which to re-roll
	"""
	for (dice, count) in enumerate(dice_array, start=1):		
		if dice == 1:
			if count == 6: score += 2200
			if count == 5: score += 2100			
			if count == 4: score += 2000
			if count == 3: score += 1000
			if count in [1, 2]: score += (count * 100)
		else:
			if count >= 4: score += (dice * 200)
			if count >= 3: score += (dice * 100)
			if (dice == 5 and count != 3): score += (count * 50)                             

	return score
		
#test cases
while True:
	roll = input("Enter 6 values (1-6) separated by a space: ")
	roll = [randint(1,6) for i in range(0, 6)] if roll == "" else [int(i) for i in roll.split(' ')]
	print(str(score(roll)) + " : " + str(roll))