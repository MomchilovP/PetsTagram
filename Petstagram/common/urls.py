from django.urls import path

from Petstagram.common.views import LandingPage

urlpatterns = [
    path('', LandingPage.as_view(), name='index'),
]
