from django import forms
from suscriber.models import Subscription, City

class SuscribeForm(forms.ModelForm):

	city = forms.ModelChoiceField(queryset=City.objects.order_by('name'))

	class Meta:
		model = Subscription
		fields = '__all__'
