from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.ContactCreateView.as_view()),
    path('list/', views.ContactListView.as_view()),
    path('set_spam/', views.ContactSetSpamView.as_view()),
    path('search/name/', views.ContactSearchByNameView.as_view()),
    path('search/number/', views.ContactSearchByMobileNumberView.as_view()),
    path('user/', views.ContactDisplayView.as_view())
]
