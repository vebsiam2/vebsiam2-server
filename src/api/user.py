from django.http import HttpResponse
from django.conf.urls import url, patterns
from django.utils import simplejson
from model.user import User
import sys

urlpatterns = patterns('',
  url(r'^create$', 'api.user.create', name='create_user'),
  url(r'^enable/(\d+)$', 'api.user.enable', name='enable_user'),
  url(r'^detail/([0-9a-f]+)$', 'api.user.detail', name='detail_user'),
  url(r'^fetch', 'api.user.fetch', name='fetch_user'),
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

def enable(request,userid):
    u = User.find_by_id(userid)
    ret = {'success':False}
    if(u): 
        u.enable()
        ret['success'] = True
    else:
        ret["error"] = 'User is not found'
    return HttpResponse(simplejson.dumps(ret),"application/json")

def detail(request,userid):
    u = None
    err = None
    try:
        u = User.find_by_id(userid)
    except:
        err = sys.exc_info()[0]
    
    return user_details(u,err)

def user_details(u, err):
    ret = {'success':False}
    if(err):
        ret["error"] = err
    else:
        if(u): 
            data = u.__dict__.copy()
            data['_id'] = str(u._id)
            ret["data"] = data
        else:
            ret["data"]=None
        ret['success'] = True        
    return HttpResponse(simplejson.dumps(ret),"application/json")

def fetch(request):
    u = None
    err = None
    try:
        u = User.find_by_unique_field(request.GET.items()[0][0], request.GET.items()[0][1])
    except:
        err = sys.exc_info()[0]
    
    return user_details(u, err)

    