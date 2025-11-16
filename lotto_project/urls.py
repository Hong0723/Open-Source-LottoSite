from django.contrib import admin
from django.urls import path, include
from lotto import views as lotto_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/logout/", lotto_views.custom_logout, name="logout"),  # 커스텀 로그아웃 뷰
    path("accounts/", include("django.contrib.auth.urls")),  # /accounts/login/ 등
    path("", include("lotto.urls")),
]
