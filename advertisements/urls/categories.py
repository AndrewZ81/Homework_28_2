from django.urls import path

from advertisements import views

urlpatterns = [
    path('', views.CategoryListView.as_view()),
    path('<int:pk>/', views.CategoryDetailView.as_view()),
    path('create/', views.CategoryCreateView.as_view()),
    path('<int:pk>/update/', views.CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', views.CategoryDeleteView.as_view()),
]