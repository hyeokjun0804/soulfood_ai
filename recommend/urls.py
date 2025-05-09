from django.urls import path
from recommend import views

app_name = "recommend"

urlpatterns = [
    path('recommend/', views.recommend_view, name='recommend_view'),  # 루트 URL에 대한 뷰 설정
    path('pop_restaurants/', views.load_restaurants, name='load_restaurants'),
    path('recom_customers/<str:model>/', views.load_customers, name='load_customers'),
]