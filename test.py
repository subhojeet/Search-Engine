
import urllib
from bs4 import BeautifulSoup


f = open("delete.txt","w")
soup = BeautifulSoup(open("test_dataset/128570"))
l = []

alt= ''

for a in soup.findAll('a'):
    for img in a.findAll('img'):
	if(img['alt']!=''):
	    alt+=' ' + img['alt']
	
print alt

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out


# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = u''.join((u' ' + chunk) for chunk in chunks if chunk).encode('utf-8').strip()

text+=alt

f.write(text)
f.close()

