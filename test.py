import gzip
from html.parser import HTMLParser
from html.entities import name2codepoint
import re


a=1
b=1



def h(g):
	g+=1
	return g

	
	text = "He was carefully disguised but captured quickly by police. This is <b>so</b> much <b><em>fun</em></b>"	
	text_new = re.sub(patternTag,'',text)
	print(text)
	print(re.sub(patternTag,'',text))

	
while a<5:
	b=h(b)
	print(b)
	a+=1
	
d=open('df.txt','wb')
# d.write(1)
fd='dfa'
print(type(fd.format('b')))