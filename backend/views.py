from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from backend.models import User, Token, Expense, Income


# Create your views here.

def Home(request):
    return render(request, 'home.html')


# Expenses price view
@csrf_exempt
def submit_expenes(request):
    """ Submit an expense """

    # TODO; validate data user might be fake . amount might be fake , token might be fake ...
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()

    Expense.objects.create(user=this_user, amount=request.POST['amount'],
                           text=request.POST['text'], date=date)

    return JsonResponse({
        'status': 'OK',
    }, encoder=json.JSONEncoder)



# Incomes Price view
@csrf_exempt
def submit_incomes(request):
    """ Submit an expense """

    # TODO; validate data user might be fake . amount might be fake , token might be fake ...
    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()

    Income.objects.create(user=this_user, amount=request.POST['amount'],
                          text=request.POST['text'], date=date)

    return JsonResponse({
        'status': 'OK',
    }, encoder=json.JSONEncoder)
