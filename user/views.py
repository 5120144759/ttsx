import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

from user.models import User, UserTicket
from utils.func import get_ticket


def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        pwd1 = request.POST.get('pwd')
        pwd2 = request.POST.get('cpwd')
        email = request.POST.get('email')
        if not all([username, pwd1, pwd2, email]):
            data = {'msg': '请填写所有字段'}
            return render(request, 'user/register.html', data)
        if pwd1 == pwd2:
            password = make_password(pwd1)
            User.objects.create(username=username, password=password, email=email)
            return HttpResponseRedirect(reverse('user:login'))
        data = {'msg': '两次输入的密码不同'}
        return render(request, 'user/register.html', data)


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = User.objects.filter(username=username).first()
        if user and check_password(pwd, user.password):
            ticket = get_ticket()
            out_time = datetime.datetime.now() + datetime.timedelta(days=1)
            UserTicket.objects.create(ticket=ticket, user=user, out_time=out_time)
            res = HttpResponseRedirect(reverse('ttsx:index'))
            res.set_cookie('ticket', ticket, expires=out_time)
            return res


def logout(request):
    if request.method == 'GET':
        res = HttpResponseRedirect(reverse('user:login'))
        res.delete_cookie('ticket')
        return res
