from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item
from lists.views import home_page

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html',
			{ 'comment': 'Yey, waktunya berlibur' }
		)
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_displays_comment_if_To_Do_list_empty(self):
		request = HttpRequest()
		response = home_page(request)

		self.assertEqual(Item.objects.count(),0)
		self.assertIn('Yey, waktunya berlibur', response.content.decode())

	def test_home_page_display_comment_if_To_Do_list_less_than_5(self):
		Item.objects.create(text='itemey 1')
		
		request = HttpRequest()
		response = home_page(request)

		self.assertLess(Item.objects.count() , 5)
		self.assertIn('Sibuk tapi santai', response.content.decode())
	
	def test_home_page_display_comment_if_To_Do_list_greater_equal_than_5(self):
		Item.objects.create(text='item 1')
		Item.objects.create(text='item 2')
		Item.objects.create(text='item 3')
		Item.objects.create(text='item 4')
		Item.objects.create(text='item 5')

		request = HttpRequest()
		response = home_page(request)
	
		self.assertGreaterEqual(Item.objects.count(), 5)
		self.assertIn('Oh tidak', response.content.decode())

class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')

class ListViewTest(TestCase):

	def test_uses_list_templete(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_items(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):
	
	def test_save_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
		