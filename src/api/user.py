from django.http import HttpResponse
from django.conf.urls import url, patterns
from django.utils import simplejson
from model.user import User
from django.template.response import TemplateResponse
import sys
import urllib2
import urllib

urlpatterns = patterns('',
  url(r'^create$', 'api.user.create', name='create_user'),
  url(r'^enable/(\d+)$', 'api.user.enable', name='enable_user'),
  url(r'^detail/([0-9a-f]+)$', 'api.user.detail', name='detail_user'),
  url(r'^fetch', 'api.user.fetch', name='fetch_user'),
  url(r'^register', 'api.user.register', name='register_user'),
)
RECAPTCHA_PRIVATE_KEY = '6LfNpNgSAAAAAEvMbbfkkzrRoXWBxmKW2hmeqWzF'
RECAPTCHA_VERIFY_URL = 'http://www.google.com/recaptcha/api/verify'

def create(request):
    '''
    if(request.method != 'POST'): 
        return HttpResponse("Invalid create request", status=503)
    json_data = simplejson.loads(request.raw_post_data)
    '''
    json_data = request.REQUEST  # Getting all the request parameters as json string
    print json_data 
    ' Check to see if all params have empty values'    
    jsondataempty=True
    for val in json_data.values():
        if val:
            jsondataempty=False
        
    if jsondataempty:
        ret = {
               'success':False,
               'id':'',
               'error':'All input fields are empty'
        }
    else:
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

def createfromjson(json_data):
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

    
def register(request):
    if(request.method != 'POST'):
        ''' Render the register.html template here ''' 
        return TemplateResponse(request, 'register.html')
        '''return HttpResponse("<html><h1>Self Registration Page- GET</h1></html>", status=200)
        '''
    ''' Captcha support '''
    recaptcha_post_data = [('privatekey',RECAPTCHA_PRIVATE_KEY),
                 ('challenge',request.POST.get("recaptcha_challenge_field", None)),
                 ('response',request.POST.get("recaptcha_response_field", None)),
                 ('remoteip',request.META.get("REMOTE_ADDR", None)),
                 ]     # a sequence of two element tupless
    recaptcha_result = urllib2.urlopen(RECAPTCHA_VERIFY_URL, urllib.urlencode(recaptcha_post_data))
    recaptcha_verify_content = recaptcha_result.read()
    print recaptcha_verify_content
    
    recaptcha_error=True
    if 'true' in recaptcha_verify_content:
        recaptcha_error=False
        
    
    if not recaptcha_error:        
        out=create(request)
        return  HttpResponse(out)
    else:
        ret = {
               'success': False,
               'id':'',
               'error':'Error in validating recaptcha response'}
        return HttpResponse(simplejson.dumps(ret),"application/json")
    