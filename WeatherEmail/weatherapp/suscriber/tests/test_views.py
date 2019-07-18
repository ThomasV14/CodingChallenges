from django.test import TestCase, Client
from django.urls import reverse
from suscriber import models


class TestViews(TestCase):
	
	def setUp(self):
		self.client = Client()

		self.index_url = reverse('suscriber:index')
		self.subscribe_url = reverse('suscriber:suscribe')
		self.confirm_url = reverse('suscriber:confirm')
		self.invalid_url = reverse('suscriber:invalid')

		self.index_template = 'suscriber/index.html'
		self.subscribe_template = 'suscriber/suscribe_page.html'
		self.confirm_template = 'suscriber/confirmation_page.html'
		self.invalid_template = 'suscriber/invalid_page.html'

	def test_index_GET(self):
		response = self.client.get(self.index_url)
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,self.index_template)

	def test_subscribe_GET(self):
		response = self.client.get(self.subscribe_url)
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,self.subscribe_template)

	def test_confirm_GET(self):
		response = self.client.get(self.confirm_url)
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,self.confirm_template)

	def test_invalid_GET(self):
		response = self.client.get(self.invalid_url)
		self.assertEquals(response.status_code,200)
		self.assertTemplateUsed(response,self.invalid_template)