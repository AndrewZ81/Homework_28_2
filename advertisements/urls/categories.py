from django.urls import path

from advertisements import views

urlpatterns = [
    path('', views.CategoryView.as_view()),
    path('<int:pk>/', views.CategoryDetailView.as_view()),
]