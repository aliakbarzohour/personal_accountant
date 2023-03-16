from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def submit_expenes(request):
    return render(request, 'home.html')

    print(request.POST)
    return JsonResponse({
        'status': 'oK',
    }, encoder=json.JSONEncoder)

    # return render(request, '2.html')