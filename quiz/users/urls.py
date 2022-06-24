from django.urls import path

from .views import index, savol_detail, logout_view, create_question, check_answer

app_name = "users"
urlpatterns = [
    path('', index, name="home"),
    path('savol-detail/<int:id>/', savol_detail, name="savol_detail"),
    path('logout', logout_view, name="logout"),
    path('create-question/', create_question, name="create_question"),
    path('check-answer/<int:id>/', check_answer, name="check_answer"),
   
]
