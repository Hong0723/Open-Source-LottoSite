# lotto/templatetags/lotto_extras.py
from django import template

register = template.Library()

@register.filter
def split_numbers(value):
    """
    '1,2,3,4,5,7' -> [1, 2, 3, 4, 5, 7]
    """
    if not value:
        return []
    return [int(x) for x in str(value).split(",")]

@register.filter
def lotto_color(num):
    """
    번호에 따라 공 색상 클래스 이름 반환
    """
    n = int(num)
    if 1 <= n <= 10:
        return "yellow"
    elif 11 <= n <= 20:
        return "blue"
    elif 21 <= n <= 30:
        return "red"
    elif 31 <= n <= 40:
        return "green"
    else:  # 41~45
        return "purple"

@register.filter
def rank_badge_class(rank):
    """
    등수에 따라 배지 색상 클래스 반환
    """
    if not rank or rank == 0:
        return "bg-secondary"
    rank = int(rank)
    if rank == 1:
        return "bg-danger"
    elif rank == 2:
        return "bg-warning text-dark"
    elif rank == 3:
        return "bg-primary"
    elif rank == 4:
        return "bg-success"
    elif rank == 5:
        return "bg-info"
    else:
        return "bg-secondary"

@register.filter
def rank_label(rank):
    """
    등수에 따라 라벨 텍스트 반환
    """
    if not rank or rank == 0:
        return "미당첨"
    rank = int(rank)
    return f"{rank}등"

@register.filter
def prize_display(prize):
    """
    상금을 포맷팅해서 표시
    """
    if not prize or prize == 0:
        return "-"
    prize = int(prize)
    if prize >= 100000000:
        return f"{prize // 100000000}억 {prize % 100000000 // 10000}만원"
    elif prize >= 10000:
        return f"{prize // 10000}만원"
    else:
        return f"{prize:,}원"