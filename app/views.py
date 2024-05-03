from app.serializers import LoginSerializer, CloupeCreateSerializer, CoupleMessageSerializer, CoupleSpecialDateSerializer, CoupleWishListSerializer, CoupleImageSerializer
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .models import Cloupe, CoupleMessage, CoupleSpecialDate, CoupleWishList, CoupleImage

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CloupeCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = CloupeCreateSerializer(data=request.data)
        if serializer.is_valid():
            couple = serializer.save()
            return Response({'id': couple.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CoupleMessageCreateAPIView(generics.CreateAPIView):
    serializer_class = CoupleMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        cloupe = Cloupe.objects.filter(user1=user) | Cloupe.objects.filter(user2=user)
        if cloupe.exists():
            serializer.save(cloupe=cloupe.first(), creator=user)
        else:
            raise PermissionDenied({'error': 'No couple found'})
        
class CoupleMessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoupleMessage.objects.all()
    serializer_class = CoupleMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user != obj.creator:
            raise PermissionDenied({'error': 'Permission denied'})
        return obj
    
class CoupleSpecialDateCreateAPIView(generics.CreateAPIView):
    serializer_class = CoupleSpecialDateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        cloupe = Cloupe.objects.filter(user1=user) | Cloupe.objects.filter(user2=user)
        if cloupe.exists():
            serializer.save(cloupe=cloupe.first())
        else:
            raise PermissionDenied({'error': 'No couple found'})
        
class CoupleSpecialDateDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoupleSpecialDate.objects.all()
    serializer_class = CoupleSpecialDateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user != obj.cloupe.user1 and user != obj.cloupe.user2:
            raise PermissionDenied({'error': 'Permission denied'})
        return obj
    
class CoupleWishListCreateAPIView(generics.CreateAPIView):
    serializer_class = CoupleWishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        cloupe = Cloupe.objects.filter(user1=user) | Cloupe.objects.filter(user2=user)
        if cloupe.exists():
            serializer.save(cloupe=cloupe.first())
        else:
            raise PermissionDenied({'error': 'No couple found'})

class CoupleWishListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoupleWishList.objects.all()
    serializer_class = CoupleWishListSerializer

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user != obj.cloupe.user1 and user != obj.cloupe.user2:
            raise PermissionDenied({'error': 'Permission denied'})
        return obj
    

class CoupleImageCreateAPIView(generics.CreateAPIView):
    serializer_class = CoupleImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        cloupe = Cloupe.objects.filter(user1=user) | Cloupe.objects.filter(user2=user)
        if cloupe.exists():
            serializer.save(cloupe=cloupe.first())
        else:
            raise PermissionDenied({'error': 'No couple found'})

class CoupleImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoupleImage.objects.all()
    serializer_class = CoupleImageSerializer

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user != obj.cloupe.user1 and user != obj.cloupe.user2:
            raise PermissionDenied({'error': 'Permission denied'})
        return obj