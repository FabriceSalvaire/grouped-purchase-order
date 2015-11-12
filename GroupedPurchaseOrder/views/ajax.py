####################################################################################################
#
# GroupedPurchaseOrder - A Django Application.
# Copyright (C) 2014 Fabrice Salvaire
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from django.views.decorators.http import require_POST

from django_ajax.decorators import ajax

####################################################################################################

_counter = 0

@ajax
def hello(request):
    global _counter
    _counter += 1
    return {'result': 'item {}'.format(_counter)}

# GET /ajax/hello HTTP/1.1
# Host: 127.0.0.1:8000
# User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0
# Accept: */*
# Accept-Language: fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3
# Accept-Encoding: gzip, deflate
# X-Requested-With: XMLHttpRequest
# Referer: http://127.0.0.1:8000/suppliers/
# Cookie: django_language=en; sessionid=wgpdfaqp1ld8qhoubpbh43xwmhayl2yi; csrftoken=xIF20ZHDFw9q18m03EJI19CPwIeWGLUM
# Connection: keep-alive
# -->
# HTTP/1.0 200 OK
# Date: Mon, 10 Nov 2014 22:06:34 GMT
# Server: WSGIServer/0.2 CPython/3.4.2
# Content-Type: application/json
# Vary: Cookie
# X-Frame-Options: SAMEORIGIN
# 
# {"content": {"result": "item 2"}, "status": 200, "statusText": "OK"}

@ajax
@require_POST
def bye(request):
    print(request.POST)
    return {'result': 'ok {}'.format(request.POST['foo'])}

# POST /ajax/bye HTTP/1.1
# Host: 127.0.0.1:8000
# User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0
# Accept: */*
# Accept-Language: fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3
# Accept-Encoding: gzip, deflate
# Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# X-CSRFToken: xIF20ZHDFw9q18m03EJI19CPwIeWGLUM
# X-Requested-With: XMLHttpRequest
# Referer: http://127.0.0.1:8000/suppliers/
# Content-Length: 7
# Cookie: django_language=en; sessionid=wgpdfaqp1ld8qhoubpbh43xwmhayl2yi; csrftoken=xIF20ZHDFw9q18m03EJI19CPwIeWGLUM
# Connection: keep-alive
# Pragma: no-cache
# Cache-Control: no-cache
#
# foo=bar
# -->
# HTTP/1.0 200 OK
# Date: Mon, 10 Nov 2014 22:20:43 GMT
# Server: WSGIServer/0.2 CPython/3.4.2
# X-Frame-Options: SAMEORIGIN
# Vary: Cookie
# Content-Type: application/json
# 
# {"content": {"result": "ok bar"}, "status": 200, "statusText": "OK"}

# {% block head %}
# <script type="text/javascript" src="{% static 'GroupedPurchaseOrder/js/jquery-v1.11.1.min.js' %}"></script>
# <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax.js' %}"></script>
# <script type="text/javascript">
#  function hello_callback()
#  {
#    ajaxGet('/ajax/hello', function(content)
# 	   {
# 	     //onSuccess
# 	     // alert(content.result);
# 	     $("ul#foo").append("<li>" + content.result + "</li>"); 
# 	   })
#  }
#  function bye_callback()
#  {
#    ajaxPost('/ajax/bye', {'foo': 'bar'}, function(content)
# 	   {
# 	     //onSuccess
# 	     // alert(content.result);
# 	     $("ul#foo li:last").remove(); 
# 	     $("ul#foo li:last").append(' ' + content.result); 
# 	   })
#  }
# </script>
# {% endblock %}
# 
# <ul id="foo">
# </ul>
# <button class="btn btn-xs" onclick="hello_callback()">{% trans "hello" %}</button>
# <button class="btn btn-xs btn-danger" onclick="bye_callback()">{% trans "bye" %}</button>

####################################################################################################
# 
# End
# 
####################################################################################################
