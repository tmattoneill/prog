import re
print (sum(list(map(int, re.findall('[0-9]+', open("regex_sum_204180.txt", 'r').read())))))
