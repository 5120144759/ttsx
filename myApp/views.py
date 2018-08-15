from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

from myApp.models import Goods, Category, MainWheel, MainNav, \
    Cart, Order, OrderGoodsModel
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
    ctx = {'goods_list': goods_list, 'c_list': c_list,
           'w_list': w_list, 'm_list': m_list}
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
        ctx = {'goods': goods, 'c_list': c_list, 'cid': int(cid),
               'goods_list': goods_list}
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
            cart = Cart.objects.filter(goods_id=goods_id,
                                       user_id=user.id).first()
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
            cart = Cart.objects.filter(goods_id=goods_id,
                                       user_id=user.id).first()
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
        num = 0
        for cart in carts_list:
            num += cart.c_num
        return render(request, 'ttsx/cart.html',
                      {'carts_list': carts_list, 'num': num})


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


def change(request):
    if request.method == 'POST':
        id = request.POST.get('cart_id')
        cart = Cart.objects.get(pk=id)
        cart.is_select = not cart.is_select
        cart.save()
        return JsonResponse({'code': 200, 'is_select': cart.is_select})


def getPrice(request):
    if request.method == 'GET':
        user = request.user
        carts = Cart.objects.filter(user=user, is_select=True)
        count_price = 0
        if carts:
            for cart in carts:
                count_price += cart.goods.price * cart.c_num
        count_price = round(count_price, 3)
        return JsonResponse({'count_price': count_price, 'code': 200})


def placeOrder(request):
    if request.method == 'GET':
        user = request.user
        add = UserAddress.objects.get(user=user)
        carts_list = Cart.objects.filter(is_select=1)
        o_num = 0
        o_price = 0
        for cart in carts_list:
            o_num += cart.c_num
            o_price += cart.c_num * cart.goods.price
        if o_num == 0:
            return HttpResponseRedirect(reverse('ttsx:index'))
        order = Order(user=user, o_num=o_num, o_status=1, o_price=o_price)
        order.save()
        for cart in carts_list:
            OrderGoodsModel.objects.create(goods_id=cart.goods_id,
                                           goods_num=cart.c_num,
                                           order_id=order.id)
            cart.delete()
        order_goods_list = OrderGoodsModel.objects.filter(order_id=order.id)
        ctx = {'user': user, 'add': add,
               'order_goods_list': order_goods_list,
               'order': order}
        return render(request, 'ttsx/place_order.html', ctx)

def pay(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(pk=order_id)
    order.o_status = 2
    return HttpResponseRedirect(reverse('user:all_order'))


def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('search')
        if keyword:
            goods_list = Goods.objects.filter(Q(name__icontains=keyword)).all()
            num = request.GET.get('page_num', 1)
            paginator = Paginator(goods_list, 20)
            page = paginator.page(num)
            ctx = {
                'cid': 0,
                'gid': 0,
                'goods_list': page
            }
            return render(request, 'ttsx/list.html', ctx)

def my_order(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        user = request.user
        add = UserAddress.objects.get(user=user)
        order_goods_list = OrderGoodsModel.objects.filter(order_id=order_id)
        order = Order.objects.get(pk=order_id)
        ctx = {'user': user, 'add': add,
               'order_goods_list': order_goods_list,
               'order': order}
        return render(request, 'ttsx/place_order.html', ctx)
