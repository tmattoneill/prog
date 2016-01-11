from random import randint
from os import rename, remove

score_filename = "scores.txt"
tmp_filename = "scores.tmp"
err_val = str(-1)



def questions():
	operandList = [0, 0, 0, 0, 0]
	operatorList = ['', '', '', '']
	operatorDict = {1:'+',2:'-', 3:'*', 4:'**'}
	
	for index in range(0, 5):
		operandList[index] = randint(1, 9)
	
	for index in range(0, 4): 
		if (index > 0 and operatorList[index-1]!='**'):
			operator = operatorDict[randint(1,4)]
		else:
			operator = operatorDict[randint(1,3)]

		operatorList[index] = operator

	questionString = str(operandList[0])
	
	for index in range (1, 5):
		questionString = questionString + operatorList[index - 1] + str(operandList[index])
		
	result = eval(questionString)
	questionString.replace("**", "^")


def updateUserPoints(newUser, userName, score):
	
	if newUser:
		inputFile = open(score_filename, 'a')
		inputFile.write(userName + ', ' + score)
		inputFile.close()
		return True
	else:
		tmpFile = open(tmp_filename, 'w')
		inputFile = open(score_filename, 'r')
		
		for line in inputFile:
			content = line.split(',')
			if content[0] != userName:
				tmpFile.write(line)
		
		tmpFile.write('\n' + userName + ', ' + score + '\n')
	
	tmpFile.close()
	inputFile.close()
	
	remove(score_filename)
	rename(tmp_filename, score_filename)


def getUserPoint(userName):
	try:
		inputFile = open(score_filename, 'r')
		
		for line in inputFile:
			content = line.split(',')
			if content[0] == userName:
				inputFile.close()
				return content[1]

		inputFile.close()
		print("username '%s' not found in file %s"%(userName, score_filename))
		return err_val
	except IOError:
		print("ERROR: '%s' not found. Creating new %s file"%(score_filename,score_filename))
		inputFile = open(score_filename, 'w')
		inputFile.close()
		return err_val
		

#print (getUserPoint("stuart"))

#updateUserPoints(True, "Stanley", '183')
#updateUserPoints(False, "benny", '158')

while True:
    questions()
