from django.conf.urls import url, patterns
from django.template.response import TemplateResponse
from django.http import HttpResponse

urlpatterns = patterns('',
  url(r'^login$', 'api.auth.login', name='get_LoginPage'),
)


def login(request):
    if(request.method == 'GET'):
        return TemplateResponse(request, 'login.html', {'next':None}) 
    return HttpResponse("Invalid login request", status=503)
