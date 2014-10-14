from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.dates import MonthArchiveView
from blogengine.models import Category, Post, Tag
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

import markdown2

# Create your views here.
class CategoryListView(ListView):
	def get_queryset(self):
		slug = self.kwargs['slug']
		try:
			category = Category.objects.get(slug=slug)
			return Post.objects.filter(category=category)
		except Category.DoesNotExist:
			return Post.objects.none()

class TagListView(ListView):
	def get_queryset(self):
		slug = self.kwargs['slug']
		try:
			tag = Tag.objects.get(slug=slug)
			return tag.post_set.all()
		except Tag.DoesNotExist:
			return Post.objects.none()


class PostMonthArchiveView(MonthArchiveView):
	queryset = Post.objects.all()
	date_field = 'pub_date'
	make_object_list = True


def getSearchResults(request):
	query = request.GET.get('q', '')
	page = request.GET.get('page', 1)

	results = Post.objects.filter(Q(text__icontains=query) | Q(title__icontains=query))

	pages = Paginator(results, 5)

	try:
		returned_page = pages.page(page)
	except EmptyPage:
		returned_page = pages.page(pages.num_pages)

	return render_to_response('blogengine/search_post_list.html',
		{'page_obj': returned_page,
		'object_list': returned_page.object_list,
		'search': query})


	
