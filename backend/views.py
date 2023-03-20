# -*- coding: utf-8 -*-

from datetime import datetime
import string
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from backend.models import User, Token, Expense, Income, Passwordresetcodes
import random
from django.contrib.auth.hashers import make_password
import os
from postmark import PMMail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def random_str(N): return ''.join(random.SystemRandom().choice(
    string.ascii_uppercase + string.ascii_lowercase + string.digits))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def register(request):
    # form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
    if request.POST.__contains__('requestcode'):
        # duplicate email
        if User.objects.filter(email=request.POST['email']).exists():
            # TODO: forgot password
            context = {'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'}
            # TODO: keep the form data
            return render(request, 'register.html', context)

        # if user does not exists
        if not User.objects.filter(username=request.POST['username']).exists():
            code = random_str(28)
            now = datetime.now()
            email = request.POST['email']
            password = make_password(request.POST['password'])
            username = request.POST['username']
            temporarycode = Passwordresetcodes(
                email=email, time=now, code=code, username=username, password=password)
            temporarycode.save()
            message = PMMail(api_key=settings.POSTMARK_API_TOKEN,
                             subject="فعال سازی اکانت ",
                             sender="Aliakbar Zohour",
                             to=email,
                             # TODO: Build a server for deploy 
                             text_body="برای فعال سازی ایمیلی خود روی لینک روبرو کلیک کنید: https://???/accounts/register/?email={}&code={}".format(email, code),
                             tag="Create account")
            message.send()
            context = {
                'message': 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'}
            return render(request, 'login.html', context)
        else:
            # TODO: forgot password
            context = {
                'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه'}
            # TODO: keep the form data
            return render(request, 'register.html', context)
    elif request.GET.__contains__('code'):
        email = request.GET['email']
        code = request.GET['code']
        # if code is in temporary db, read the data and create the user
        if Passwordresetcodes.objects.filter(code=code).exists():
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password, email=email)
            this_token = random_str(48)
            token = Token.objects.create(user=newuser, token=this_token)
            # delete the temporary activation code from db
            Passwordresetcodes.objects.filter(code=code).delete()
            context = {'message': 'اکانت شما ساخته شد . توکن شما {} است . آن را دخیره کنید  چون دیگر نمایش داده نخواهد شد !'.format(this_token)}
            return render(request, 'login.html', context)
        else:
            context = {
                'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'login.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)


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
