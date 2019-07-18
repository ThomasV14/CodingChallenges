from django.test import TestCase
from suscriber.models import Subscription, City
from suscriber.forms import SuscribeForm



class TestForms(TestCase):

	def setUp(self):
		self.cities = City.objects.all()
		self.test_valid_email = 'test1@yahaoo.com'
		self.test_invalid_email = 'invalid@invalid'
		self.valid_subscription = Subscription.objects.create(email=self.test_valid_email,city=self.cities[0])
		self.invalid_subscription = Subscription.objects.create(email=self.test_invalid_email,city=self.cities[0])

	def test_valid_form(self):
		sub = Subscription.objects.all()
		form_data = {'email':self.test_valid_email,'city':sub[0].id}
		form = SuscribeForm(data=form_data,instance=self.valid_subscription)
		self.assertTrue(form.is_valid())

	def test_invalid_form(self):
		sub = Subscription.objects.all()
		form_data = {'email':self.test_invalid_email,'city':sub[1].id}
		form = SuscribeForm(data=form_data,instance=self.invalid_subscription)
		self.assertFalse(form.is_valid())