from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token

def get_csrf(request):
    response = JsonResponse({'Info': "Success - Set CSRF Cookie"})
    # this is finally making sense to me.  the get_token function is a built in django function that returns a csrf token.  we are then setting the csrf token in the response header.  the response header is then sent back to the client.  the client then sets the csrf token in the cookie.  the csrf token is then sent back to the server in the header of the next request.  the server then checks the csrf token in the header against the csrf token in the cookie.  if they match, the request is allowed to continue.  if they don't match, the request is rejected.  this is how django protects against csrf attacks.
    response['X-CSRFToken'] = get_token(request)
    return response