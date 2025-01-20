
from django.core.cache import cache # 캐시에 key-value 들어가요 ~
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

# ⭐️ 장고는 캐싱 기능을 기본적으로 갖고 있다! redis를 쓰지 않고도 가능하다 이것! > 얘는 장고를 실행하고 있는 컴퓨터의 (로컬)메모리에 자기 나름대로 저장하고 갖고 오는 것
# 이거 안하고 레디스 사용하고 싶으면 settings.py 에 다른 거 저장해주면 됨 + 장고랑 레디스 사이를 연결해줄 미들웨어(django-redis) 설치가 필요하다.

# 상품 목록 조회를 위한 drf 함수형 뷰
# drf에서는 함수형 뷰일 때 반드시 @api_view 붙여줘야 된다고 했지!
@api_view(["GET"])
def product_list(request):
    # 일단 cache에서 value 를 꺼내올 키를 만들고 (캐시에서 get을 사용하여 key로 value 값을 들고 올 예정) 
    cache_key = "product_list"
    # product_list라는 이름의 key의 value 값으로 상품 목록이 캐시에 저장되어 있어야 함.
    
    # 캐시 키로 DB를 찌르기 전에 먼저 cache를 찔러야 한다.
    # 💡 캐시에 데이터를 안 담아놔서 캐시에 해당 key의 value 데이터가 없는 상황 > DB에서 들고와서 key-value 형태로 캐시에 저장해주고 > 다시 캐시에서 해당 키로 value 꺼내옴
    # 캐시에서 key 값으로 value를 가져올 때는 get을 사용한다(딕셔너리~) 
    # 기존 캐시에서 key로 get해서 value 데이터가 없으면 캐시에 넣어줘야 한다.
    
    # 💡 만약 캐시에서 상품목록 데이터 들고오려고 product_list라는 키로 get 했는데 데이터가 존재하지 않으면 > DB 에서 직접 긁어와서 캐시에 세팅해줌
    if not cache.get(cache_key):
        print("\ncache miss\n")
        # 직접 DB 상품 테이블 객체 다 들고와서
        products = Product.objects.all()
        # 직렬화(JSON)해주고(여러 개니까 many=True 옵션 주고)
        serializer = ProductSerializer(products, many=True)
        # 변수에 넣어주기. 물론 이렇게 안하고 바로 set에 꽂아도 됨!
        # 이후로는 DB말고 캐시에서 먼저 긁어올 수 있도록 이 밑에서 캐시에 세팅해줘야지.
        json_response = serializer.data
        # json_response가 지금 key-value 로 정의된 데이터! 얘를 바로 캐쉬에다 넣어주면 (set) 됨
        # 💡 어떠한 key와 value로 세팅할 건지, 캐시 만료시간을 몇 초로 세팅할 건지
        cache.set(cache_key, json_response, 10)
    
    # 💡 이제 캐시에는 무조건 product_list라는 이름의 key로 상품목록 value가 저장되어 있으니 캐시에 캐시키로 찔러서 갖고 와 ~
    response_data = cache.get(cache_key)
    # 이제 그걸 응답으로 넣어주기 ~ (DB 긁어와서 할 때보다 캐시에서 바로 들고 올 때 시간이 훨씬 단축되는 것을 알 수 있다.)
    return Response(response_data)
