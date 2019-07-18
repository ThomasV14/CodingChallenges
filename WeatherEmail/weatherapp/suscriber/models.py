from django.db import models


class City(models.Model):
	name = models.CharField(max_length = 100)
	state = models.CharField(max_length = 100)
	longitude = models.DecimalField(max_digits = 15,decimal_places = 10)
	lattitude = models.DecimalField(max_digits = 15,decimal_places = 10)

	def __str__(self):
		return self.name + ',' + self.state


class Subscription(models.Model):
	email = models.EmailField(unique=True)
	city = models.ForeignKey(City,on_delete=models.CASCADE)

	def __str__(self):
		return self.email + ' ' + str(self.city)