from rest_framework import serializers

from blog.models import Post, Comment, Reaction


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    """

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """

    class Meta:
        model = Comment
        fields = '__all__'


class ReactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Reaction model.
    """

    class Meta:
        model = Reaction
        fields = '__all__'


class InputParamSerializer(serializers.Serializer):
    """
    Serializer for validating requests that accepts either a comment_id or post_id.
    """
    comment_id = serializers.IntegerField(required=False, allow_null=True)
    post_id = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        comment_id = data.get('comment_id')
        post_id = data.get('post_id')

        if not comment_id and not post_id:
            raise serializers.ValidationError('Either parent_id or post_id must be provided.')

        if comment_id and post_id:
            raise serializers.ValidationError('Both parent_id and post_id cannot be set at the same time.')

        return data


class ReactionInputParamSerializer(serializers.Serializer):
    """
        Serializer for validating requests that accepts either (a comment_id or post_id) and a reaction_type.
        """
    comment_id = serializers.IntegerField(required=False, allow_null=True)
    post_id = serializers.IntegerField(required=False, allow_null=True)
    reaction_type = serializers.CharField(required=True)

    def validate(self, data):
        comment_id = data.get('comment_id')
        post_id = data.get('post_id')
        reaction_type = data.get('reaction_type')

        if not comment_id and not post_id:
            raise serializers.ValidationError('Either parent_id or post_id must be provided.')

        if comment_id and post_id:
            raise serializers.ValidationError('Both parent_id and post_id cannot be set at the same time.')

        if not reaction_type or reaction_type not in ['like', 'dislike']:
            raise serializers.ValidationError('Reaction type must be set to either like or dislike.')

        return data
