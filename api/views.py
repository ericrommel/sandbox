import re

from django.contrib.auth.models import User, Group
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.response import Response

from polls.models import Question, Choice
from .serializers import UserSerializer, GroupSerializer, QuestionSerializer, ChoiceSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """

    # Fix for TC `test_query_count_is_off`. Optimize the fetching
    queryset = Question.objects.prefetch_related('choice_set').all()

    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Fix for TC `test_multi_update`. Add PATCH to the HTTP methods allowed and its mapping to `partial_update`
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates one or more questions.
        `QuestionViewSet` inherits from `viewset.ModelViewSet`.
        This viewset, as per the code, provides default actions that are needed
        to handle the intentions.
        """
        if isinstance(request.data, list):
            updated_questions = []
            for item in request.data:
                question_id = self.extract_id_from_url(item['url'])
                question_instance = self.get_object_or_none(id=question_id)
                if question_instance:
                    serializer = self.get_serializer(question_instance, data=item, partial=True)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
                    updated_questions.append(serializer.data)
            return Response({"results": updated_questions}, status=status.HTTP_200_OK)
        else:
            return super(QuestionViewSet, self).partial_update(request, *args, **kwargs)

    def extract_id_from_url(self, url: str) -> int | None:
        """
        Extracts the question id from the given URL: `/api/questions/pk/`
        """
        match = re.search(r'/api/questions/(\d+)/$', url)
        if match:
            return int(match.group(1))
        return None

    def get_object_or_none(self, id: int) -> Question | None:
        """
        Gets the question instance with the given id
        """
        try:
            return Question.objects.get(pk=id)
        except Question.DoesNotExist:
            return None


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
