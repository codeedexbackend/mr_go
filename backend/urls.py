from django.urls import path
from backend import views 

urlpatterns =[
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('userprofile/<int:user_id>/', views.UserView.as_view(), name='user_profile'),
    path('userprofileedit/<int:pk>/', views.UserProfileEditView.as_view(), name='user_profile_edit_by_id'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('ContactUsView/', views.ContactUsView.as_view(), name='ContactUsView'),
    path('ShippingRegView/', views.ShippingRegView.as_view(), name='ShippingRegView'),
    path('ShippingReggetView/<int:user_id>/', views.ShippingReggetView.as_view(), name='ShippingReggetView'),
    path('ShippingRegEditView/<int:pk>/', views.ShippingRegEditView.as_view(), name='ShippingRegEditView'),

]