from django.contrib import admin
from django.urls import path, include

from users import views
from users.views import logout_view

app_name = "main"

urlpatterns = [
    path("", views.index, name="homepage"),
    path('users/', include('users.urls', namespace="users")),
    path('admin/', admin.site.urls),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path('logout', logout_view, name="logout")

]
