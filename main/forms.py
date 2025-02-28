from django import forms
from .models import Teacher

class BecomeTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'phone', 'skill_level', 'directions', 'skills', 'experience', 'price', 'avatar']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'directions': forms.Textarea(attrs={'class': 'form-control custom-input'}),
            'skills': forms.Textarea(attrs={'class': 'form-control custom-input'}),
            'skill_level': forms.Select(choices=[
                ('Beginner', 'Beginner'),
                ('Intermediate', 'Intermediate'),
                ('Advanced', 'Advanced')
            ], attrs={'class': 'form-control custom-input'}),
            'experience': forms.Textarea(attrs={'class': 'form-control custom-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control custom-input'}),
            # Поле avatar будет обрабатываться отдельно
        }

from .models import Profile

from django import forms
from main.models import Profile

class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя'})
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'bio', 'name']  # Добавляем name

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Обновляем username в User
        profile.user.username = self.cleaned_data['name']
        profile.user.save()  # Сохраняем User

        if commit:
            profile.save()  # Сохраняем профиль

        return profile
from .models import Teacher

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['avatar', 'phone', 'skill_level', 'skills', 'directions', 'experience', 'price']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Введите номер телефона'}),
            'skill_level': forms.TextInput(attrs={'placeholder': 'Например: A2 или основы Python'}),
            'skills': forms.Textarea(attrs={'placeholder': 'Расскажите о ваших навыках', 'rows': 3}),
            'directions': forms.TextInput(attrs={'placeholder': 'Например: Программирование, Дизайн, Маркетинг'}),
            'experience': forms.Textarea(attrs={'placeholder': 'Опишите ваш опыт преподавания', 'rows': 4}),
            'price': forms.NumberInput(attrs={'placeholder': 'Цена в тенге'}),
        }

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=100,  # Минимальное пополнение
        label="Сумма пополнения (₸)"
    )
from django import forms
from .models import ShopItem

class ShopItemForm(forms.ModelForm):
    class Meta:
        model = ShopItem
        fields = ['name', 'description', 'price', 'image', 'available']  # Поля для формы
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название товара'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
