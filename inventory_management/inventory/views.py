from .models import Item
from .serializers import ItemSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from django.core.cache import cache
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger('api')

class CreateItemView(generics.CreateAPIView):
    serializer_class = ItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logger.info(f"User {request.user.username} is trying to create an item.")
        try:
            response = super().post(request, *args, **kwargs)
            logger.info(f"Item created successfully: {response.data}")
            return response
        except Exception as e:
            logger.error(f"Error creating item: {str(e)}")
            return Response({'detail': 'Error creating item.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RetrieveItemView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        logger.info(f"User {request.user.username} is trying to retrieve item with ID {item_id}.")
        cache_key = f'item_{item_id}'

        # Check Redis cache first
        cached_item = cache.get(cache_key)
        if cached_item:
            logger.info(f"Item {item_id} retrieved from cache.")
            return Response(cached_item, status=status.HTTP_200_OK)

        # If not in cache, retrieve from the database
        try:
            item = self.get_object()  # Fetch the item using the queryset
            serializer = self.get_serializer(item)
            # Store the retrieved item in the cache
            cache.set(cache_key, serializer.data, timeout=300)  # Cache for 5 minutes
            logger.info(f"Item {item_id} retrieved from database and cached.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            logger.warning(f"Item with ID {item_id} not found.")
            return Response({'detail': 'Oops sorry, item not found.'}, status=status.HTTP_404_NOT_FOUND)

class UpdateItemView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        logger.info(f"User {request.user.username} is trying to update item with ID {item_id}.")
        response = super().update(request, *args, **kwargs)  # Perform the update

        # Invalidate the cache for the updated item
        cache_key = f'item_{item_id}'
        cache.delete(cache_key)
        logger.info(f"Cache for item {item_id} invalidated after update.")

        return response

class DeleteItemView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete items

    def destroy(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        logger.info(f"User {request.user.username} is trying to delete item with ID {item_id}.")
        response = super().destroy(request, *args, **kwargs)
        logger.info(f"Item with ID {item_id} deleted successfully.")
        return response

class ListItemView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can list items

    def get(self, request, *args, **kwargs):
        logger.info(f"User {request.user.username} is trying to list items.")
        response = super().get(request, *args, **kwargs)
        logger.info("Items listed successfully.")
        return response

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"User registration initiated with username {request.data.get('username')}.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info("User registered successfully.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info(f"User {request.data.get('username')} is attempting to log in.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AccessToken.for_user(user)  # Create JWT token
        logger.info(f"User {request.data.get('username')} logged in successfully.")
        return Response({'token': str(token)}, status=status.HTTP_200_OK)