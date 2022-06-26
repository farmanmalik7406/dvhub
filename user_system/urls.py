from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user_system.views import Todos, Index

urlpatterns = [
    path('', Index.as_view()),
    path('todos/', Todos.as_view()),
    path('updateTodo/', Todos.as_view()),
    path('todo/<str:action>/<int:pk>', Todos.as_view()),
    path('accounts/login/', LoginView.as_view()),
    path('accounts/logout/', LogoutView.as_view()),
    path('user/<str:action>/', Index.as_view()),
    path('register_user/',Index.as_view()),
    path('sendotp/',Index.as_view()),
    path('verifyotp/',Index.as_view())

]
