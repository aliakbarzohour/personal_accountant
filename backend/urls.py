from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('', views.submit_expenes),
    re_path(r'^submit/expense/$', views.submit_expenes, name='submit_expense')
]
