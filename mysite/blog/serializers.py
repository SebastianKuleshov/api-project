from rest_framework import serializers

from .models import Blog


class BlogSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()

    def create(self, validated_data):
        user = self.context["request"].user
        return Blog.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance

    def destroy(self, instance):
        instance.delete()
        return instance
