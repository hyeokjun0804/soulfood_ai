from django.shortcuts import render, redirect, reverse
from restaurant.models import *  # Restaurant 모델 임포트
from konlpy.tag import Okt
from fuzzywuzzy import fuzz, process

# 음식 종류 매핑 (한식, 중식 등)
cuisine_mapping = {
    '중식': '중식',
    '중국집': '중식',
    '중식집': '중식',
    '일식': '일식',
    '일식집': '일식',
    '한식' : '한식',
    '한식집': '한식',
    '양식' : '유럽음식',
    '양식집': '유럽음식',
    '이탈리아식' : '이탈리아식',
    '이탈리안' : '이탈리아식',
    '이탈리안집': '이탈리아식',
    '아시아음식' : '아시아음식',
    '프랑스음식' : '프랑스식',
    '프랑스식': '프랑스식',
    '아시안': '아시아음식',
    '아프리카음식' : '아프리카음식',
    '아프리카': '아프리카음식'
}

# Okt 토크나이저 초기화
okt = Okt()
print(okt)


def extract_nouns(text):
    """
    주어진 텍스트에서 명사를 추출하는 함수입니다.
    """
    morphs = okt.pos(text)
    nouns = [word for word, tag in morphs if tag in ['Noun', 'Alpha']]
    return nouns


def find_similar_word(target_word: str, text: str, threshold: int = 90):
    """
    주어진 단어와 텍스트 내의 단어들을 비교하여 가장 유사한 단어를 찾습니다.
    유사도가 임계값(threshold) 이상인 경우 일치하는 단어를 반환합니다.
    :param target_word: 비교할 단어
    :param text: 텍스트 (문자열)
    :param threshold: 유사도 임계값
    :return: 가장 유사한 단어 또는 None
    """
    text_words = text.split()  # 텍스트를 단어로 분리
    best_match, similarity = process.extractOne(target_word, text_words, scorer=fuzz.partial_ratio)

    # 유사도가 임계값 이상이면 일치하는 단어를 반환
    if similarity >= threshold:
        return best_match
    return None


def recommend_restaurant(search_query):
    # 검색 쿼리에서 명사 추출
    nouns = extract_nouns(search_query)

    # 전체 식당을 가져오는 대신, 시작점으로는 모든 식당을 가져옴
    matching_restaurants = Restaurant.objects.all()

    # 동적으로 지역과 카테고리 리스트를 생성합니다.
    regions = []
    cuisines = []

    # Category 모델에서 모든 카테고리명을 추출하여 cuisines에 추가
    categories = Category.objects.all()
    for category in categories:
        cuisines.append(category.name)

    # Province 모델에서 모든 지역명을 추출하여 regions에 추가
    provinces = Province.objects.all()
    for province in provinces:
        regions.append(province.name)

    # City, District, Town, Village에서 지역을 추출하여 regions에 추가
    cities = City.objects.all()
    for city in cities:
        regions.append(city.name)

    districts = District.objects.all()
    for district in districts:
        regions.append(district.name)

    towns = Town.objects.all()
    for town in towns:
        regions.append(town.name)

    villages = Village.objects.all()
    for village in villages:
        regions.append(village.name)

    # 명사들 중 지역과 카테고리를 찾습니다
    region = None
    cuisine = None

    print("Extracted Nouns: ", nouns)  # 추출된 명사 출력

    for noun in nouns:
        # 음식 종류 매핑을 통해 명사 변환
        if noun in cuisine_mapping:
            cuisine = cuisine_mapping[noun]  # 음식 종류 변환
            print(f"Matched Cuisine: {noun} -> {cuisine_mapping[noun]}")

        # 지역을 기준으로 찾기
        region_match = find_similar_word(noun, " ".join(regions))
        if region_match:
            region = noun
            print(f"Region Match: {noun} -> {region_match}")

    # 지역을 기준으로 식당 필터링
    if region:
        print(f"Filtering restaurants by region: {region}")
        matching_restaurants = matching_restaurants.filter(
            province__name__icontains=region
        ) | matching_restaurants.filter(
            city__name__icontains=region
        ) | matching_restaurants.filter(
            district__name__icontains=region
        ) | matching_restaurants.filter(
            town__name__icontains=region
        ) | matching_restaurants.filter(
            village__name__icontains=region
        )

    # 카테고리(음식 종류)를 기준으로 식당 필터링
    if cuisine:
        print(f"Filtering restaurants by cuisine: {cuisine}")
        matching_restaurants = matching_restaurants.filter(category__name__icontains=cuisine)

    # 일치하는 식당이 없다면 '추천 음식집이 없습니다' 메시지를 반환
    if not matching_restaurants.exists():
        print("No matching restaurants found. Returning '추천 음식집이 없습니다'.")
        return "추천 음식집이 없습니다."

    # 추천된 식당 중 첫 번째 식당을 반환
    return matching_restaurants.first()


def chatbot_view(request):
    if not request.user.is_authenticated:
        # 인증되지 않은 경우 로그인 페이지로 리디렉션
        return redirect(reverse('account:login'))

    """
    사용자의 질문을 처리하고 추천 식당을 반환하는 뷰입니다.
    """
    if request.method == 'POST':
        # POST 요청에서 검색 쿼리를 가져옴
        search_query = request.POST.get('chatting')  # 'chatting'은 입력 필드의 이름

        if search_query:
            # 검색 쿼리를 기반으로 추천 식당을 가져옴
            recommended_restaurants = recommend_restaurant(search_query)

            # 추천된 식당이 없으면 메시지를 설정
            if recommended_restaurants == "추천 음식집이 없습니다.":
                message = recommended_restaurants
                recommended_restaurants = []  # 식당 리스트는 빈 리스트로 설정
            else:
                message = None  # 식당이 있으면 메시지 없음

            # 검색 쿼리와 추천된 식당을 템플릿에 전달
            return render(request, 'chatbot/chatbot.html', {
                'search_query': search_query,
                'recommended_restaurants': recommended_restaurants,
                'message': message  # 템플릿에 메시지 전달
            })
        else:
            # 검색 쿼리가 없을 경우 처리
            message = "검색어를 입력해주세요."
            return render(request, 'chatbot/chatbot.html', {
                'message': message
            })

    # GET 요청일 경우, 검색어 없이 페이지를 렌더링
    return render(request, 'chatbot/chatbot.html')
