from django.shortcuts import render, get_object_or_404, redirect, reverse
from restaurant.models import Restaurant, Category, City, Province, Review
from django.db.models import Q
from django.core.paginator import Paginator
from restaurant.forms import ReviewForm
from django.http import HttpResponseForbidden

# 레스토랑 필터링 함수
def get_filtered_restaurants(query, category_filter, region_filter):
    restaurants = Restaurant.objects.all()  # 모든 레스토랑 데이터를 가져옵니다.

    # 검색어가 있으면 검색어를 포함하는 레스토랑만 필터링합니다.
    if query:
        restaurants = restaurants.filter(
            Q(restaurant_name__icontains=query) |  # 식당 이름에서 검색어 포함 여부 확인
            Q(road_address__icontains=query) |  # 도로 주소에서 검색어 포함 여부 확인
            Q(jibun_address__icontains=query) |  # 지번 주소에서 검색어 포함 여부 확인
            Q(category__name__icontains=query)  # 카테고리 이름에서 검색어 포함 여부 확인
        )

    # 카테고리 필터가 "All"이 아닌 경우만 필터링합니다.
    if category_filter and category_filter != "All":
        restaurants = restaurants.filter(category__name=category_filter)

    # 지역 필터가 "All"이 아닌 경우만 필터링합니다.
    if region_filter and region_filter != "All":
        restaurants = restaurants.filter(province__name=region_filter)

    return restaurants  # 필터링된 레스토랑을 반환합니다.


# 음식 종류 뷰
def restaurant_view(request):
    query = request.GET.get('q')  # 검색어
    category_filter = request.GET.get('category')  # 카테고리 필터
    region_filter = request.GET.get('region')  # 지역 필터

    # 필터링된 레스토랑을 가져옵니다.
    restaurants = get_filtered_restaurants(query, category_filter, region_filter)

    # 페이지네이터 설정 - 한 페이지에 20개의 레스토랑 표시
    paginator = Paginator(restaurants, 20)
    page_number = request.GET.get('page')  # 현재 페이지 번호
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 레스토랑 목록

    # 고유 카테고리와 지역 값 가져오기
    categories = Category.objects.values_list('name', flat=True).distinct()  # 카테고리 목록
    regions = Province.objects.values_list('name', flat=True).distinct()  # 지역 목록

    return render(request, 'restaurant/restaurant_list.html', {
        'page_obj': page_obj,  # 페이지네이션 객체
        'query': query,  # 검색어
        'category_filter': category_filter,  # 선택된 카테고리 필터
        'region_filter': region_filter,  # 선택된 지역 필터
        'categories': categories,  # 카테고리 목록
        'regions': regions,  # 지역 목록
    })



# 식당 상세 정보 뷰
def restaurant_detail(request, restaurant_id):
    # 식당 정보를 가져오기
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # 해당 식당의 리뷰 가져오기
    reviews = restaurant.reviews.all()

    # 리뷰 작성/수정 처리
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # 새 리뷰 작성
            review = form.save(commit=False)
            review.user = request.user
            review.restaurant = restaurant
            review.save()
            return redirect('restaurant:restaurant_detail', restaurant_id=restaurant_id)
    else:
        form = ReviewForm()

    return render(request, 'restaurant/restaurant_detail.html', {
        'restaurant': restaurant,
        'reviews': reviews,
        'form': form
    })


def edit_review(request, review_id):
    if not request.user.is_authenticated:
        # 인증되지 않은 경우 로그인 페이지로 리디렉션
        return redirect(reverse('account:login'))

    # 수정할 리뷰 가져오기
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('restaurant:restaurant_detail', restaurant_id=review.restaurant.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'restaurant/edit_review.html', {'form': form, 'review': review})


def delete_review(request, review_id):
    if not request.user.is_authenticated:
        # 인증되지 않은 경우 로그인 페이지로 리디렉션
        return redirect(reverse('account:login'))
    """
    리뷰 삭제 뷰.
    """
    review = get_object_or_404(Review, id=review_id)

    # 리뷰 작성자만 삭제 가능
    if review.user != request.user:
        return HttpResponseForbidden("리뷰를 삭제할 권한이 없습니다.")

    # 리뷰 삭제
    restaurant_id = review.restaurant.id  # 식당 ID 저장
    review.delete()

    # 리뷰 삭제 후 해당 식당의 상세 페이지로 리디렉션
    return redirect('restaurant:restaurant_detail', restaurant_id=restaurant_id)