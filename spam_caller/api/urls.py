from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/', include('users.urls')),
    path('contact/', include('contacts.urls'))
]
