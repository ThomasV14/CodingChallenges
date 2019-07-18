from django.test import TestCase
from suscriber.models import Subscription, City



class TestModels(TestCase):

	def setUp(self):
		self.cities = City.objects.all()
		self.test_email = 'test1@yahaoo.com'
	
	def test_top_cities(self):
		self.assertEquals(len(self.cities),100)

	def test_creation_subscription(self):
		subscription = Subscription.objects.create(email=self.test_email,city=self.cities[0])
		self.assertEquals(subscription.email,self.test_email)
		self.assertEquals(subscription.city,self.cities[0])
		subs = Subscription.objects.all()
		self.assertEquals(len(subs),1)