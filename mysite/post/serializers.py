from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    
    def destroy(self, instance):
        instance.delete()
        return instance

# class PostSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     def update(self, instance, validated_data):
#         validated_data.pop('user')
#         return super().update(instance, validated_data)
    
#     class Meta:
#         model = Post
#         fields = '__all__'