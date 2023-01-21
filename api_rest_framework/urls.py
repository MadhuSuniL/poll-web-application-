from django.urls import path
from .views import *

urlpatterns = [
    path('login',LoginApi.as_view()),
    path('register',RegisterApi.as_view()),
    path('poll',PollApi.as_view()),
    path('poll_detail/<id>',PollDetails.as_view()),
    path('delete_old_poll',Delete24Api.as_view()),
]