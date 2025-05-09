from django.db import models
from account.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'category'  # 테이블 이름 category 지정
    def __str__(self):
        return self.name

class Province(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'province'  # 테이블 이름 category 지정
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'city'  # 테이블 이름 city 지정
    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'district'  # 원하는 테이블 이름 지정
    def __str__(self):
        return self.name

class Town(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'town'  # 원하는 테이블 이름 지정
    def __str__(self):
        return self.name

class Village(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'village'  # 원하는 테이블 이름 지정

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    jibun_address = models.CharField(max_length=255)
    road_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    weekday_hours = models.CharField(max_length=100, blank=True, null=True)
    weekend_hours = models.CharField(max_length=100, blank=True, null=True)
    free_parking = models.BooleanField(default=False)
    baby_chair = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)
    restaurant_image = models.ImageField("식당 이미지", upload_to="restaurant/thumbnails", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'restaurant'  # 원하는 테이블 이름 지정

    def __str__(self):
        return self.restaurant_name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 커스텀 User 모델과 연결
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')  # 식당과 연결
    rating = models.PositiveIntegerField(default=5)  # 별점 (1~5)
    comment = models.TextField()  # 리뷰 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간

    class Meta:
        db_table = 'review'  # 테이블 이름 지정
        ordering = ['-created_at']  # 최근 작성된 리뷰가 먼저 표시되도록 정렬

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.restaurant_name} - {self.rating}점"