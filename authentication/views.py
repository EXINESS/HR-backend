from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .serializers import UserSerializer


class CreateUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if User.objects.filter(
                email=serializer.validated_data.get('email')
            ).first():
                return Response(
                    {'error': 'This email is already taken'},
                    status=status.HTTP_409_CONFLICT,
                )

            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                validate_password(password)
                user = User.objects.create_user(
                    email=email, password=password, is_active=False
                )

                return Response(
                    {'message': 'User created. Verification email sent'},
                    status=status.HTTP_200_OK,
                )

            except ValidationError as e:
                return Response(
                    {'error': 'Password is too weak', 'reason': e},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)