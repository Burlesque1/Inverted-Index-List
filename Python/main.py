from method import *


num = 0
docID = 0
binary_flag = False # True for ascii 
dir_tag = False
while num < 1:
	if num%500 == 0:
		dir_tag = True # every 500 pages within a folder
	else:
		dir_tag = False
	data_f = "H:\nz2_merged\\" + str(num) + "_data"
	index_f = "H:\\nz2_merged\\" + str(num) + "_index"	
	# docID = handle_index_file2(index_f, docID, data_f, dir_tag)
	
	tar_f = "H:\\NYU\\CS 6913\\Assignment2\\NZ\\vol_0_99.tar"
	docID = handle_index_file(tar_f, docID, data_f, dir_tag)
	num += 1



