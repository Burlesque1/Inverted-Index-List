

lexicon = dict()

iif = open('inverted_index_list', 'wb')
with open('merged-file') as f:
	curr_term = ''
	for line in f:
		l = line.split(' ')
		if  line[0] = curr_term:
			# write into file in bytes
			iif.write()
			# accumulate pos
			pass
		else:
			curr_term = line[0]
			# lexicon[pos] = here
			pass
			# continuously write into file
			# just use lexicon to record pos