from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh import query
ix = open_dir("indexdir")


# when searching  via the search button or enter
def mainSearch(userQuery,freqWeight = scoring.TF_IDF(), pageLength = 10, resLimit = None):
	with ix.searcher(weighting = freqWeight) as searcher:
	    query = QueryParser("content", ix.schema).parse(userQuery)
	    results = searcher.search(query,limit=resLimit)
	    print results
	    pageLength = min(pageLength,len(results))
	    
	    # making an array of dictionary 
	    res=[]
	    for i in range (pageLength):
	    	res.append({ 'title':results[i]['title'], 'path':results[i]['path']} )
	    
	    x = {'length':len(results) ,'runtime':results.runtime, 'searchResult':res}
	    return x


# when navigating through page numbers
def pageSearch(userQuery, pageNumber = 1, freqWeight = scoring.TF_IDF(), pageLength = 10, resLimit = None):
	with ix.searcher(weighting = freqWeight) as searcher:
	    query = QueryParser("content", ix.schema).parse(userQuery)
	    results = searcher.search_page(query, pageNumber, pagelen=pageLength)
	    pageLength = min(pageLength,len(results))
	    
	    # making an array of dictionary 
	    res=[]
	    for i in range (pageLength):
	    	res.append({ 'title':results[i]['title'], 'path':results[i]['path']} )

	    x = {'length':len(results) , 'searchResult':res}
	    return x


x=mainSearch('"THERE is home"')
print x
