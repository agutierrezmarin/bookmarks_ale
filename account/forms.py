from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repite la contraseña", widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Las contrasenias no son iguales")
        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=data).exists():
            raise forms.ValidationError("Este email ya esta en uso.")
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = get_user_model().objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Este Email ya esta en uso.")
        return data


class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label="Fecha de nacimiento",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d"],
    )

    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]
