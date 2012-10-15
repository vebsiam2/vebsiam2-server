from django.http import HttpResponse
from django.conf.urls import url, patterns

urlpatterns = patterns('',
  url(r'^hello$', 'api.user.hello', name='hello_user'),
)

def hello(request):
    return HttpResponse("Hello, World")
