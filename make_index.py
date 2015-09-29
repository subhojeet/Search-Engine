import os
import urllib
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import *

# get the page content
def getPageContent(filepath):
	soup = BeautifulSoup(open(filepath))
	l = []

	alt = ''

	# extract the Alts in the imagetag of links
	# for a in soup.findAll('a'):
	#     for img in a.findAll('img'):
	# 		if(img['alt'] and img['alt']!=''):
	# 		    alt+=u' ' + img['alt']
	

	# kill all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out

	# add the alt extracted from the hyperlinks
	# text = alt
	
	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = u''.join((u' ' + chunk) for chunk in chunks if chunk).encode('utf-8').strip()
	return text 


# get the title of the page
def getPageTitle(filepath):
	soup = BeautifulSoup(open(filepath))
	if not soup.title:
		return ""

	return soup.title.string


schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = create_in("indexdir", schema)
writer = ix.writer()

#f = open("files.txt","w")


for root, directories, filenames in os.walk(ur'dataset/'):
    for filename in filenames:
		pageContent = getPageContent(os.path.join(root,filename))
		pageTitle = getPageTitle(os.path.join(root,filename))
		writer.add_document(title=unicode(pageTitle), path  = unicode(os.path.join(root,filename)), content=unicode(pageContent.decode('utf-8')))


writer.commit()

'''
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("Log")
    results = searcher.search(query)
    print results[0]'''

#f.close()
