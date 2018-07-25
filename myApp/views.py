from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myApp.models import Goods, Category, MainWheel, MainNav


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
        ctx = {'goods_list': page, 'c_list': c_list, 'cid': cid}
        return render(request, 'ttsx/list.html', ctx)
