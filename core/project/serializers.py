from rest_framework import serializers
from .models import Project, Status
from note.models import Note
from note.serializers import NoteSerializer
from project_handle.models import ProjectHandle
from django.db import transaction

class ProjectHandleSerializer(serializers.ModelSerializer):
    # peran = serializers.IntegerField()
    # customuser = serializers.IntegerField()


    # # def get_customuser(self, obj):
    # #     return obj.customer

    # def get_peran(self, obj):
    #     return obj.peran
    class Meta:
        model = ProjectHandle
        fields =  ('customuser', 'peran')

class ProjectSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    project_handler = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.status.name
    
    def get_project_handler(self, obj):
        project_handles = ProjectHandle.objects.filter(project=obj)
        project_handler_names = [{
            "name": f"{handle.customuser.first_name} {handle.customuser.last_name}",
            "peran": handle.peran.name
        } for handle in project_handles]
        return project_handler_names
    class Meta:
        model = Project
        fields = ('id', 'name', 'mulai', 'estimasi', 'modal', 'harga', 'desc', 'status', 'progres', 'project_handler')


class CreateProjectSerializer(serializers.ModelSerializer):
    project_handler = ProjectHandleSerializer(many=True, write_only=True)
    
    class Meta:
        model = Project
        fields = ('id', 'name', 'mulai', 'estimasi', 'modal', 'harga', 'desc', 'status', 'progres', 'project_handler')

    @transaction.atomic
    def create(self, validated_data):
        project_handlers_data = validated_data.pop('project_handler')
        print(project_handlers_data)
        project = Project.objects.create(**validated_data)
        for project_handler_data in project_handlers_data:
            customuser_id = project_handler_data.get('customuser')
            print(customuser_id)
            peran_id = project_handler_data.get('peran')
            ProjectHandle.objects.create(
                project=project,
                customuser=customuser_id,
                peran=peran_id)
        serializer = self.__class__(project)
        return project
    
class UpdateProjectSerializer(serializers.ModelSerializer):
    note = NoteSerializer
    penambahan_modal = serializers.IntegerField(write_only=True)
    catatan = serializers.CharField(write_only=True)
    class Meta:
        model = Project
        fields = ('id', 'name', 'penambahan_modal', 'status', 'progres', 'catatan')
        extra_kwargs = {
            'notees': {'write_only': True},  
        }       
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        penambahan_modal = validated_data.get('penambahan_modal', None)
        instance.status = validated_data.get('status', instance.status)
        instance.progres = validated_data.get('progres', instance.progres)   
        if penambahan_modal is not None:
            instance.modal += penambahan_modal
        instance.save()
        notes = validated_data.get('catatan')
        user_id = self.context['request'].user
        if notes:
            note_data = {
                'project': instance,
                'costumuser': user_id,
                'note': notes
            }
        print(note_data)
        Note.objects.create(**note_data)
        return instance



