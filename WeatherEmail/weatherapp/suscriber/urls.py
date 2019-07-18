from django.urls import path
from suscriber import views

app_name = 'suscriber'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('suscribe/', views.SuscribeView.as_view(), name='suscribe'),
    path('invalid/',views.InvalidView.as_view(),name='invalid'),
    path('confirm/',views.ConfirmationView.as_view(),name='confirm')
]