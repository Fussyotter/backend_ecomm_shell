import json

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import generics
from .serializers import UserSerializer

from .models import User


    # this is finally making sense to me.  the get_token function is a built in django function that returns a csrf token.  we are then setting the csrf token in the response header.  the response header is then sent back to the client.  the client then sets the csrf token in the cookie.  the csrf token is then sent back to the server in the header of the next request.  the server then checks the csrf token in the header against the csrf token in the cookie.  if they match, the request is allowed to continue.  if they don't match, the request is rejected.  this is how django protects against csrf attacks.
def get_csrf(request):
    response = JsonResponse({'Info': "Success - Set CSRF Cookie"})
    response['X-CSRFToken'] = get_token(request)
    return response

@require_POST
def loginView(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'Error': "Please provide both username and password"}, status=400)
    
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'Error': "Invalid Credentials"}, status=400)
    
    login(request, user)
    return JsonResponse({'Info': "Success - Logged In"})

class signupView(APIView):
    queryset = User.objects.all()

    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'Info': "Success - Created User"})
        return JsonResponse(serializer.errors, status=400)
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
