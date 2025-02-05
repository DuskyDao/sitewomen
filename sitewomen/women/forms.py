from django import forms
from .models import Category, Husband


# fmt: off
class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))  # текстовое поле, class: form-input для css
    slug = forms.SlugField(max_length=255, label="URL")  #  слаг
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")  # большое текстовое поле 50столбцов и 5строк
    is_published = forms.BooleanField(required=False, label="Статус", initial=True)  # чекер
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории", empty_label="Категория не выбрана")  # раскрівающееся меню с данными из таблиц
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label="Муж", empty_label="Не замужем")  #
