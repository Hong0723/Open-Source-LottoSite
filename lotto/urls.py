from django.urls import path
from . import views

urlpatterns = [
    # 메인 / 사용자 기능
    path("", views.home, name="home"),
    path("buy/manual/", views.buy_manual, name="buy_manual"),
    path("buy/auto/", views.buy_auto, name="buy_auto"),
    path("my/tickets/", views.my_tickets, name="my_tickets"),
    path(
        "round/<int:round_number>/result/",
        views.round_result,
        name="round_result",
    ),

    # 관리자 기능
    path(
        "admin-panel/dashboard/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),
    path(
        "admin-panel/rounds/",
        views.admin_rounds,
        name="admin_rounds",
    ),
    path(
        "admin-panel/round/<int:round_number>/draw/",
        views.admin_draw_round,
        name="admin_draw_round",
    ),
    path(
        "admin-panel/round/<int:round_number>/winners/",
        views.admin_winners,
        name="admin_winners",
    ),
    path(
        "admin-panel/round/create-next/",
        views.admin_create_next_round,
        name="admin_create_next_round",
    ),
]
