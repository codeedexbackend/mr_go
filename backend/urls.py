from django.urls import path
from backend import views 

urlpatterns =[
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),

]