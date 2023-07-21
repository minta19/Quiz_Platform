from django.shortcuts import get_object_or_404
from .models import CustomUser,Quiz,QuizQuestions,QuizAnswers,QuizResponse
from .serializers import (RegisterSerializer,QuizSerializer,QuizListSerializer,UserListSerializer,UserEditSerializer,
                          UserProfileSerializer,QuizDetailsSerializer,QuizResponseSerializer,QuizAnalyticsSerializer)
from rest_framework  import generics,status
from rest_framework.response import Response
from rest_framework .permissions import IsAdminUser,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from django.db.models import Sum

#signup
class UserRegisteration(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"MESSAGE":"USER CREATED "},status=status.HTTP_201_CREATED)
    
#Admin adding user   
class UserAdding(generics.CreateAPIView):
    permission_classes=[IsAdminUser,IsAuthenticated]
    serializer_class=RegisterSerializer
    authentication_classes=[JWTAuthentication]
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({"MESSAGE":"USER ADDED BY ADMIN  "},status=status.HTTP_201_CREATED)
    
#admin can view the list of users   
class UserList(generics.ListAPIView):
    permission_classes=[IsAdminUser,IsAuthenticated]
    serializer_class=UserListSerializer
    authentication_classes=[JWTAuthentication]
    queryset=CustomUser.objects.all()

#admin can retrieve,update & delete users
class User_DRU_Admin(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser,IsAuthenticated]
    serializer_class=UserEditSerializer
    authentication_classes=[JWTAuthentication]
    queryset=CustomUser.objects.all()
    def delete(self, request, *args, **kwargs):
        response= super().delete(request, *args, **kwargs)
        return Response({"MESSAGE":"USER DELETED"})
    
#quiz creation   
class QuizCreate(generics.CreateAPIView):
    serializer_class=QuizSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    queryset=Quiz.objects.all()
     
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        # request.data['created_by']=request.user.id
        response = super().post(request, *args, **kwargs)
        return Response({"MESSAGE":"QUIZ CREATED"})
    
# Quiz listing -list of available quizes   
class QuizList(generics.ListAPIView):
    serializer_class=QuizListSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    queryset=Quiz.objects.all()

# profile of the user
class UserProfile(generics.RetrieveAPIView):
    serializer_class=UserProfileSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get_object(self):
        return self.request.user

#filtering the quiz    
class QuizFiltering(generics.ListAPIView):
    serializer_class=QuizListSerializer
    filter_backends=(filters.DjangoFilterBackend,)
    filterset_fields=('topic', 'difficulty_level', 'date_created')
    queryset=Quiz.objects.all()
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

#retrieving only questions  of quiz with ans options
class QuizonlyQuestion(generics.RetrieveAPIView):
    def retrieve(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        serializer = QuizDetailsSerializer(quiz, context={'questions': questions})
        return Response(serializer.data)
    
#quiz taking   
class QuizTaking(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        serializer = QuizDetailsSerializer(quiz, context={'questions': questions})
        return Response(serializer.data)


    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()

        total_score = 0
        for question in questions:
            selected_option = request.data.get('answer_' + str(question.id))

            if selected_option:
                try:
                    answer = question.answers.get(options=selected_option, is_correct=True)
                    total_score += question.score
                except QuizAnswers.DoesNotExist:
                    pass
        user = request.user
        quiz_result = QuizResponse.objects.create(user=user, quiz=quiz, total_score=total_score)

        total_marks = questions.aggregate(total_marks=Sum('score'))['total_marks']

        pass_percentage = (total_score / total_marks) * 100 if total_marks > 0 else 0
        pass_mark_percentage = 40

        if pass_percentage >= pass_mark_percentage:
            message = "Congratulations! You passed the quiz."
        else:
            message = "Sorry, you did not pass the quiz."

        context = {
            "message": message,
            "total_score": total_score,
        }

        return Response(context, status=status.HTTP_200_OK)

#result
class QuizResultsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        quiz_results = QuizResponse.objects.filter(user=user)
        serializer = QuizResponseSerializer(quiz_results, many=True)
        return Response(serializer.data)
    
#Quiz Analytics
class QuizAnalyticsView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        quiz = Quiz.objects.first() 
        serializer=QuizAnalyticsSerializer(quiz,data={}, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)
    

