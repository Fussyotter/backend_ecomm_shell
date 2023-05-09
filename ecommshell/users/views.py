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

    # Return the user details along with the CSRF cookie
    response = JsonResponse({'Info': "Success - Logged In"})
    response['X-CSRFToken'] = get_token(request)
    response['user'] = {'id': user.id, 'username': user.username}
    return response

class signupView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            email = serializer.validated_data.get('email')
            first_name = serializer.validated_data.get('first_name', '')
            last_name = serializer.validated_data.get('last_name', '')
            User.objects.create_user(username=username, password=password, email=email,
                                     first_name=first_name, last_name=last_name)
            return Response({'Info': "Success - Created User"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
