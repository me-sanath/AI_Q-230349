from rest_framework import serializers
from .models import Question, Answer, Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']

class AnswerSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Answer
        fields = ['id', 'question', 'content', 'created_at', 'updated_at', 'created_by', 
                  'created_by_username', 'upvotes', 'downvotes']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'tags', 'created_at', 'updated_at', 'created_by', 
                  'created_by_username', 'answers', 'is_approved', 'views']
