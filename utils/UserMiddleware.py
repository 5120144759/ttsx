import datetime
import re

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import reverse

from user.models import User, UserTicket


class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        paths = [r'^/user/login/$', r'^/user/register/$', r'^/$', r'^/myAdmin/login/$']

        for path in paths:
            if re.match(path, request.path):
                return None
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user = UserTicket.objects.filter().first()
            if user:
                if user.out_time.replace(tzinfo=None) < datetime.datetime.now():
                    user.delete()
                    return HttpResponseRedirect(reverse('user:login'))
                u = User.objects.filter(id=user.user_id).first()
                request.user = u
                return None
            else:
                return HttpResponseRedirect(reverse('user:login'))
        else:
            return HttpResponseRedirect(reverse('user:login'))
