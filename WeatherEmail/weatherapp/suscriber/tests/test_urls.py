from django.test import SimpleTestCase
from django.urls import reverse, resolve
from suscriber import views

class TestUrls(SimpleTestCase):
	
	def test_index_url_is_resolved(self):
		url = reverse('suscriber:index')
		self.assertEquals(resolve(url).func.view_class,views.IndexView)

	def test_suscribe_url_is_resolved(self):
		url = reverse('suscriber:suscribe')
		self.assertEquals(resolve(url).func.view_class,views.SuscribeView)
	
	def test_confirm_url_is_resolved(self):
		url = reverse('suscriber:confirm')
		self.assertEquals(resolve(url).func.view_class,views.ConfirmationView)
		
	def test_invalid_url_is_resolved(self):
		url = reverse('suscriber:invalid')
		self.assertEquals(resolve(url).func.view_class,views.InvalidView)