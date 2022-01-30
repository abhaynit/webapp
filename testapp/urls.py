from django.urls import path
from testapp import views

urlpatterns = [
    path('',views.register,name = 'registration'),
    path('signup/',views.advance_register, name='signup'),
    path('login/',views.user_login, name = 'login'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.user_profile, name='profile'),
    path('chpass',views.user_change_password,name = 'chpass'),
    path('forgot',views.forgot_password,name = 'forgot'),
    path('profile_update/',views.user_profile,name = 'profile_update'),
    path('userdetail/<int:id>',views.user_detail,name='userdetail'),
    path('dashboard/',views.user_dashboard,name = 'dashboard'),
    path('hello/',views.test,name = 'test',),
]
