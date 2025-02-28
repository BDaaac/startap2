from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model

class Teacher(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=20)
    skill_level = models.CharField(
        max_length=20,
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')],
        default='Beginner'
    )
    directions = models.TextField()
    skills = models.TextField()
    experience = models.TextField()
    price = models.FloatField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.name



class ChatMessage(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"От {self.sender} к {self.receiver} в {self.timestamp:%Y-%m-%d %H:%M}"


class Ad(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('hidden', 'Скрыто'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Пополнение'),
        ('purchase', 'Покупка'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"


class ShopItem(models.Model):
    CATEGORY_CHOICES = [
        ('background', 'Фон'),
        ('pet', 'Питомец'),
    ]

    name = models.CharField(max_length=255)  # Название товара
    description = models.TextField(blank=True)  # Описание
    price = models.PositiveIntegerField()  # Цена в виртуальной валюте
    image = models.ImageField(upload_to='shop/', blank=True, null=True)  # Изображение товара
    available = models.BooleanField(default=True)  # Доступность товара
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='icon')  # Категория

    def __str__(self):
        return self.name

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.item.name}"
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    favorite_teachers = models.ManyToManyField('Teacher', blank=True, related_name='favorited_by')
    is_teacher = models.BooleanField(default=False)
    owned_items = models.ManyToManyField(ShopItem, blank=True, related_name="owners")  # Купленные вещи

    # Добавляем баланс
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Выбранные предметы кастомизации
    selected_background = models.ForeignKey(ShopItem, null=True, blank=True, on_delete=models.SET_NULL, related_name='selected_backgrounds')
    selected_frame = models.ForeignKey(ShopItem, null=True, blank=True, on_delete=models.SET_NULL, related_name='selected_frames')
    selected_icon = models.ForeignKey(ShopItem, null=True, blank=True, on_delete=models.SET_NULL, related_name='selected_icons')

    def __str__(self):
        return self.name or self.user.username

