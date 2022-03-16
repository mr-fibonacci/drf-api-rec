from rest_framework import serializers
from .models import Profile
from posts.models import Post
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            # print(following)
            return following.id if following else None
        return None

    def get_posts_count(self, obj):
        posts_count = Post.objects.filter(owner=obj.owner).count()
        return posts_count
        

    def get_followers_count(self, obj):
        followers_count = Follower.objects.filter(followed=obj.owner).count()
        return followers_count
        

    def get_following_count(self, obj):
        following_count = Follower.objects.filter(owner=obj.owner).count()
        return following_count
        

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
        ]
