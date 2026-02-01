from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random

class ShortenedURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')
    long_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=15, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.short_code} -> {self.long_url}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('redirect_url', kwargs={'short_code': self.short_code})

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    @classmethod
    def generate_unique_code(cls):
        length = 6
        characters = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choice(characters) for _ in range(length))
            if not cls.objects.filter(short_code=code).exists():
                return code

    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
