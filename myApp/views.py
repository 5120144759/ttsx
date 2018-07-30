from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from myApp.models import Goods, Category, MainWheel, MainNav, Cart
from user.models import UserAddress


def home(request):
    return HttpResponseRedirect(reverse('ttsx:index'))


def index(request):
    goods_list = []
    c_list = Category.objects.all()
    for i in range(1, len(c_list) + 1):
        if len(Goods.objects.filter(category_id=i)) > 3:
            goods_list1 = Goods.objects.filter(category_id=i)[:4]
        else:
            goods_list1 = Goods.objects.filter(category_id=i)
        goods_list += list(goods_list1)
    w_list = MainWheel.objects.all()
    m_list = MainNav.objects.all()
    ctx = {'goods_list': goods_list, 'c_list': c_list, 'w_list': w_list, 'm_list': m_list}
    return render(request, 'ttsx/index.html', ctx)


def show(request):
    if request.method == 'GET':
        cid = request.GET.get('cid')
        return HttpResponseRedirect(reverse('ttsx:more', kwargs={
            'cid': cid,
            'sid': '0'
        }))


def more(request, cid, sid):
    if request.method == 'GET':
        goods_list = Goods.objects.filter(category_id=cid)
        if cid == '0':
            goods_list = Goods.objects.all().order_by('-Popularity')

        c_list = Category.objects.all()
        if sid == '0':
            pass
        if sid == '1':
            goods_list = goods_list.order_by('-price')
        if sid == '2':
            goods_list = goods_list.order_by('-Popularity')
        num = request.GET.get('page_num', 1)
        paginator = Paginator(goods_list, 20)
        page = paginator.page(num)
        ctx = {'goods_list': page, 'c_list': c_list, 'cid': int(cid)}
        return render(request, 'ttsx/list.html', ctx)


def detail(request, gid, cid):
    if request.method == 'GET':
        goods = Goods.objects.get(pk=gid)
        goods_list = Goods.objects.filter(category_id=cid)
        c_list = Category.objects.all()
        ctx = {'goods': goods, 'c_list': c_list, 'cid': int(cid), 'goods_list': goods_list}
        return render(request, 'ttsx/detail.html', ctx)


def addCart(request):
    if request.method == 'POST':
        user = request.user
        ctx = {
            'code': 200,
            'msg': '添加成功'
        }
        sum = 0
        goods_id = request.POST.get('goods_id')
        if user.id:
            cart = Cart.objects.filter(goods_id=goods_id, user_id=user.id).first()
            if cart:
                cart.c_num += 1
                cart.save()
                carts = Cart.objects.filter(user=user)
                for c in carts:
                    sum += c.c_num
                ctx['sum'] = sum
            else:
                cart = Cart()
                cart.user = user
                cart.goods_id = goods_id
                cart.c_num = 1
                cart.save()
                carts = Cart.objects.filter(user=user)
                for c in carts:
                    sum += c.c_num
                ctx['sum'] = sum
            return JsonResponse(ctx)
    else:
        pass


def cartNum(request):
    if request.method == 'GET':
        user = request.user
        sum = 0
        carts = Cart.objects.filter(user=user)
        for c in carts:
            sum += c.c_num
        ctx = {'sum': sum}
        return JsonResponse(ctx)


def detailAddCart(request):
    if request.method == 'POST':
        user = request.user
        ctx = {
            'code': 200,
            'msg': '添加成功'
        }
        sum = 0
        goods_id = request.POST.get('goods_id')
        c_num = request.POST.get('num')
        if user.id:
            cart = Cart.objects.filter(goods_id=goods_id, user_id=user.id).first()
            if cart:
                cart.c_num += int(c_num)
                cart.save()
                carts = Cart.objects.filter(user=user)
                for c in carts:
                    sum += c.c_num
                ctx['sum'] = sum
            else:
                cart = Cart()
                cart.user = user
                cart.goods_id = goods_id
                cart.c_num = c_num
                cart.save()
                carts = Cart.objects.filter(user=user)
                for c in carts:
                    sum += c.c_num
                ctx['sum'] = sum
            return JsonResponse(ctx)


def cart(request):
    if request.method == 'GET':
        user = request.user
        carts_list = Cart.objects.filter(user=user)
        return render(request, 'ttsx/cart.html', {'carts_list': carts_list})

def addGoods(request):
    if request.method == 'POST':
        ctx = {
            'code': 200,
            'msg': '添加成功'
        }
        id = request.POST.get('cart_id')
        cart = Cart.objects.get(pk=id)
        cart.c_num += 1
        cart.save()
        ctx['c_num'] = cart.c_num
        ctx['price'] = cart.goods.price
        return JsonResponse(ctx)


def subGoods(request):
    ctx = {
        'code': 200,
        'msg': '减少成功'
    }
    id = request.POST.get('cart_id')
    cart = Cart.objects.get(pk=id)
    if cart.c_num == 1:
        cart.delete()
        ctx['code'] = 201
        return JsonResponse(ctx)
    cart.c_num -= 1
    cart.save()
    ctx['c_num'] = cart.c_num
    ctx['price'] = cart.goods.price
    return JsonResponse(ctx)

def delCart(request):
    if request.method == 'POST':
        ctx = {
            'code': 200,
            'msg': '删除成功'
        }
        id = request.POST.get('cart_id')
        cart = Cart.objects.get(pk=id)
        cart.delete()
        return JsonResponse(ctx)

