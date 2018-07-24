import random
from functools import wraps
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def get_ticket():
    a = '1234567890qwertyuiopasdfghjklzxcvbnm'
    ticket = ''
    for i in range(30):
        ticket += random.choice(a)
    return ticket


def wapper(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.user.r_id == 1:
            return HttpResponseRedirect(reverse('ttsx:index'))
        return func(request, *args, *kwargs)

    return inner
