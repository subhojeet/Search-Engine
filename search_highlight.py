from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh import query
from whoosh import highlight


# scoring funtion for fragments in highlights
def StandardDeviationScorer(fragment):
	return 0 - stddev([t.pos for t in fragment.matched])

# when searching  via the search button or enter
def mainSearch(userQuery, indexDirectory, freqWeight = scoring.BM25F(), pageLength = 10, resLimit = None):
	ix = open_dir(indexDirectory)
	with ix.searcher(weighting = freqWeight) as searcher:
	    query = QueryParser("content", ix.schema).parse(userQuery)
	    results = searcher.search(query,limit=resLimit)
	    pageLength = min(pageLength,len(results))

	    # adding the highlight fragments corresponding to top results
	    high = []
	    for hit in range (pageLength):
	    	#setting the scorer funtion for scoring of fragments
	    	results[hit].scorer = StandardDeviationScorer
	    	results[hit].order = highlight.SCORE
	    	high.append(results[hit].highlights("content",top=5).encode('utf-8'))
	    
	    
	    # making an array of dictionary 
	    res=[]
	    for i in range (pageLength):
	    	res.append({ 'title':results[i]['title'], 'path':results[i]['path'], 'snippet': high[i]} )
	    
	    x = {'length':len(results) ,'runtime':results.runtime, 'searchResult':res}
	    return x


# when navigating through page numbers
def pageSearch(userQuery, indexDirectory, pageNumber = 1, freqWeight = scoring.TF_IDF(), pageLength = 10, resLimit = None):
	ix = open_dir(indexDirectory)
	with ix.searcher(weighting = freqWeight) as searcher:
	    query = QueryParser("content", ix.schema).parse(userQuery)
	    results = searcher.search_page(query, pageNumber, pagelen=pageLength)
	    pageLength = min(pageLength,len(results))
	    
	    # adding the highlight fragments corresponding to top results
	    high = []
	    for hit in range (pageLength):
	    	#setting the scorer funtion for scoring of fragments
	    	results[hit].scorer = StandardDeviationScorer
	    	results[hit].order = highlight.SCORE
	    	high.append(results[hit].highlights("content",top=5).encode('utf-8'))
	    
	    # making an array of dictionary 
	    res=[]
	    for i in range (pageLength):
	    	res.append({ 'title':results[i]['title'], 'path':results[i]['path'], 'snippet':high[i]} )

	    x = {'length':len(results) , 'searchResult':res}
	    return x


x=pageSearch('Article',"indexdir_stopwords")
print x

