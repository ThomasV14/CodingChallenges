from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from suscriber.forms import SuscribeForm

class IndexView(TemplateView):
	template_name = 'suscriber/index.html'

class ConfirmationView(TemplateView):
	template_name = 'suscriber/confirmation_page.html'

class InvalidView(TemplateView):
	template_name = 'suscriber/invalid_page.html'

class SuscribeView(TemplateView):
	template_name = 'suscriber/suscribe_page.html'
	form_class = SuscribeForm

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		form = self.form_class()
		context['form'] = form
		return context

	def post(self,request,**kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect(reverse('suscriber:confirm'))
		else:
			return HttpResponseRedirect(reverse('suscriber:invalid'))