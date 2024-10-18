from inventory.models import Item
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class UserRegistrationLoginTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        url = reverse('user-registration')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        url = reverse('user-login')
        data = {
            'username': self.user.username,
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        print(response.data)  # Add this line to see the response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class ItemAPITests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_data)

        # Login to get the token
        login_url = reverse('user-login')
        response = self.client.post(login_url, {
            'username': self.user.username,
            'password': 'password123'
        }, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create an item with a unique name
        self.item_data = {
            'name': 'Unique Test Item',
            'description': 'Test description',
            'quantity': 10
        }
        self.client.post(reverse('item-create'), self.item_data, format='json')  # Create item
        self.created_item = Item.objects.first()  # Store the created item for use in tests

    def test_create_item(self):
        url = reverse('item-create')
        new_item_data = {
            'name': 'New Test Item',  # Use a different name
            'description': 'Test description',
            'quantity': 10
            }
        response = self.client.post(url, new_item_data, format='json')
        
        print(response.data)  # Print the response data to see validation errors
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)  # One already created in setUp
        self.assertEqual(Item.objects.last().name, 'New Test Item')

    
    def test_create_item_unauthenticated(self):
        self.client.credentials()  # Remove the token
        url = reverse('item-create')
        response = self.client.post(url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_item(self):
        url = reverse('item-detail', kwargs={'pk': self.created_item.id})  # Use the created item's ID
        response = self.client.get(url)
        
        # Update the expected name to match what was set in setUp
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Unique Test Item')  # Change this line

    def test_retrieve_item_not_found(self):
        url = reverse('item-detail', kwargs={'pk': 999})  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        update_url = reverse('item-update', kwargs={'pk': self.created_item.id})  # Use the created item's ID
        updated_data = {'name': 'Updated Item', 'description': 'Updated description', 'quantity': 20}
        response = self.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(id=self.created_item.id).name, 'Updated Item')

    def test_update_item_not_found(self):
        update_url = reverse('item-update', kwargs={'pk': 999})  # Non-existent ID
        updated_data = {'name': 'Updated Item', 'description': 'Updated description', 'quantity': 20}
        response = self.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item(self):
        delete_url = reverse('item-delete', kwargs={'pk': self.created_item.id})  # Use the created item's ID
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)  # Check that the item is deleted

    def test_delete_item_not_found(self):
        delete_url = reverse('item-delete', kwargs={'pk': 999})  # Non-existent ID
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
