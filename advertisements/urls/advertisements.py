from django.urls import path

from advertisements import views

urlpatterns = [
    path('', views.AdvertisementView.as_view()),
    path('<int:pk>/', views.AdvertisementDetailView.as_view()),
]
