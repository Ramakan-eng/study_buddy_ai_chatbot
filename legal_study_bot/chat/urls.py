from django.urls import path

from .views import ask_case




urlpatterns = [
    path("ask/question/", ask_case, name="ask_case"),
]