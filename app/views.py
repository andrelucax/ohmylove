from app.serializers import LoginSerializer, CloupeCreateSerializer, CoupleMessageSerializer, CoupleSpecialDateSerializer, CoupleWishListSerializer, CoupleImageSerializer
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .models import Cloupe, CoupleMessage, CoupleSpecialDate, CoupleWishList, CoupleImage
from django.utils import timezone
import random
import boto3
from django.conf import settings

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
    
class CoupleSpecialDateListAPIView(generics.ListAPIView):
    queryset = CoupleSpecialDate.objects.all()
    serializer_class = CoupleSpecialDateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cloupe = get_user_cloupe(user)
        return CoupleSpecialDate.objects.filter(cloupe=cloupe)
    
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
    
class CoupleWishListListAPIView(generics.ListAPIView):
    queryset = CoupleWishList.objects.all()
    serializer_class = CoupleWishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cloupe = get_user_cloupe(user)
        return CoupleWishList.objects.filter(cloupe=cloupe, completed=False)

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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user != obj.cloupe.user1 and user != obj.cloupe.user2:
            raise PermissionDenied({'error': 'Permission denied'})
        return obj
    
class CoupleMessageOfTheDayAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        message = self.get_random_message(request.user)
        imageUrl = self.get_random_image(request.user)

        data = {
            'message': message,
            'image': imageUrl,
        }

        return Response(data)

    def get_random_message(self, user):
        couple = Cloupe.objects.filter(user1=user) | Cloupe.objects.filter(user2=user)
        if couple.exists():
            couple_messages = couple.first().messages.all().exclude(creator=user)
            if couple_messages.exists():
                random_message = random.choice(couple_messages)
                return CoupleMessageSerializer(random_message).data
        return None

    def get_random_image(self, user):
        couple = Cloupe.objects.filter(user1=user) | Cloupe.objects.filter(user2=user)
        if couple.exists():
            couple_images = couple.first().images.all()
            if couple_images.exists():
                random_image = random.choice(couple_images)
                image_url = ""
                if settings.DEBUG:
                    image_url = settings.SITE_URL + random_image.file.url
                else:
                    image_url = generate_presigned_url(random_image.file.name)
                return {
                    "url": image_url,
                    "name": random_image.name
                }
        return None
    
def generate_presigned_url(file_name):
    s3_client = boto3.client('s3',
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    response = s3_client.generate_presigned_url('get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': file_name
        },
        ExpiresIn=86400 # 1 day
    )

    return response

def get_user_cloupe(user):
    cloupe = Cloupe.objects.filter(user1=user) | Cloupe.objects.filter(user2=user)
    if cloupe.exists():
        return cloupe.first()
    else:
        raise PermissionDenied({'error': 'No couple found'})