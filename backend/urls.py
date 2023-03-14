from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_expenes),
    path(r'^submit/expense/$', views.submit_expenes, name='submit_expense')
]
