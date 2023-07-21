from django.urls import path
from .views import( UserRegisteration,UserAdding,QuizCreate,QuizList,UserList,User_DRU_Admin,
                           UserProfile,QuizFiltering,QuizonlyQuestion,QuizTaking,QuizResultsView,QuizAnalyticsView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh',TokenRefreshView.as_view(),name='token_refresh'),
    path('signup/',UserRegisteration.as_view(),name='sign_up'),
    path('useradd/',UserAdding.as_view(),name='admin_useradd'),
    path('userlist/',UserList.as_view(),name='user_list'),
    path('create/',QuizCreate.as_view(),name=' quiz_create'),
    path('quizview<int:quiz_id>/',QuizonlyQuestion.as_view(),name='quiz_question'),
    path('quiztaking<int:quiz_id>/',QuizTaking.as_view(),name='quiz_take'),
    path('filter/',QuizFiltering.as_view(),name='quiz_filter'),
    path('profile/',UserProfile.as_view(),name='user_profile'),
    path('list/',QuizList.as_view(),name='quiz_list'),
    path('edituser/<int:pk>/',User_DRU_Admin.as_view(),name='edit_user'),
    path('result/',QuizResultsView.as_view(),name='quiz_result'),
    path('analytics/',QuizAnalyticsView.as_view(),name='quiz_data'),
    

]