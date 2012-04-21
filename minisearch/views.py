# Create your views here.
#from django.http import HttpResponse
#from django.template import Context, loader
from django.shortcuts import render_to_response
from models import crawl_site, lookup, get_root, get_page, remove_last_slash, compute_ranks, multi_lookup, split_string, quicksort_pages, arrange_links

def index(request):
    return render_to_response('index.html')
def advanced(request):
    return render_to_response('advanced.html')
def results(request):
     inp = request.GET['input']	
     search_words = split_string(str(inp), " ,.?!\"\'~`#$%^&*\n\r()+=;:<>\|/")
     site = remove_last_slash(str(request.GET['site']))
     try:
        request.GET['path']
	advanced = True	
     except: 
	advanced = False
     if advanced:	
     	root = remove_last_slash(str(request.GET['path']))
     else:	
        root = get_root(site)
     if site == root:
        seeds = [site]
     else:
        seeds = [site, root]
     index, graph = crawl_site(list(seeds), root)
     ranks = compute_ranks(graph)
     links = multi_lookup(index, search_words)
     if links == None or links == []:
	if not advanced:
	   return render_to_response('no_results.html', {'input': inp, 
'site':site})
	else:
	   return render_to_response('advanced_no_results.html', {'input': inp, 
'site':site, "links":links,  "path":root})
     links = arrange_links(quicksort_pages(links, ranks))
     try: 
	total = len(links)
     except: 
	total = 0
     if not advanced:
        return render_to_response('results.html', {'input': inp, 
'site':site, "links":links, "total":total})
     else:
	return render_to_response('advanced_results.html', {'input': inp, 
'site':site, "links":links, "total":total, "path":root})
