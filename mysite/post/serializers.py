from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        validated_data.pop('user')
        return super().update(instance, validated_data)
    
    class Meta:
        model = Post
        fields = '__all__'