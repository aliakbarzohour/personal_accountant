from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    re_path(r'^submit/expense/$', views.submit_expenes, name='submit_expense'),
    re_path(r'^submit/income/$', views.submit_incomes, name='submit_income'),
]
