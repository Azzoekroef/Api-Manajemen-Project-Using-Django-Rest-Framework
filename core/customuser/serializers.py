from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser, Jabatan,LevelJabatan
from django.conf import settings

class JabatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jabatan
        fields = ['id', 'name']

class LevelJabatanSerializers(serializers.ModelSerializer):
    class Meta:
        model = LevelJabatan
        fields = ['id', 'name']

class CustomUserSerializer(serializers.ModelSerializer):
    jabatan = JabatanSerializer()
    fullname = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        base_url = settings.BASE_URL  # Gantilah ini dengan variabel yang sesuai dengan URL dasar aplikasi Anda
        image_url = obj.image.url if obj.image else None

        if image_url:
            return f"{base_url}{image_url}"
        else:
            return None

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name','last_name', 'fullname', 'image', "qoute",  'email', 'password', 'salary', 'jabatan', 'phone_number', 'street_address', 'city', 'province']
        extra_kwargs = {
            'password': {'write_only': True}, 
        }
    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    

class UpdateCustomUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name','last_name', 'fullname', 'image', "qoute",  'email', 'password', 'salary', 'jabatan', 'phone_number', 'street_address', 'city', 'province']
        extra_kwargs = {
            'password': {'write_only': True}, 
        }
    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"




class CreateUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id' ,'username', 'mulai_bekerja', 'jabatan', 'level_jabatan']
        extra_kwargs = {
            'password': {'write_only': True},  
        }
    def update(self, instance, validated_data):
        instance.mulai_kerja = validated_data.get('mulai_kerja', instance.mulai_kerja)
        instance.email = validated_data.get('email', instance.email)

class UpdateUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id' ,'username', 'mulai_bekerja', 'jabatan', 'level_jabatan', 'salary']
        extra_kwargs = {
            'password': {'write_only': True},  
        }
    def update(self, instance, validated_data):
        jabatan = validated_data.get('jabatan',None)
        if jabatan is not None:
            jabatan_id = jabatan.id
            try:
                jabatan_instance = Jabatan.objects.get(id=jabatan_id)
                instance.jabatan = jabatan_instance
            except Jabatan.DoesNotExist:
                pass
        level_jabatan = validated_data.get('level_jabatan')
        if level_jabatan is not None:
            level_jabatan_id = level_jabatan.id
            try:
                level_jabatan_instance = LevelJabatan.objects.get(id=level_jabatan_id)
                instance.level_jabatan = level_jabatan_instance
            except Jabatan.DoesNotExist:
                pass
        instance.username = validated_data.get('username', instance.username)
        instance.mulai_bekerja = validated_data.get('mulai_bekerja', instance.mulai_bekerja)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.save()
        return instance