## 1️⃣ 필수 과제 



#### 💡 User와 Post 앱 개발 (MTV 패턴)

<details> 
    <summary> 
        User 앱
    </summary>

1. 사용자 모델 구현
    
    기본 Django User 모델을 확장하여 커스텀 필드 추가 (예: 프로필 이미지, 소개글)
    
    - `CustomUser`
2. 회원가입, 로그인, 로그아웃 기능 구현
    1. 회원가입
        - view: `signup` or `SignUpView`
        - template: `user/signup.html`
    2. 로그인
        - view: `login` or `LoginView`
        - template: `user/login.html`
    3. 로그아웃
        - view: `logout` or `LogoutView`
3. 사용자 프로필 페이지 구현
    - view: `user_profile` or `UserProfileView`
    - template: `user/profile.html`

</details>

<details> 
    <summary>
        Post 앱 (CRUD)
    </summary>

  1. Post 모델 구현
      
      필드: 제목, 내용, 작성자, 작성일, 수정일
      
      - `Post`
  2. 게시판 기능
      1. 게시글 목록 보기 (Read - List)
          - view: `post_list` or `PostListView`
          - template: `post/post_list.html`
      2. 게시글 상세 보기 (Read - Detail)
          - view: `post_detail` or `PostDetailView`
          - template: `post/post_detail.html`
      3. 게시글 작성 기능 (Create)
          - view: `post_create` or `PostCreateView`
          - template: `post/post_form.html`
      4. 게시글 수정 기능 (Update)
          - view: `post_update` or `PostUpdateView`
          - template: `post/post_form.html` (작성 기능과 공유)
      5. 게시글 삭제 기능 (Delete)
          - view: `post_delete` or `PostDeleteView`
          - template: `post/post_confirm_delete.html`

</details>

##

#### ✅ 필수앱 구현 참고사항

**View**

- views.py는 함수 or 클래스 택 1

**기본 템플릿**

- 베이스 템플릿: `base.html`
- 네비게이션 바: `navbar.html`
- 푸터: `footer.html`

**데이터베이스**

- SQLite3

##

## 2️⃣ 도전과제

<details>
    <summary>
       DRF(Django Rest Framework)로 변환 
    </summary>

  - User와 Post 앱을 API로 변환
  - Serializer 구현
      - `UserSerializer`
      - `PostSerializer`
  - APIView 사용하여 CRUD 기능 구현
  - URL 설정 및 라우팅 

</details>

<details>
    <summary>
        좋아요 기능 
    </summary>

  - Post 모델에 좋아요 필드 추가
  - 좋아요 개수 표시

</details>

<details>
    <summary>
       댓글 기능
    </summary>
   
  - Comment 모델 구현
      - `Comment`
  - 댓글 기능
      - 댓글 작성
      - 댓글 수정
      - 댓글 삭제
  - 게시글 상세 페이지에 댓글 목록 표시

</details>

<details>
    <summary>
       데이터베이스
    </summary>
   
  - SQLite3에서 PostgreSQL or MySQL로 마이그레이션

</details>

<hr>

과제를 진행하며 학습에 필요한 주석들을 각각의 코드위에 상세히 달아놓았다.



