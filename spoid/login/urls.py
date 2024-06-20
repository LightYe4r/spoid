from django.urls import path
from .views import *

urlpatterns = [
    path('user-info/', CreateUser.as_view()),
]
