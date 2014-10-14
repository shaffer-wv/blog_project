from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from blogengine.models import Post, Category, Tag
from blogengine.views import CategoryListView, TagListView, getSearchResults

urlpatterns = patterns('',
	# Index
	url(r'^(?P<page>\d+)?/?$', ListView.as_view(model=Post, paginate_by=5), name='index'),
	# Individual posts
	url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(model=Post,), name='post'),
	# Categories
	url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryListView.as_view(paginate_by=5, model=Category,), name='category'),
	# Tags
	url(r'^tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagListView.as_view(paginate_by=5, model=Tag,), name='tag'),
	# Search
	url(r'^search', getSearchResults, name='search'),
)