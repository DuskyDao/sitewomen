from pyexpat import model
from tabnanny import verbose
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

    title = models.CharField(
        max_length=255, verbose_name="Заголовок"
    )  # название статьи
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="slug"
    )
    content = models.TextField(
        blank=True, verbose_name="Текст статьи"
    )  # текстовое поле, blank=True - можно не заполнять при создании
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания"
    )  # время создания
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения"
    )  # время обновления
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Статус",
    )
    cat = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="Ктегории",
    )  # связь для категорий
    tags = models.ManyToManyField(
        "TagPost", blank=True, related_name="tags", verbose_name="Теги"
    )  # связь для тегов
    husband = models.OneToOneField(
        "Husband",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wuman",
        verbose_name="Муж",
    )  # связь для мужей

    objects = models.Manager()  # возвращаем менеджер по умолчанию
    published = PublishedManager()  # наш кастомный менеджер

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Известные женщины"  # в единственном числе
        verbose_name_plural = "Известные женщины"  # в множественном

        ordering = ["-time_create"]  # указываем обратную сортировку по времени создания
        indexes = [models.Index(fields=["-time_create"])]

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Имя категории")
    slug = models.SlugField(
        max_length=254, unique=True, db_index=True, verbose_name="slug"
    )

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Имя тега")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="slug"
    )

    class Meta:
        verbose_name = "Теги"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse(
            "tag", kwargs={"tag_slug": self.slug}
        )  # "tag" маршрут с urls.py (name='tag') возвращает tag_slug c значением slug в данном случае из таблици TagPost


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name
