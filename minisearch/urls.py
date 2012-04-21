from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('minisearch.views',
    # Examples:
    # url(r'^$', 'mini.views.home', name='home'),
    # url(r'^mini/', include('mini.foo.urls')),
    url(r'^$', 'index'),
    url(r'^results/$', 'results'),
    url(r'^advanced.html$', 'advanced'),
    

   
	


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
