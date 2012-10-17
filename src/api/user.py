from django.http import HttpResponse
from django.conf.urls import url, patterns
from django.utils import simplejson
from model.user import User

urlpatterns = patterns('',
  url(r'^create$', 'api.user.create', name='create_user'),
)

def create(request):
    if(request.method != 'POST'): 
        return HttpResponse("Invalid create request", status=503)
    json_data = simplejson.loads(request.raw_post_data)
    u = User()
    for name in json_data: 
        u.name = json_data[name]
    u.save()
    return HttpResponse("Hello, World")
