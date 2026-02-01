from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ShortenedURL
from django.utils import timezone
import datetime

class URLShortenerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()
        self.client.login(username='testuser', password='password123')

    def test_url_shortening(self):
        long_url = "https://www.google.com"
        response = self.client.post(reverse('create_url'), {'long_url': long_url})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ShortenedURL.objects.count(), 1)
        url_obj = ShortenedURL.objects.first()
        self.assertEqual(url_obj.long_url, long_url)

    def test_redirection(self):
        url_obj = ShortenedURL.objects.create(
            user=self.user,
            long_url="https://www.github.com",
            short_code="githb"
        )
        response = self.client.get(reverse('redirect_url', args=[url_obj.short_code]), follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url_obj.long_url)

    def test_click_tracking(self):
        url_obj = ShortenedURL.objects.create(
            user=self.user,
            long_url="https://www.github.com",
            short_code="githb2"
        )
        self.client.get(reverse('redirect_url', args=[url_obj.short_code]))
        url_obj.refresh_from_db()
        self.assertEqual(url_obj.clicks, 1)

    def test_custom_alias(self):
        custom_code = "mycustom"
        self.client.post(reverse('create_url'), {
            'long_url': "https://example.com",
            'custom_code': custom_code
        })
        self.assertTrue(ShortenedURL.objects.filter(short_code=custom_code).exists())
