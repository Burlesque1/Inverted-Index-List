import tarfile
import gzip
import zlib
import re
import os



def word_parsing_tool(decomp_data, w_file, docID):
	# patternTag = "<(!|/)?(.|\n)*?>"
	patternTag = "</?[a-zA-Z0-9]+[^><]*>"
	patternBlank = "(^\\s*)|(\\s*$)";
	
	decomp_data_no_tag = re.sub(patternTag,'',str(decomp_data))
	
	
	# for m in re.finditer(r"[A-Za-z]+", text_new):
	for m in re.finditer(r"[A-Za-z]+", str(decomp_data)):
		term, pos = m.group(0), (m.start(), m.end())
		w_file.write(term + ' ' + str(docID) + ' ' + str(m.start()) + '\n')
		# print('%s: %02d-%02d' % (m.group(0), m.start(), m.end()))			
	
	
	
	
def handle_data_file(pos, page_size, file_name):
	with gzip.open(file_name, 'rb') as f:
		f.seek(pos)
		decomp_data= f.read(page_size)
	return decomp_data[0:100]
	# gf = gzip.GzipFile(file_name)
	# print(gf.peek(page_size))
	 
	 
	 
def create_docID_table(url, docID, page_table):
	page_table.write( str(url)+ " " + str(docID) + "\n")
	pass

	
	# for nz2
def handle_index_file2(file_name, docID, data_f, dir_tag):
	pos_accum = 0
	count = docID
	
	directory = str(int(docID/500))
	posting = "/posting_" + file_name[-7]
	if dir_tag == True:
		if not os.path.exists(directory):
			print('Creating directory ' + directory)
			os.makedirs(directory)
		
	# generate intermediate posting
	w_file = open(directory + posting, 'a')				# remember to set as binary/ascii
	page_table = open('page_table','a')		# add exception
	with gzip.open(file_name) as f:			# reduce open/close num
		for line in f:
			line = str(line).split(' ')
			url = line[0]
			size = int(line[3])
			
			# # create page (or docID-to-URL) table.
			# create_docID_table(url, docID, page_table)
			
			print(line)
			print(line[3], pos_accum)
			# # uncompressing gzip file
			# decomp_data = handle_data_file(pos_accum, size, data_f)		
				
			# # call parser to parse decomp_data and generate initial posting
			# word_parsing_tool(decomp_data, w_file, docID)
			
			pos_accum += size
			print('\n\n\n\n')
			docID += 1
			if  docID - count > 5:
				break
	w_file.close()
	page_table.close()
	return docID

	

def handle_tar_file(tar_f, docID, dir_tag, file_num=0):
	directory  = "posting/" 
	if not os.path.exists(directory):
		print('Creating directory ' + directory)
		os.makedirs(directory)
	w_file = open(directory + str(file_num), 'a')				# remember to set as binary/ascii
	page_table = open('page_table','a')		# add exception
	with  tarfile.open(tar_f, "r") as tar:
		count = 0	# count # of files in current tar
		# total_member = len(tar.getmembers())
		for data_mname in tar.getnames():
			if '_data' in data_mname:
				pos = data_mname.find('_data')
				index_mname = data_mname[0:pos] + '_index'
				# data_mname = 
				print(data_mname)
				print(index_mname)
				
				# decomp index
				index_member = tar.getmember(index_mname)
				detar_index = tar.extractfile(index_member).read()
				degz_index= zlib.decompress(detar_index, zlib.MAX_WBITS|32)
				
				# decomp data
				data_member = tar.getmember(data_mname)
				detar_data= tar.extractfile(index_member).read()
				degz_data= zlib.decompress(detar_index, zlib.MAX_WBITS|32)
				
				pos_accum = 0
				for line in str(degz_index).split('\\n')[0:2]:	 # 2 records
					line = line.split(' ')
					url = line[0]
					size = int(line[3])
					# print(line, url, size)
						
					# create page (or docID-to-URL) table.
					create_docID_table(url, docID, page_table)
					
					
					# read block from degz_dara
					data_block = str(degz_data[pos_accum:(pos_accum + size)])
					
					
					# call parser to parse decomp_data and generate initial posting
					word_parsing_tool(data_block, w_file, docID)
						
						
					pos_accum += size
					# print('\n\n\n\n')
					docID += 1
				count += 1	  # index_f is usually from 100/tarfile
			# if count > 1:
				# break
	w_file.close()
	page_table.close()
	return docID, count