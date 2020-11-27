from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Content
from myapi.serializers import ContentSerializer

CONTENT_URL = reverse('content:content-list')
DOCS_URL = reverse('api-docs:docs-index')


def sample_content(x=2, y=3):
    return Content.objects.create(
        x=2, y=3)


class PublicContentApiTests(TestCase):
    """Test the public available Content API"""

    def setUp(self):
        self.client = APIClient()
        self.content = sample_content()

    def test_get_content_success(self):
        """Test that can get content"""
        res = self.client.get(CONTENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = ContentSerializer(self.content)
        self.assertIn(serializer.data, res.data)

    def test_get_content_filter_success(self):
        """Test that can get content with filter"""
        the_content = sample_content()
        params = {
            'id': self.content.id
        }
        res = self.client.get(CONTENT_URL, params)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer1 = ContentSerializer(self.content)
        serializer2 = ContentSerializer(the_content)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_content_submit_success(self):
        """Test that Content submit successful with right inputs"""
        payload = {
            'x': 2,
            'y': 3
        }
        res = self.client.post(CONTENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Content.objects.filter(
            id=res.data['id']
        ).exists()
        self.assertTrue(exists)
        result = self.client.get(CONTENT_URL, {
            'id': res.data['id']})
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        the_content = Content.objects.get(id=res.data['id'])
        serializer = ContentSerializer(the_content)
        self.assertIn(serializer.data, result.data)

    def test_content_submit_correct(self):
        """Test that output is right"""
        payload = {
            'x': 2,
            'y': 3
        }
        res = self.client.post(CONTENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Content.objects.filter(
            id=res.data['id']
        ).exists()
        self.assertTrue(exists)
        result = self.client.get(CONTENT_URL, {
            'id': res.data['id']})
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        the_content = Content.objects.get(id=res.data['id'])
        serializer = ContentSerializer(the_content)
        self.assertIn(serializer.data, result.data)
        self.assertEqual(payload['x']*payload['y'], result.data[0]['z'])

    def test_content_submit_invalid(self):
        """Test that Content submit missing inputs failed"""
        payload = {'x': ''}
        res = self.client.post(CONTENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_content_submit_invalid_input(self):
        """Test that Content submit for wrong input failed"""
        payload = {
            'x': 'test',
            'y': 2
        }
        res = self.client.post(CONTENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_content_delete_successful(self):
        """Test that Content delete successful with right inputs"""
        the_content = sample_content()
        res = self.client.delete(CONTENT_URL+"{}/".format(the_content.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = Content.objects.filter(id=the_content.id).exists()
        self.assertFalse(exists)
        params = {'id': the_content.id}
        result = self.client.get(CONTENT_URL, params)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual([], result.data)


class DocsApiTests(TestCase):
    """Test the API documentation"""

    def setUp(self):
        self.client = APIClient()
        creds = {
            'username': 'Joe',
            'password': 'pa$$word'
        }
        self.user = get_user_model().objects.create_user(**creds)
        creds['username'] = 'john'
        self.superuser = get_user_model().objects.create_superuser(**creds)

    def test_docs_public_successful(self):
        """Test that public cannot see docs"""
        res = self.client.get(DOCS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_docs_invalid_successful(self):
        """Test that user cannot see docs"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(DOCS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_docs_valid_successful(self):
        """Test that Admin can see docs"""
        self.client.force_authenticate(user=self.superuser)
        res = self.client.get(DOCS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
