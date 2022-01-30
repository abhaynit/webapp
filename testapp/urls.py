from django.urls import path
from testapp import views

urlpatterns = [
    path('dashboard/',views.dashboard,name = 'abhay'),
    path('register/',views.register,name = 'register'),
    path('',views.user_login,name = 'user_login'),
    path('logout/',views.user_logout,name = 'user_logout'),
    path('student_out/',views.student_out,name = 'student_out'),
    path('issued_pass/',views.already_issued_pass,name = 'isuued_pass'),
    path('inpass/<int:id>/',views.guard_submit,name = 'intime'),
    path('user_change_password/',views.user_change_password,name = 'user_change_password'),
]
