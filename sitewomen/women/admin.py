from turtle import title
from django.contrib import admin, messages
from .models import Category, TagPost, Women


class MariedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [("married", "Замужем"), ("single", "Не замужем")]

    def queryset(self, request, queryset):
        # return queryset
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        elif self.value() == "single":
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    # readonly_fields = ["slug"]
    filter_horizontal = ["tags"]
    list_display = (
        "title",
        "time_create",
        "is_published",
        "cat",
        "brief_info",
    )
    list_display_links = ("title",)
    ordering = ["-time_create", "title"]
    list_editable = ("is_published",)
    list_per_page = 5
    actions = ["set_published", "set_draft"]
    search_fields = ["title__startswith", "cat__name"]
    list_filter = [MariedFilter, "cat__name", "is_published"]

    @admin.display(description="Количество символов", ordering="content")
    def brief_info(self, women: Women):
        return f"Описание: {len(women.content)} символов"

    @admin.action(description="Опубликовать выбранные")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(
            request, f"Снято с публикации {count} записей.", messages.WARNING
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_display_links = ("id", "name")


@admin.register(TagPost)
class TagsPostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
    )
    list_display_links = ("id", "tag")
