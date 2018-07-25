import datetime

from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from user.models import User, UserTicket
from myApp.models import Category, Goods
from utils.func import get_ticket, wapper


@wapper
def index(request):
    if request.method == 'GET':
        goods_list = Goods.objects.all()
        num = request.GET.get('page_num', 1)
        paginator = Paginator(goods_list, 4)
        page = paginator.page(num)
        return render(request, 'admin/product_list.html', {'goods_list': page})


def login(request):
    if request.method == 'GET':
        return render(request, 'admin/login.html')

    if request.method == 'POST':
        username = request.POST.get('usernmae')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first
        if user and check_password(password, user.password):
            ticket = get_ticket()
            out_time = datetime.datetime.now() + datetime.timedelta(days=1)
            UserTicket.objects.create(ticket=ticket, user=user, out_time=out_time)
            res = ''
            if user.r_id == '1':
                res = HttpResponseRedirect(reverse('ttsx:index'))

            else:
                res = HttpResponseRedirect(reverse('admin:index'))
            res.set_cookie('ticket', ticket, expires=out_time)
            return res

@wapper
def product_detail(request):
    if request.method=='GET':
        c_list = Category.objects.all()
        ctx = {'c_list': c_list}
        return render(request, 'admin/product_detail.html', ctx)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        category_id = Category.objects.get(name=category).id
        popular = request.POST.get('popular')
        icon = request.FILES.get('icon')
        intro = request.POST.get('intro')
        specifics = request.POST.get('specifics')
        if not all([name, price, category_id, popular, icon, intro, specifics]):
            return render(request, 'admin/product_detail.html')
        Goods.objects.create(name=name, price=price, category_id=category_id,
                             Popularity=popular,
                             icon=icon, introducte=intro, specifics=specifics)
        return HttpResponseRedirect(reverse('admin:index'))


@wapper
def modify(request):
    if request.method == 'GET':
        goods_id = request.GET.get('goods_id')
        goods = Goods.objects.get(pk=goods_id)
        c_list = Category.objects.all()
        ctx = {'c_list': c_list, 'goods': goods}
        return render(request, 'admin/product_detail.html', ctx)

    if request.method == 'POST':
        goods_id = request.GET.get('goods_id')
        goods = Goods.objects.get(pk=goods_id)
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        category_id = Category.objects.get(name=category).id
        popular = request.POST.get('popular')
        icon = request.FILES.get('icon')
        intro = request.POST.get('intro')
        specifics = request.POST.get('specifics')
        if icon:
            goods.name = name
            goods.price = price
            goods.category_id = category_id
            goods.Popularity = popular
            goods.icon = icon
            goods.introducte = intro
            goods.specifics = specifics
            goods.save()
            return HttpResponseRedirect(reverse('admin:index'))
        goods.name = name
        goods.price = price
        goods.category_id = category_id
        goods.Popularity = popular
        goods.introducte = intro
        goods.specifics = specifics
        goods.save()
        return HttpResponseRedirect(reverse('admin:index'))

@wapper
def delete(request):
    if request.method == 'GET':
        goods_id = request.GET.get('goods_id')
        goods = Goods.objects.get(pk=goods_id)
        goods.delete()
        goods_list = Goods.objects.all()
        return render(request, 'admin/product_list.html', {'goods_list': goods_list})

@wapper
def addCategoty(request):
    if request.method == 'GET':
        return render(request, 'admin/add_category.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.FILES.get('icon')
        Category.objects.create(name=name, icon=icon)
        return HttpResponseRedirect(reverse('admin:addcategory'))