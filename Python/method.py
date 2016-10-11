import tarfile
import gzip
import zlib
import re
import os



def word_parsing_tool(data_block, w_file, docID):
	patternTag = "<[^>]*>"
	# patternTag = "</?[a-zA-Z0-9]+[^><]*>"
	# patternBlank = "(^\\s*)|(\\s*$)";
	patternBlank = r"[\t\r\n\f\v]";
	# print(type(data_block))
	reg1 = re.compile(patternTag)
	reg2 = re.compile(patternBlank)
	reg3 = re.compile(r'&nbsp;')
	content1 = reg1.sub('', data_block)
	content2 = reg2.sub('', content1)
	content3 = reg3.sub('', content2)
	
	
	# for m in re.finditer(r"[A-Za-z]+", text_new):
	for m in re.finditer(r"[A-Za-z]+", content3):
		term, pos = m.group(0), (m.start(), m.end())
		# print(term + ' ' + str(docID) + ' ' + str(m.start()) + '\n')
		# print('%s: %02d-%02d' % (m.group(0), m.start(), m.end()))			
	

	 
	 
	 
def create_docID_table(url, docID, page_table):
	page_table.write(str(url)+ " " + str(docID) + "\n")
	pass

	
	
def decompress(tar, target):
	member = tar.getmember(target)
	de_tar = tar.extractfile(member).read()
	de_gz= zlib.decompress(de_tar, zlib.MAX_WBITS|32)	
	return de_gz
	
	

def handle_data(docID, degz_index, degz_data, page_table, w_file):
	pos_accum = 0
	for line in str(degz_index).replace('b\'', '').split('\\n')[0:-1]:	 # 2 records
		line = line.split(' ')
		url = str(line[0])
		size = int(line[3])
				
		# create page (or docID-to-URL) table.
				
		
		# read block from degz_data
		try:
			data_block = degz_data[pos_accum:(pos_accum + size)].decode(encoding='iso-8859-1')				
			# print(data_block)
		except Exception as e:
			print(e,'iso-8859-1 not work')
			data_block= fd.read(size).decode(encoding='windows-1252')
		except Exception as e:
			print(str(e),'windows-1252 not work')
		else:
			sp = data_block.find('<')
			
			# Skip error pages
			if int(data_block[9:13])>=400: #if data_block[0:15].find(str(404))!=-1:
				# print(data_block[9:13], "error page")
				continue
			# call parser to parse decomp_data and generate initial posting
			
			pos_accum += size
			docID += 1
			# print('\n\n\n\n')
	return docID
	
	
	
	# for NZ
def handle_tar_file(tar_f, docID, file_num=0):
	directory  = "posting/" 
	if not os.path.exists(directory):
		print('Creating directory ' + directory)
		os.makedirs(directory)
	w_file = open(directory + str(file_num), 'a')				# remember to set as binary/ascii
	page_table = open('page_table','a')		# add exception
	with  tarfile.open(tar_f, "r") as tar:
		count = 0	# count # of files in current tar
		for data_mname in tar.getnames():		# 100 files
			if '_data' in data_mname:
				pos = data_mname.find('_data')
				index_mname = data_mname[0:pos] + '_index'
				
				# decomp index
				degz_index = decompress(tar, index_mname)
				
				# decomp data
				degz_data = decompress(tar, data_mname)
				
				# parse url and generate url-table, intermediate postings
				count += 1	  # usually 100/tarfile
				print('\n' + data_mname + ' complete\n')
				print(docID, 'docID')
	w_file.close()
	page_table.close()
	return docID, (file_num + count)
	
	
	
	
	
	# for nz2	
def handle_data_file(pos, page_size, file_name):
	with gzip.open(file_name, 'rb') as f:
		f.seek(pos)
		decomp_data= f.read(page_size)
	return decomp_data[0:100]
	# gf = gzip.GzipFile(file_name)
	# print(gf.peek(page_size))
	
	
	
def handle_index_file(file_name, docID, data_f, dir_tag):
	pos_accum = 0
	count = docID
	
	directory = "posting_" 
	posting = '/' + file_name[-7]
	if dir_tag == True:
		if not os.path.exists(directory):
			print('Creating directory ' + directory)
			os.makedirs(directory)
		
	# generate intermediate posting
	w_file = open(directory + posting, 'a')				# remember to set as binary/ascii
	page_table = open('page_table_nz2','a')		# add exception
	with gzip.open(file_name) as f:			# reduce open/close num
		for line in f:
			line = str(line).split(' ')
			url = line[0]
			size = int(line[3])
			
			# # create page (or docID-to-URL) table.
			create_docID_table(url, docID, page_table)
			
			# print(line)
			# print(line[3], pos_accum)
			# uncompressing gzip file
			decomp_data = handle_data_file(pos_accum, size, data_f).decode(encoding='iso-8859-1')		
				
			# call parser to parse decomp_data and generate initial posting
			# word_parsing_tool(decomp_data, w_file, docID)
			
			pos_accum += size
			docID += 1
			# if  docID - count > 5:
				# break
	w_file.close()
	page_table.close()
	return docID