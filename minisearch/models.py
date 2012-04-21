from django.db import models
from urllib import urlopen

def crawl_site(seed, main): 
    tocrawl = seed
    crawled = []
    graph = {}  
    index = {}
    global root
    root = main    	 
    while tocrawl:	
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
	    if content:
	       add_page_to_index(index, page, content)
               outlinks = get_all_links(content)
	       graph[page] = outlinks
               union(tocrawl, outlinks)
            crawled.append(page)	  	
    return index, graph

def get_page(url): 
    try:
         return urlopen(url).read()
    except:
  	 return False	
    
    
def get_next_target(page):
    page = page.lower()	
    start_link1 = page.find('href =')
    if start_link1 != -1:
       start_link = min(start_link1, page.find('href='))
    else:
       start_link = page.find('href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []    	
    while True:	
        url, endpos = get_next_target(page)	
        if url:
	   url = process_url(url, root)
	   if url:	  
	      links.append(url)
           page = page[endpos:]	   	
        else:
            break
    return links

def get_root(seed):
    double_slash = seed.find("//")
    slash = seed.find("/", double_slash+2)		
    if slash == -1:
       return seed	
    return seed[0:slash]

def remove_last_slash(string):
    if string[-1] == "/":
       return string[0:-1]
    else: 
       return string	
	
def process_url(url, root):#!!!
    url = remove_last_slash(url)
    if root in url:
       return url
    elif url[0:1] == "/":
       return root + url
    elif url.find("//") == -1 or url.find("//") > 6: 
       return root + "/" + url
    else:	
       return False	 

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def add_page_to_index(index, url, content):
    words = split_string(content, " ,.?!\"\'~`#$%^&*\n\r()+=;:<>\|/")
    position = 0	
    for word in words:
        add_to_index(index, word, url, position)
        position = position + 1

def add_to_index(index, keyword, url, position):
    keyword = keyword.lower() 	
    if keyword in index:
        index[keyword].append([url, position])
    else:
        index[keyword] = [[url, position]]

def lookup(index, keyword):
    keyword = keyword.lower()	
    if keyword in index:
        return index[keyword]
    else:
        return None

def multi_lookup(index, keywords):
    if not keywords:
       return []    
    activepos = lookup(index, keywords[0])       
    for keyword in keywords[1:]:
        newactivepos = []
        nexturlpos = lookup(index, keyword)
        if nexturlpos:
           for pos in activepos:
               if [pos[0], pos[1] + 1] in nexturlpos:
                  newactivepos.append([pos[0], pos[1] +1])
        activepos = newactivepos
    result = []
    if activepos == None:
       return None		
    for pos in activepos:
	result.append(pos[0])
    return result


def split_string(source,splitlist):
    output = []
    atsplit = True
    for char in source:
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            else:
                output[-1] = output[-1] + char
    return output

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d*ranks[node]/len(graph[node])
                      
            newranks[page] = newrank
        ranks = newranks
    return ranks

def ordered_search(index, ranks, keyword):
  if keyword in index:
      ranklist = []
      for page in index[keyword]:
          ranklist.append(page[0])
      return quicksort_pages(ranklist, ranks)      
  return None  

def quicksort_pages(pages, ranks):
    if not pages or len(pages) <=1:
       return pages
    else:
       pivot = ranks[pages[0]]
       worse = []
       better = []
       for page in pages[1:]:
           if ranks[page] <= pivot:
              worse.append(page)
           else:
              better.append(page)
    return quicksort_pages(better, ranks)+ [pages[0]]+ quicksort_pages(worse, ranks)

def arrange_links(l):
    results = {}
    for elt in l:
        if elt not in results:
           results[elt] = 1
        else: results[elt] = results[elt]+1
    return results



