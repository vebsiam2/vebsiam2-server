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
        # TODO: Add validation of attribute names and values 
        u.__dict__[name] = json_data[name]
    u.save()
    ret = {
       'success':True,
       'id':str(u._id)
    }
    return HttpResponse(simplejson.dumps(ret),"application/json")
