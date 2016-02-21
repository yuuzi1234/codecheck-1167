from rest_framework import serializers
from .models import Projects


class ProjectsSerializer(serializers.ModelSerializer):
    url = serializers.CharField(allow_null=True, max_length=255,
                                required=False)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(
        style={'base_template': 'textarea.html'})

    class Meta:
        model = Projects
        fields = ('id', 'url', 'title', 'description', 'created_at')

    def create(self, validated_data):
        """
        POST /api/projects
        """
        return Projects.objects.create(**validated_data)
