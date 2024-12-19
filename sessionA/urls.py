from django.urls import path
from .views import SignupView, LoginView, HomeView, AddView, EditView, DeleteView, LogoutView

urlpatterns = [
    path('api/signup/', SignupView.as_view(), name='api_signup'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/home/', HomeView.as_view(), name='api_home'),
    path('api/add/', AddView.as_view(), name='api_add'),
    path('api/edit/<int:id>/', EditView.as_view(), name='api_edit'),
    path('api/delete/<int:id>/', DeleteView.as_view(), name='api_delete'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
]
