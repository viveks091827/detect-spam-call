from django.urls import path
from .views import Register, Login, ListUser, ListProfile

urlpatterns=[
	path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('user', ListUser.as_view(), name='list_users'),
    path('profile/', ListProfile.as_view(), name='list_profiles')
]