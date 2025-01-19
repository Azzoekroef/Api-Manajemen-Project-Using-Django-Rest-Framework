from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Jabatan, LevelJabatan
from .forms import CustomUserCreationForm,CustomUserChangeForm
# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # Gunakan custom form untuk membuat pengguna
    # Jika Anda ingin menambahkan custom form juga untuk mengubah pengguna, Anda bisa menambahkan `form` di sini
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'salary', 'jabatan', 'phone_number', 'street_address', 'city', 'province')}),
        ('Additional Info', {'fields': ('image',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(CustomUser, CustomUserAdmin),

# admin.site.register(CustomUser),
admin.site.register(Jabatan),
admin.site.register(LevelJabatan),

