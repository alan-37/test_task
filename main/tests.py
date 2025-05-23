from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class AdTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.ad = Ad.objects.create(
            title="Книга",
            description="Описание книги",
            category="Книги",
            condition="new",
            user=self.user
        )

    def test_ad_creation(self):
        """Проверяет, что объявление корректно создаётся"""
        self.assertEqual(self.ad.title, "Книга")
        self.assertEqual(self.ad.user, self.user)

    def test_ad_edit_by_owner(self):
        """Автор может редактировать своё объявление"""
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('edit_ad', args=[self.ad.id]), {
            'title': 'Обновлённое название',
            'description': 'Новое описание',
            'category': 'Книги',
            'condition': 'used'
        })
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Обновлённое название')

    def test_ad_edit_by_other_user(self):
        """Другой пользователь не может редактировать чужое объявление"""
        self.client.login(username='otheruser', password='password')
        response = self.client.get(reverse('edit_ad', args=[self.ad.id]))
        self.assertEqual(response.status_code, 403)

    def test_ad_delete_by_owner(self):
        """Автор может удалить своё объявление"""
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('delete_ad', args=[self.ad.id]))
        self.assertEqual(Ad.objects.count(), 0)

    def test_ad_delete_by_other_user(self):
        """Другой пользователь не может удалить чужое объявление"""
        self.client.login(username='otheruser', password='password')
        response = self.client.post(reverse('delete_ad', args=[self.ad.id]))
        self.assertEqual(response.status_code, 403)

    def test_send_proposal(self):
        """Пользователь может отправить предложение обмена"""
        other_ad = Ad.objects.create(
            title="Телефон",
            description="Старый телефон",
            category="Электроника",
            condition="used",
            user=self.other_user
        )
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('send_proposal', args=[other_ad.id]), {
            'ad_sender': self.ad.id,
            'comment': 'Хочу обменять!'
        })
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_cant_propose_to_own_ad(self):
        """Нельзя предложить обмен на своё же объявление"""
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('send_proposal', args=[self.ad.id]), {
            'ad_sender': self.ad.id,
            'comment': 'Ошибка!'
        })
        self.assertEqual(ExchangeProposal.objects.count(), 0)

    def test_profile_view(self):
        """Профиль показывает мои объявления и предложения"""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Книга')
