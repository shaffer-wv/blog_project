from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from blogengine.models import Post, Category, Tag

import markdown

# Create your tests here.
class PostTest(TestCase):

	def test_create_tag(self):
		tag = Tag()

		tag.name = 'python'
		tag.slug = 'python'
		tag.save()

		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)
		only_tag = all_tags[0]
		self.assertEquals(only_tag, tag)

		self.assertTrue(only_tag.name, 'python')
		self.assertTrue(only_tag.slug, 'python')

	def test_create_category(self):
		# Create the category
		category = Category()

		# Add attributes
		category.name = 'python'
		category.description = 'The Python programming language'
		category.slug = 'python'

		category.save()

		# Check we can find it
		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)
		only_category = all_categories[0]
		self.assertEquals(only_category, category)

		# Check attributes
		self.assertEquals(only_category.name, 'python')
		self.assertEquals(only_category.description, 'The Python programming language')
		self.assertEquals(only_category.slug, 'python')

	def test_create_post(self):
		tag = Tag()
		tag.name = 'python'
		tag.save()

		# Create the category
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		# Create the post
		post = Post()

		# Set the attributes
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.category = category

		# Save it
		post.save()

		# Add the tag to the post
		post.tags.add(tag)
		post.save()

		# Check we can find it
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		# Check attributes
		self.assertEquals(only_post.title, 'My first post')
		self.assertEquals(only_post.text, 'This is my first blog post')
		self.assertEquals(only_post.slug, 'my-first-post')
		self.assertEquals(only_post.pub_date.day, post.pub_date.day)
		self.assertEquals(only_post.pub_date.month, post.pub_date.month)
		self.assertEquals(only_post.pub_date.year, post.pub_date.year)
		self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
		self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
		self.assertEquals(only_post.pub_date.second, post.pub_date.second)
		self.assertEquals(only_post.category.name, 'python')
		self.assertEquals(only_post.category.description, 'The Python programming language')

		# Check tags
		post_tags = only_post.tags.all()
		self.assertEquals(len(post_tags), 1)
		only_post_tag = post_tags[0]
		self.assertEquals(only_post_tag, tag)
		self.assertEquals(only_post_tag.name, 'python')

class BaseAcceptanceTest(LiveServerTestCase):
	def setUp(self):
		self.client = Client()

class AdminTest(BaseAcceptanceTest):
	fixtures = ['users.json']

	def test_login(self):
		# Get login page
		response = self.client.get('/admin/')

		# Check response code
		self.assertEquals(response.status_code, 200)

		# Check 'Log in' in response
		self.assertTrue('Log in' in response.content)

		# Log the user in
		self.client.login(username='bobsmith', password="password")

		# Check the response code
		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)

		# Check 'Log out' in response
		self.assertTrue('Log out' in response.content)

	def test_logout(self):
		# Log in
		self.client.login(username='bobsmith', password="password")

		# Check response code
		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)

		# Check 'Log out' in response
		self.assertTrue('Log out' in response.content)

		# Log out
		self.client.logout()

		# Check response code
		response = self.client.get('/admin/')
		self.assertEquals(response.status_code, 200)

		# Check 'Log in' in response
		self.assertTrue('Log in' in response.content)

	def test_create_post(self):
		# Create the category
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'python'
		tag.save()

		# Log in
		self.client.login(username='bobsmith', password="password")

		# Check response code
		response = self.client.get('/admin/blogengine/post/add/')
		self.assertEquals(response.status_code, 200)

		# Create the new post
		response = self.client.post('/admin/blogengine/post/add/', {
			'title': 'My first post',
			'text': 'This is my first post',
			'slug': 'my-first-post',
			'pub_date_0': '2014-9-23',
			'pub_date_1': '22:00:04',
			'site': '1',
			'category': '1',
			'tags': '1'
			},
			follow=True)
		self.assertEquals(response.status_code, 200)

		# Check added successfully
		self.assertTrue('added successfully' in response.content)

		# Check new post now in database
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

	def test_edit_post(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'python'
		tag.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		# Create the post
		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first post'
		post.slug = 'my-first-post'
		post.pub_date = timezone.now()
		post.site = site
		post.category = category
		post.save()
		post.tags.add(tag)
		post.save()

		# Log in
		self.client.login(username='bobsmith', password="password")

		# Edit the post
		response = self.client.post('/admin/blogengine/post/1/', {
			'title': 'My second post',
			'text': 'This is my second post',
			'slug': 'my-second-post',
			'pub_date_0': '2014-9-23',
			'pub_date_1': '22:00:05',
			'site': '1',
			'category': '1',
			'tags': '1'
			},
			follow=True)
		self.assertEquals(response.status_code, 200)

		# Check changed successfully
		self.assertTrue('changed successfully' in response.content)

		# Check edits are in database
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post.title, 'My second post')
		self.assertEquals(only_post.text, 'This is my second post')
		self.assertEquals(only_post.slug, 'my-second-post')

	def test_delete_post(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'python'
		tag.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		# Create the post
		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first post'
		post.slug = 'my-first-post'
		post.pub_date = timezone.now()
		post.site = site
		post.category = category
		post.save()
		post.tags.add(tag)
		post.save()

		# Log in
		self.client.login(username='bobsmith', password="password")

		# Delete post
		response = self.client.post('/admin/blogengine/post/1/delete/', {
			'post': 'yes'
			}, follow=True)
		self.assertEquals(response.status_code, 200)

		# Check deleted successfully
		self.assertTrue('deleted successfully' in response.content)

		# Check post deleted
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 0)

	def test_create_category(self):
		self.client.login(username='bobsmith', password="password")

		response = self.client.get('/admin/blogengine/category/add/')
		self.assertEquals(response.status_code, 200)

		response = self.client.post('/admin/blogengine/category/add/', {
			'name': 'python',
			'description': 'The Python programming language'
			}, follow=True)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('added successfully' in response.content)

		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)

	def test_edit_category(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		self.client.login(username='bobsmith', password="password")

		response = self.client.post('/admin/blogengine/category/1/', {
			'name': 'perl',
			'description': 'The Perl programming language'
			}, follow=True)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('changed successfully' in response.content)

		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 1)
		only_category = all_categories[0]
		self.assertEquals(only_category.name, 'perl')
		self.assertEquals(only_category.description, 'The Perl programming language')

	def test_delete_category(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		self.client.login(username='bobsmith', password="password")

		response = self.client.post('/admin/blogengine/category/1/delete/', {
			'post': 'yes'
			}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('deleted successfully' in response.content)

		all_categories = Category.objects.all()
		self.assertEquals(len(all_categories), 0)

	def test_create_tag(self):
		self.client.login(username='bobsmith', password="password")

		response = self.client.get('/admin/blogengine/tag/add/')
		self.assertEquals(response.status_code, 200)

		response = self.client.post('/admin/blogengine/tag/add/', {
			'name': 'python',
			}, follow=True)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('added successfully' in response.content)

		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)

	def test_edit_tag(self):
		tag = Tag()
		tag.name = 'python'
		tag.save()

		self.client.login(username='bobsmith', password="password")

		response = self.client.post('/admin/blogengine/tag/1/', {
			'name': 'java',
			}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('changed successfully' in response.content)

		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 1)
		only_tag = all_tags[0]
		self.assertEquals(only_tag.name, 'java')

	def test_delete_tag(self):
		tag = Tag()
		tag.name = 'python'
		tag.save()

		self.client.login(username='bobsmith', password="password")

		response = self.client.post('/admin/blogengine/tag/1/')
		self.assertEquals(response.status_code, 200)

		response = self.client.post('/admin/blogengine/tag/1/delete/', {
			'post': 'yes'
			}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('deleted successfully' in response.content)

		all_tags = Tag.objects.all()
		self.assertEquals(len(all_tags), 0)

	def test_create_post_without_tag(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		# Log in
		self.client.login(username='bobsmith', password="password")

		# Check response code
		response = self.client.post('/admin/blogengine/post/add/', {
			'title': 'My first post',
			'text': 'This is my first post',
			'pub_date_0': '2014-10-2',
			'pub_date_1': '22:00:04',
			'slug': 'my-first-post',
			'site': '1',
			'category': '1'
			},
			follow=True)
		self.assertEquals(response.status_code, 200)

		self.assertTrue('added succesfully' in response.content)

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
	

class PostViewTest(BaseAcceptanceTest):
	
	def test_index(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'perl'
		tag.save()

		# Create the site
		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		# Create the post
		post = Post()
		post.title = 'My first post'
		post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
		post.slug = 'my-first-post'
		post.pub_date = timezone.now()
		post.site = site
		post.category = category
		post.save()
		post.tags.add(tag)
		post.save()

		# Check new post saved
		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)

		# Fetch the index
		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)

		# Check the post title is in the response
		self.assertTrue(post.title in response.content)

		# Check the post text is in the response
		self.assertTrue(markdown.markdown(post.text) in response.content)
		self.assertTrue(markdown.markdown(post.text) in response.content)

		# Check the category is in the response
		self.assertTrue(post.category.name in response.content)

		# Check the tag is in the response
		post_tag = all_posts[0].tags.all()[0]
		self.assertTrue(post_tag.name in response.content)

		# Check post date is in the response
		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

		# Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

	def test_individual_post(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		tag = Tag()
		tag.name = 'perl'
		tag.save()

		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.category = category
		post.save()
		post.tags.add(tag)
		post.save()

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		post_url = only_post.get_absolute_url()

		response = self.client.get(post_url)
		self.assertEquals(response.status_code, 200)

		self.assertTrue(post.title in response.content)
		self.assertTrue(markdown.markdown(post.text) in response.content)

		self.assertTrue(post.category.name in response.content)

		post_tag = all_posts[0].tags.all()[0]
		self.assertTrue(post_tag.name in response.content)

		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

	def test_category_page(self):
		category = Category()
		category.name = 'python'
		category.description = 'The Python programming language'
		category.save()

		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.category = category
		post.save()

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		category_url = post.category.get_absolute_url()

		# Fetch the category
		response = self.client.get(category_url)
		self.assertEquals(response.status_code, 200)

		self.assertTrue(post.category.name in response.content)
		self.assertTrue(post.title in response.content)

	def test_tag_page(self):
		tag = Tag()
		tag.name = 'python'
		tag.save()

		site = Site()
		site.name = 'example.com'
		site.domain = 'example.com'
		site.save()

		post = Post()
		post.title = 'My first post'
		post.text = 'This is my first blog post'
		post.pub_date = timezone.now()
		post.slug = 'my-first-post'
		post.site = site
		post.save()
		post.tags.add(tag)
		post.save()

		all_posts = Post.objects.all()
		self.assertEquals(len(all_posts), 1)
		only_post = all_posts[0]
		self.assertEquals(only_post, post)

		tag_url = post.tags.all()[0].get_absolute_url()

		response = self.client.get(tag_url)
		self.assertEquals(response.status_code, 200)

		self.assertTrue(post.tags.all()[0].name in response.content)

		self.assertTrue(markdown.markdown(post.text) in response.content)

		self.assertTrue(str(post.pub_date.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.pub_date.day) in response.content)

	def test_nonexistent_category_page(self):
		category_url = '/category/blah'
		response = self.client.get(category_url)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('No posts found' in response.content)

	def test_nonexistent_tag_page(self):
		tag_url = '/tag/blah'
		response = self.client.get(tag_url)
		self.assertEquals(response.status_code, 200)
		self.assertTrue('No posts found' in response.content)

class FlatPageViewTest(BaseAcceptanceTest):
	def test_create_flat_page(self):
		# Create flag page
		page = FlatPage()
		page.url = '/about/'
		page.title = 'About me'
		page.content = 'All about me'
		page.save()

		# Add the site
		page.sites.add(Site.objects.all()[0])
		page.save()

		# Check new page saved
		all_pages = FlatPage.objects.all()
		self.assertEquals(len(all_pages), 1)
		only_page = all_pages[0]
		self.assertEquals(only_page, page)

		# Check data correct
		self.assertEquals(only_page.url, '/about/')
		self.assertEquals(only_page.title, 'About me')
		self.assertEquals(only_page.content, 'All about me')

		# Get url
		page_url = only_page.get_absolute_url()

		# Get page
		response = self.client.get(page_url)
		self.assertEquals(response.status_code, 200)

		# Check title and content in response
		self.assertTrue('About me' in response.content)
		self.assertTrue('All about me' in response.content)