import pandas as pd
from django.shortcuts import render, redirect, reverse
from recommend.dbCtrl import bring_dataframe_from_table
from restaurant.models import Restaurant
from django.db.models import Case, When
from django.template.loader import render_to_string
from django.http import JsonResponse


# 추천 페이지 뷰
def recommend_view(request):
    # 사용자가 인증된 상태라면 추천 페이지로 이동
    if request.user.is_authenticated:
        return render(request, 'recommend/recommend.html')
    # 인증되지 않았다면 로그인 페이지로 리디렉션
    return redirect(reverse("account:login"))


# 인기 식당 로드
def load_restaurants(request):
    # PostgreSQL에서 인기 식당 데이터를 가져오기
    pop_restaurants = bring_dataframe_from_table('popular_restaurants')
    # 평점 기준으로 상위 20개의 restaurant_id 추출
    pop_restaurants_ids = pop_restaurants.sort_values('mean').iloc[:20, 1].to_list()
    # Case를 사용하여 restaurant_id 순서를 유지하면서 정렬
    preserved_order = Case(*[When(id=restaurant_id, then=pos) for pos, restaurant_id in enumerate(pop_restaurants_ids)])
    # 추출된 restaurant_id에 해당하는 Restaurant 데이터를 가져와 순서대로 정렬
    pop_restaurants_data = Restaurant.objects.filter(id__in=pop_restaurants_ids).order_by(preserved_order)
    print(pop_restaurants_data)
    # 컨텍스트에 인기 식당 데이터를 전달
    context = {
        "restaurants": pop_restaurants_data
    }
    # 추천 식당 목록을 템플릿에 렌더링하여 HTML로 변환
    recommend_html = render_to_string("recommend/recommend_list.html", context)
    # 변환된 HTML을 JSON 형식으로 반환
    return JsonResponse({'recommend_html': recommend_html})


# 사용자 기반 추천 로드
def load_customers(request, model):
    # 현재 로그인한 사용자 ID 가져오기
    user_id = request.user.user_id
    # 데이터프레임 초기화
    df = pd.DataFrame()
    # 모델에 맞는 데이터프레임 불러오기
    if model == "svd_model":
        df = bring_dataframe_from_table(model)
    elif model == "nmf_model":
        df = bring_dataframe_from_table(model)
    elif model == "mf_model":
        df = bring_dataframe_from_table(model)
    # 고객 데이터를 가져오기
    customers = bring_dataframe_from_table("customers")
    # 현재 사용자가 방문한 식당 목록 추출
    restaurant_ids_visited = customers[customers['user_id'] == user_id]["restaurant_ids"].str.split(",").explode().astype(int).tolist()
    print(restaurant_ids_visited)
    # 예측 모델에서 추천된 식당 목록을 추출
    recommend_restaurant_ids = df[df["user_id"] == user_id].sort_values("predicted_rating", ascending=False)
    recommend_restaurant_ids = recommend_restaurant_ids.iloc[:100, 1].to_list()
    print("recommend_restaurant_ids", recommend_restaurant_ids)

    # 이미 방문한 식당을 제외하고 나머지 식당 ID 추출
    remaining_restaurant_ids = [restaurant_id for restaurant_id in recommend_restaurant_ids if restaurant_id not in restaurant_ids_visited]
    remaining_restaurant_ids = remaining_restaurant_ids[:20]

    # 식당 ID를 정수형으로 변환
    remaining_restaurant_ids = list(map(int, remaining_restaurant_ids))

    # 디버깅을 위해 남은 식당 ID 출력
    print(f"Remaining restaurant IDs: {remaining_restaurant_ids}")

    # 추천할 식당 ID가 비어 있는지 확인
    if not remaining_restaurant_ids:
        print("No remaining restaurant IDs to recommend.")
        return JsonResponse({'customers_html': "<p>No restaurant recommendations available</p>"})

    # Case를 사용하여 식당 순서를 보존한 채로 정렬
    preserved_order = Case(*[When(id=restaurant_id, then=pos) for pos, restaurant_id in enumerate(remaining_restaurant_ids)])
    recommend_restaurant_data = Restaurant.objects.filter(id__in=remaining_restaurant_ids).order_by(preserved_order)

    # 추천된 식당이 있는지 확인
    if not recommend_restaurant_data.exists():
        print(f"No restaurants found for IDs: {remaining_restaurant_ids}")
        return JsonResponse({'customers_html': "<p>No restaurant recommendations available</p>"})

    # 추천된 식당 출력 (디버깅용)
    for restaurant in recommend_restaurant_data:
        print(f"Recommended restaurant: {restaurant.restaurant_name}")

    # 템플릿에 추천된 식당 데이터를 전달
    context = {
        "customers": recommend_restaurant_data
    }

    # 추천된 식당 목록을 템플릿으로 렌더링
    customers_html = render_to_string("recommend/customers_list.html", context)
    return JsonResponse({'customers_html': customers_html})
