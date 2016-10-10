from method import *


num = 0
docID = 0
binary_flag = False # True for ascii 
dir_tag = False
while num < 4:
	if num%500 == 0:
		dir_tag = True # every 500 pages within a folder
	else:
		dir_tag = False
	data_f = "G:\\nz2_merged\\" + str(num) + "_data"
	index_f = "G:\\nz2_merged\\" + str(num) + "_index"
	docID = handle_index_file(index_f, docID, data_f, dir_tag)
	num += 1 



