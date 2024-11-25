from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Question, Answer, Notification
from .serializers import QuestionSerializer, AnswerSerializer, NotificationSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Assign the logged-in user as the creator
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        question = self.get_object()
        question.views += 1  # Upvotes can also be tracked as engagement
        question.save()
        return Response({'message': 'Question upvoted successfully!'})

    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        question = self.get_object()
        question.views = max(0, question.views - 1)  # Ensure no negative views
        question.save()
        return Response({'message': 'Question downvoted successfully!'})

    @action(detail=False, methods=['get'])
    def search(self, request):
        # Custom logic for search by title or tag
        query = request.query_params.get('q', '')
        queryset = self.queryset.filter(title__icontains=query) | self.queryset.filter(tags__icontains=query)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all().order_by('-created_at')
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Assign the logged-in user as the creator
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        answer = self.get_object()
        answer.upvotes += 1
        answer.save()
        return Response({'message': 'Answer upvoted successfully!'})

    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        answer = self.get_object()
        answer.downvotes += 1
        answer.save()
        return Response({'message': 'Answer downvoted successfully!'})

    @action(detail=False, methods=['get'])
    def filter_by_question(self, request):
        question_id = request.query_params.get('question_id', None)
        if question_id:
            queryset = self.queryset.filter(question_id=question_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 'No question ID provided'}, status=status.HTTP_400_BAD_REQUEST)

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        notifications = self.get_queryset().filter(is_read=False)
        notifications.update(is_read=True)
        return Response({'message': 'All notifications marked as read.'})
