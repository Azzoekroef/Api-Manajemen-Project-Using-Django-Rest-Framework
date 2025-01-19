from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.hashers import make_password
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        required=False,  # Memungkinkan password kosong atau default
    )
    password2 = forms.CharField(
    label="Password confirm",
    strip=False,
    widget=forms.PasswordInput,
    required=False,  # Memungkinkan password kosong atau default
    )

    

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'first_name', 'last_name', 'email')  # Sesuaikan dengan field yang Anda inginkan

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")  # Dapatkan nilai password dari form
        if password:  # Jika ada nilai password yang dimasukkan
            user.password = make_password(password)  # Hash password sebelum disimpan
        else:  # Jika password kosong atau default
            default_password = "123456789"
            user.password = make_password(default_password)  # Set password tidak terpakai
        if commit:
            user.save()
        return user
    
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'image' , 'last_name', 'email', 'salary', 'jabatan', 'phone_number', 'street_address', 'city', 'province']