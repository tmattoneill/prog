#!/usr/bin/python

def update_list_vals(a_list, remove_list):
	a_set = set(a_list)
	remove_set = set(remove_list)
	a_set.difference_update(remove_set)
	
	my_list = list(a_set)

my_list = list(range(5))
print "Original list: "	 + str(my_list)

remove_str = raw_input("Remove which values: ")
remove_list = [int(i) for i in remove_str]

update_list_vals(my_list, remove_list)
print "Resulting list:" + str(my_list)