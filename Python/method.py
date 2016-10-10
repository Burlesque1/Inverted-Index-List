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
	
	# for nz
def handle_index_file(tar_f, docID, data_f, dir_tag):
	count = docID	
	# directory = str(int(docID/500))
	# posting = "/posting_" + file_name[-7]
	# if dir_tag == True:
		# if not os.path.exists(directory):
			# print('Creating directory ' + directory)
			# os.makedirs(directory)
		
	# # generate intermediate posting
	# w_file = open(directory + posting, 'a')				# remember to set as binary/ascii
	# page_table = open('page_table','a')		# add exception
	with  tarfile.open(tar_f, "r") as tar:
		print(len(tar.getmembers()))
		index_f=0
		for member in tar.getmembers():	# [200 files + 1 folder]
			if member.isreg()and member.name.find("index")!= -1:
				pos_accum = 0
				detar_content = tar.extractfile(member).read()
				degz_content= zlib.decompress(detar_content, zlib.MAX_WBITS|32)
				# print(type(degz_content), len(degz_content),degz_content[0:10])
				
				for line in str(degz_content).split('\\n')[0:2]: # 10 records
					line = line.split(' ')
					url = line[0]
					size = int(line[3])
					print(line, url, size)
			
					# # create page (or docID-to-URL) table.
					# create_docID_table(url, docID, page_table)
					
					# # uncompressing gzip file
					# decomp_data = handle_data_file(pos_accum, size, data_f)		
						
					# # call parser to parse decomp_data and generate initial posting
					# word_parsing_tool(decomp_data, w_file, docID)
					
					pos_accum += size
					print('\n\n\n\n')
					docID += 1
				index_f += 1
				print("index", index_f)
				if index_f > 1:
					break
	# w_file.close()
	# page_table.close()
	return docID