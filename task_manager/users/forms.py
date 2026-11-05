from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
        ]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
        }


class UpdateForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")
        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Введенные пароли не совпадают")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user
