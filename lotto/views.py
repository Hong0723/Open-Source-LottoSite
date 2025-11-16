import random
from datetime import date

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AutoBuyForm, ManualBuyForm
from .models import Round, Ticket
from .utils import calc_rank


# --------------------
# 공통: 현재 회차 가져오기
# --------------------
def get_current_round():
    """
    현재 판매 중인 회차를 반환.
    없으면 1회차를 오늘 날짜로 생성 (과제용 간단 로직).
    """
    current = Round.objects.order_by("-round_number").first()
    if current is None:
        current = Round.objects.create(
            round_number=1,
            draw_date=date.today(),
        )
    return current


def home(request):
    round_obj = get_current_round()
    context = {
        "round": round_obj,
    }
    return render(request, "lotto/home.html", context)


def custom_logout(request):
    """로그아웃 후 홈페이지로 리다이렉트"""
    logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect("home")


# --------------------
# 사용자용 뷰
# --------------------
@login_required
def buy_manual(request):
    round_obj = get_current_round()
    if round_obj.is_drawn:
        # 이미 추첨된 회차면 구매 불가
        return render(
            request,
            "lotto/buy_manual.html",
            {
                "form": None,
                "round": round_obj,
                "error": "이미 추첨된 회차입니다. 관리자에게 문의하세요.",
            },
        )

    if request.method == "POST":
        form = ManualBuyForm(request.POST)
        if form.is_valid():
            nums = [form.cleaned_data[f"n{i}"] for i in range(1, 7)]
            numbers_str = ",".join(str(x) for x in sorted(nums))
            Ticket.objects.create(
                user=request.user,
                round=round_obj,
                numbers=numbers_str,
                is_auto=False,
            )
            # 티켓 한 장 1000원 가정
            round_obj.total_sales_amount += 1000
            round_obj.save()
            return redirect("my_tickets")
    else:
        form = ManualBuyForm()

    return render(
        request,
        "lotto/buy_manual.html",
        {"form": form, "round": round_obj},
    )


@login_required
def buy_auto(request):
    round_obj = get_current_round()
    if round_obj.is_drawn:
        return render(
            request,
            "lotto/buy_auto.html",
            {
                "form": None,
                "round": round_obj,
                "error": "이미 추첨된 회차입니다. 관리자에게 문의하세요.",
            },
        )

    if request.method == "POST":
        form = AutoBuyForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data["count"]
            for _ in range(count):
                nums = random.sample(range(1, 46), 6)
                numbers_str = ",".join(str(x) for x in sorted(nums))
                Ticket.objects.create(
                    user=request.user,
                    round=round_obj,
                    numbers=numbers_str,
                    is_auto=True,
                )
                round_obj.total_sales_amount += 1000
            round_obj.save()
            return redirect("my_tickets")
    else:
        form = AutoBuyForm()

    return render(
        request,
        "lotto/buy_auto.html",
        {"form": form, "round": round_obj},
    )


@login_required
def my_tickets(request):
    tickets = (
        Ticket.objects.filter(user=request.user)
        .select_related("round")
        .order_by("-created_at")
    )
    return render(
        request,
        "lotto/my_tickets.html",
        {"tickets": tickets},
    )


@login_required
def round_result(request, round_number):
    # 회차 번호로 찾도록 통일
    round_obj = get_object_or_404(Round, round_number=round_number)
    tickets = Ticket.objects.filter(user=request.user, round=round_obj)
    return render(
        request,
        "lotto/round_result.html",
        {"round": round_obj, "tickets": tickets},
    )


# --------------------
# 관리자용 공통 데코레이터
# --------------------
def staff_required(view_func):
    """
    staff(관리자) + 로그인 필수
    """
    return login_required(user_passes_test(lambda u: u.is_staff)(view_func))


# --------------------
# 관리자: 대시보드 / 회차 목록
# --------------------
@staff_required
def admin_dashboard(request):
    """
    관리자 대시보드:
    - 현재 회차 정보
    - 총 판매액
    - 최근 회차 목록
    - 버튼으로 추첨 / 다음 회차 생성 / 당첨자 확인
    """
    current_round = get_current_round()
    rounds = Round.objects.order_by("-round_number")
    total_sales = sum(r.total_sales_amount for r in rounds)

    return render(
        request,
        "lotto/admin_dashboard.html",
        {
            "rounds": rounds,
            "total_sales": total_sales,
            "current_round": current_round,
        },
    )


@staff_required
def admin_rounds(request):
    rounds = Round.objects.all().order_by("-round_number")
    return render(request, "lotto/admin_rounds.html", {"rounds": rounds})


# --------------------
# 관리자: 실제 추첨 실행
# --------------------
@staff_required
def admin_draw_round(request, round_number):
    # round_number 필드를 기준으로 회차 찾기 (1회차, 2회차 ...)
    round_obj = get_object_or_404(Round, round_number=round_number)

    # 이미 추첨된 회차라면 그냥 리다이렉트
    if round_obj.is_drawn:
        messages.info(request, f"{round_obj.round_number}회차는 이미 추첨되었습니다.")
        return redirect("admin_dashboard")

    # 아직 추첨 안 됐으면 여기서 추첨 실행
    winning_nums = random.sample(range(1, 46), 7)
    main_nums = sorted(winning_nums[:6])
    bonus = winning_nums[6]

    round_obj.winning_numbers = ",".join(str(x) for x in main_nums)
    round_obj.bonus_number = bonus
    round_obj.is_drawn = True
    round_obj.save()

    # 티켓 등수 계산
    tickets = Ticket.objects.filter(round=round_obj)
    for t in tickets:
        nums = t.numbers_list()  # Ticket 모델의 헬퍼 메서드라고 가정
        rank = calc_rank(nums, main_nums, bonus)
        t.rank = rank

        # 등수별 상금
        if rank == 1:
            t.prize = 2_000_000_000
        elif rank == 2:
            t.prize = 50_000_000
        elif rank == 3:
            t.prize = 1_000_000
        elif rank == 4:
            t.prize = 50_000
        elif rank == 5:
            t.prize = 5_000
        else:
            t.prize = 0
        t.save()

    messages.success(
        request,
        f"{round_obj.round_number}회차 추첨을 완료했습니다. "
        f"(당첨번호: {round_obj.winning_numbers}, 보너스: {round_obj.bonus_number})",
    )

    return redirect("admin_dashboard")


# --------------------
# 관리자: 당첨자 / 통계 확인
# --------------------
@staff_required
def admin_winners(request, round_number):
    round_obj = get_object_or_404(Round, round_number=round_number)
    tickets = Ticket.objects.filter(round=round_obj)

    # 등수별 건수 집계
    stats = {}
    for r in range(1, 6):
        stats[r] = tickets.filter(rank=r).count()
    total_tickets = tickets.count()

    # 실제 당첨 티켓 리스트(1~5등만)
    winners = tickets.filter(rank__gte=1).select_related("user").order_by("rank")

    return render(
        request,
        "lotto/admin_winners.html",
        {
            "round": round_obj,
            "stats": stats,
            "total_tickets": total_tickets,
            "winners": winners,
        },
    )


# --------------------
# 관리자: 다음 회차 생성
# --------------------
@staff_required
def admin_create_next_round(request):
    """
    다음 회차 생성 버튼용 뷰
    - 아직 추첨 안 된 회차가 있으면 생성 막기
    """
    last_round = Round.objects.order_by("-round_number").first()

    if last_round and not last_round.is_drawn:
        messages.error(request, f"{last_round.round_number}회차가 아직 추첨되지 않았습니다.")
        return redirect("admin_dashboard")

    next_num = last_round.round_number + 1 if last_round else 1

    Round.objects.create(
        round_number=next_num,
        draw_date=date.today(),
    )

    messages.success(request, f"{next_num}회차가 생성되었습니다.")
    return redirect("admin_dashboard")
