from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings

class Ad(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/у'),
    ]

    title = models.CharField("Заголовок", max_length=200)
    description = models.TextField("Описание")
    images = models.ImageField(default="no_image.png", upload_to='product_image')
    category = models.CharField("Категория", max_length=100)
    available = models.BooleanField(default=True)
    condition = models.CharField("Состояние", max_length=10, choices=CONDITION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]

    ad_sender = models.ForeignKey(Ad, related_name='sent_proposals', on_delete=models.CASCADE)
    ad_receiver = models.ForeignKey(Ad, related_name='received_proposals', on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(os.path.join(settings.MEDIA_ROOT, self.image.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.ad_sender} → {self.ad_receiver}"