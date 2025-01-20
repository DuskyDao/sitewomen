from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


# Create your models here.
class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255)  # название статьи
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    content = models.TextField(
        blank=True
    )  # текстовое поле, blank=True - можно не заполнять при создании
    time_create = models.DateTimeField(auto_now_add=True)  # время создания
    time_update = models.DateTimeField(auto_now=True)  # время обновления
    is_published = models.BooleanField(
        choices=Status.choices, default=Status.PUBLISHED
    )  # по умолчанию - опубликовано

    objects = models.Manager()  # возвращаем менеджер по умолчанию
    published = PublishedManager()  # наш кастомный менеджер

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-time_create"]  # указываем обратную сортировку по времени создания
        indexes = [models.Index(fields=["-time_create"])]

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})
