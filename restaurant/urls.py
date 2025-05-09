from django.urls import path
from restaurant import views

app_name = 'restaurant'
urlpatterns = [
    path('restaurant/', views.restaurant_view, name='restaurant_view'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]