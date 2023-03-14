from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.

def submit_expenes(request):
    return render(request, 'home.html')

    print(request.POST)
    return JsonResponse({
        'status': 'oK',
    }, encoder=json.JSONEncoder)

    # return render(request, '2.html')