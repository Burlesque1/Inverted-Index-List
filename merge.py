from queue import PriorityQueue

q=PriorityQueue()
q.put(1)

heap = PriorityQueue()

num = 0
file_index = dict()
while num < 4:
	file_name = 'posting_' + str(num)
	f=open(file_name, 'r')
	file_index[num] = f
	num += 1

for index, file in file_index.items():
	line = file.readline()
	print(index, line)
	heap.put((line,index))