from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# 기본 User Model을 대체할 커스텀 유저모델인 AUTH_USER_MODEL. 설정에 어카운트 앱의 모델이라고 경로 지정해주기(반드시 최초 마이그레이션과 함꼐하기)
# 보통 유저는 회원 기능이니까 accounts 앱에 모델 만든다.
class User(AbstractUser):
    '''
    지금 프로필 뷰에서 해당 프로필 유저 객체를 context에 담아 보내줬음
    following은 유저 모델에서 정의한 필드로, 사용자가 팔로우하고 있는 다른 사용자들이다.

    이렇게 한 사용자가 팔로우하고 있는 다른 사용자들을 접근할 수 있을 뿐만 아니라,
    related_name으로 "followers"를 설정함으로써, 그 사용자를 팔로우하고 있는 다른 사용자들도 접근할 수 있게 된다. (장고 ORM의 기능. 매니저를 통해 A모델이 B모델을 참조하고, B모델이 A모델을 역으로 참조하는 것도 가능하다.)
    즉, followers는 해당 사용자가 팔로우하고 있는 다른 사용자들이다.
    
    symmetrical은 대칭이라는 뜻으로 True 옵션을 주면 어느 한쪽이 팔로우하는 순간 쌍방 대칭으로 팔로우하게 만들어버리는 기능이라서, False로 해준다.
    '''
    # 팔로우는 유저 자기 자신 모델을 참조해야 함. 다대다(MTM) 필드에서 자기자신도 참조 가능!
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
