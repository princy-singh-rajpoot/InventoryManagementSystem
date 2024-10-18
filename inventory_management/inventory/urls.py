from django.urls import path
from .views import UserRegistrationView, UserLoginView
from django.urls import path
from .views import (
    CreateItemView,
    RetrieveItemView,
    UpdateItemView,
    DeleteItemView,
    ListItemView,
)

urlpatterns = [
    # user creation
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),

    # products creation , retirieval, updation, and deletion.
    path('items/create/', CreateItemView.as_view(), name='item-create'),  # Create item
    path('items/', ListItemView.as_view(), name='item-list'),  # List all items
    path('items/<int:pk>/', RetrieveItemView.as_view(), name='item-detail'),  # Read item
    path('items/update/<int:pk>/', UpdateItemView.as_view(), name='item-update'), 
    path('items/delete/<int:pk>/', DeleteItemView.as_view(), name='item-delete'),  # Delete item
]
