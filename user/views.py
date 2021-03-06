import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

from myApp.models import Order, OrderGoodsModel
from user.models import User, UserTicket, UserAddress
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
        return HttpResponseRedirect(reverse('user:login'))


def logout(request):
    if request.method == 'GET':
        res = HttpResponseRedirect(reverse('user:login'))
        res.delete_cookie('ticket')
        return res


def mine(request):
    if request.method == 'GET':
        user = request.user
        ctx = {'user': user}
        return render(request, 'ttsx/user_center_info.html', ctx)


def address(request):
    if request.method == 'GET':
        user = request.user
        add = UserAddress.objects.filter(user=user).first()
        if add:
            ctx = {'add': add}
            return render(request, 'ttsx/user_center_site.html', ctx)
        else:
            return render(request, 'ttsx/user_center_site.html', )
    if request.method == 'POST':
        name = request.POST.get('name')
        addr = request.POST.get('address')
        tel = request.POST.get('tel')
        if not all([name, addr, tel]):
            user = request.user
            add = UserAddress.objects.get(user=user)
            ctx = {'add': add, 'msg': '请填写所有字段'}
            return render(request, 'ttsx/user_center_site.html', ctx)
        user_addr = UserAddress.objects.filter(user=request.user).first()
        if user_addr:
            user_addr.zcpde = name
            user_addr.addr = addr
            user_addr.tel = tel
            user_addr.save()
        else:
            UserAddress.objects.create(address=addr, tel=tel, zcpde=name, user=request.user)
        return HttpResponseRedirect(reverse('user:mine'))


def allOrder(request):
    if request.method == 'GET':
        user = request.user
        order_list = Order.objects.filter(user=user).all()
        num = request.GET.get('page_num', 1)
        paginator = Paginator(order_list, 2)
        page = paginator.page(num)
        return render(request, 'ttsx/user_center_order.html', {'order_list': page})
