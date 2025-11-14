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
