from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    def __str__(self) -> str:
        return self.username
    
class Quiz(models.Model):
    difficulty_choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    title=models.CharField(max_length=255,unique=True)
    topic=models.CharField(max_length=255)
    difficulty_level=models.CharField(choices=difficulty_choices,max_length=10)
    date_created=models.DateField(auto_now_add=True)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='created_quiz')

    def __str__(self) -> str:
         return self.title
    
class QuizQuestions(models.Model):
    quiz_title=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='questions')
    question=models.TextField()
    score=models.IntegerField(null=True,blank=True,default=0)
    
    def __str__(self) -> str:
        return self.question
    
class QuizAnswers(models.Model):
    choice_ans=[
        ('A', 'Choice A'),
        ('B', 'Choice B'),
        ('C', 'Choice C'),
    ]
    options=models.CharField(choices=choice_ans,max_length=20)
    answer=models.TextField()
    question=models.ForeignKey(QuizQuestions,on_delete=models.CASCADE,related_name='answers')
    is_correct=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.answer
    
class QuizResponse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name='quiz_responses')
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.quiz} - Total Score: {self.total_score}"