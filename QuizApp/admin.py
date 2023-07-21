from django.contrib import admin
from .models import CustomUser,Quiz,QuizQuestions,QuizAnswers,QuizResponse

admin.site.register(CustomUser)
admin.site.register(Quiz)
admin.site.register(QuizQuestions)
admin.site.register(QuizAnswers)
admin.site.register(QuizResponse)