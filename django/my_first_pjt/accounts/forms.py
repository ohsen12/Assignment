# ❗️보통 forms.py 파일에는 기본 폼 클래스를 상속받아 만든 사용자 정의 폼을 넣어 둔다.
# 이를 통해 Django 기본 폼 기능을 확장하거나 커스터마이징할 수 있다.


from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.urls import reverse



# UserChangeForm을 상속받아 커스텀 해주겠음. 커스텀 안하면 필요없는 부분까지 회원정보 수정에 뜸.
# 저기서 메타 클래스에 있는 현재는 __all__이라고 적혀있는 부분만 오버라이딩 해주면 된다.
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )

# 뭐 링크? 누르면 바로 패스워드 수정하는 화면으로 갈 수 있도록 이니셜 메소드 오버라이딩 (이건 나도 모르겠음ㅜ)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 만약 우리가 갖고 있는 필드 중에서 password가 있으면 새로운 패스워드 텍스트 만들어서 끼워넣을게
        if self.fields.get("password"):
            password_help_text = (
                "You can change the password " '<a href="{}">here</a>.'
            ).format(f"{reverse('accounts:change_password')}")
            self.fields["password"].help_text = password_help_text