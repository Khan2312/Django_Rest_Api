from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(username='user', password='password'):
    """Create a sample user"""
    return get_user_model().objects.create_user(
        username=username, password=password)


class ModelTests(TestCase):

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        username = 'user'
        password = 'password'
        user = get_user_model().objects.create_superuser(
            username=username, password=password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password(password))

    def test_create_user_successful(self):
        """Test creating a new user is successful"""
        username = 'user'
        password = 'password'
        user = sample_user()
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_delete_user_successful(self):
        """Test deleting a user is successful"""
        test_user = sample_user()
        user_to_delete = get_user_model().objects.get(
            username=test_user.username)
        user_exists = get_user_model().objects.filter(
            username=test_user.username).exists()
        self.assertTrue(user_exists)
        user_to_delete.delete()
        user_exists = get_user_model().objects.filter(
            username=test_user.username).exists()
        self.assertFalse(user_exists)

    def test_content_str(self):
        """Test the content string representation"""
        content = models.Content.objects.create(
            x=1,
            y=2
        )
        self.assertEqual(str(content), str(content.id))
