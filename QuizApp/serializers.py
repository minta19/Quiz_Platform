from rest_framework import serializers
from .models import CustomUser,Quiz,QuizAnswers,QuizQuestions,QuizResponse
from rest_framework.validators import UniqueValidator
from django.db.models import Avg,Max,Min,Count,Sum
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['email','username','password']
        extra_kwargs={'password':{'write_only':True}}

    def create(self, validated_data):
        user=CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
            
        )
        return user
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','username','email']
class UserEditSerializer(serializers.ModelSerializer):
     class Meta:
        model=CustomUser
        fields=['username','email']  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['username']
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuizAnswers
        fields=['options','answer','is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answers=AnswerSerializer(many=True)
    class Meta:
        model=QuizQuestions
        fields=['id','question','answers','score']

class QuizSerializer(serializers.ModelSerializer):
    questions=QuestionSerializer(many=True)
    class Meta:
        model=Quiz
        fields=['title','topic','difficulty_level','questions']
   
    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            score = question_data.pop('score')  
            question = QuizQuestions.objects.create(quiz_title=quiz, score=score, **question_data)  

            for answer_data in answers_data:
                QuizAnswers.objects.create(question=question, **answer_data)

        return quiz
    
class QuizListSerializer(serializers.ModelSerializer):
    created_by=UserSerializer(read_only=True)
    class Meta:
        model=Quiz
        fields=['id','title','created_by','date_created','topic','difficulty_level']

class UserProfileSerializer(serializers.ModelSerializer):
    created_quiz=QuizSerializer(many=True,read_only=True)
    score=QuestionSerializer(source='QuizQuestions.score',read_only=True)
    class Meta:
        model=CustomUser
        fields=['email','username','created_quiz','score']


class AnswerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuizAnswers
        fields=['options','answer']

class QuestiononlySerializer(serializers.ModelSerializer):
    answers=AnswerViewSerializer(many=True,read_only=True)
    class Meta:
        model=QuizQuestions
        fields=['id','question','answers','score']

class QuizDetailsSerializer(serializers.ModelSerializer):
    questions=QuestiononlySerializer(many=True,read_only=True)
    created_by=UserSerializer(read_only=True)

    class Meta:
        model=Quiz
        fields=['id','title','created_by','date_created','topic','difficulty_level','questions']

class QuizTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Quiz
        fields=['title']

class QuizResponseSerializer(serializers.ModelSerializer):
    quiz=QuizTitleSerializer(read_only=True)

    class Meta:
        model=QuizResponse
        fields=['id', 'quiz','total_score']


class QuizAnalyticsSerializer(serializers.Serializer):
    quiz_overview=serializers.SerializerMethodField()
    performance_metrics=serializers.SerializerMethodField()
    most_answered_question=serializers.SerializerMethodField()
    least_answered_question=serializers.SerializerMethodField()
    
    def get_quiz_overview(self,obj):
        
        total_quizes=Quiz.objects.count()
        number_of_quiz_takers=CustomUser.objects.filter(quiz_results__isnull=False).distinct().count()
        average_quiz_score=QuizResponse.objects.all().aggregate(Avg('total_score')).get('total_score__avg')

        
        return{
            "total_quizes":total_quizes,
            "number_of_quiz_takers":number_of_quiz_takers,
            "average_quiz_score":round(average_quiz_score,2)
        }
    
    def get_performance_metrics(self,obj):
        quizzes = Quiz.objects.all()

        quiz_metrics_dict = {}

        for quiz in quizzes:
            quiz_metrics = QuizResponse.objects.filter(quiz=quiz)
            average_score = quiz_metrics.aggregate(Avg('total_score')).get('total_score__avg')
            highest_score = quiz_metrics.aggregate(Max('total_score')).get('total_score__max')
            lowest_score = quiz_metrics.aggregate(Min('total_score')).get('total_score__min')
            number_of_times_taken = quiz_metrics.count()

            total_marks = quiz.questions.aggregate(total_marks=Sum('score'))['total_marks']
            passed_users = quiz_metrics.filter(total_score__gte=(0.4 * total_marks))
            number_of_passed_users = passed_users.count() 
            pass_percentage = (number_of_passed_users / number_of_times_taken) * 100 if number_of_times_taken > 0 else 0

            quiz_metrics_dict[quiz.title] = {
                "average_score": round(average_score,2),
                "highest_score": highest_score,
                "lowest_score": lowest_score,
                "number_of_times_taken": number_of_times_taken,
                "pass_percentage":round(pass_percentage,3)
            }

        return quiz_metrics_dict
           
    
    
    def get_most_answered_question(self, obj):
        quizzes = Quiz.objects.all()
        most_answered_questions = []

        for quiz in quizzes:
            most_answered_question = QuizQuestions.objects.filter(quiz_title=quiz).annotate(
                times_question_answered=Count('answers')
            ).order_by('-times_question_answered').first()

            if most_answered_question:
                most_answered_questions.append({
                    "quiz_title": quiz.title,
                    "question": most_answered_question.question
                })
        return most_answered_questions
    
    def get_least_answered_question(self, obj):
        quizzes = Quiz.objects.all()
        least_answered_questions = []

        for quiz in quizzes:
            least_answered_question = QuizQuestions.objects.filter(quiz_title=quiz).annotate(
                times_question_answered=Count('answers')
            ).order_by('times_question_answered').first()

            if least_answered_question:
                least_answered_questions.append({
                    "quiz_title": quiz.title,
                    "question": least_answered_question.question
                })
        return least_answered_questions
