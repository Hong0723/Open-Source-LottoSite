import random
from django.db import transaction
from .models import Round, Ticket

def generate_auto_numbers() :
    return ", ".join(map(str, sorted(random.sample(range(1,46)))))

def parse_numbers(s) : 
    return sorted(int(x.strip()) for x in s.split(",") if x.strip())

def judge_ticket(ticket_numbers, win_numbers, bonus) :
    nums = set(parse_numbers(ticket_numbers))
    wins = set(parse_numbers(win_numbers))
    matched = len(nums & wins)
    bonus_hit = bonus in nums
    # 한국식 등수 규칙

    if matched == 6 :
        rank = 1
    elif matched == 5 and bonus_hit :
        rank = 2
    elif matched == 5 :
        rank = 3 
    elif matched == 4 :
        rank = 4
    elif matched == 3 :
        rank = 5        
    else :
        rank = None
    return matched, bonus_hit, rank

def run_draw_for_round(round_obj: Round):
    """지정된 회차에 대해 추첨을 수행하고 티켓 당첨 결과 반영"""
    if round_obj.is_drawn:
        return round_obj  # 이미 추첨된 경우 그냥 리턴

    # 1~45 중 6개 + 보너스 1개
    numbers = random.sample(range(1, 46), 7)
    main_numbers = sorted(numbers[:6])
    bonus_number = numbers[6]

    round_obj.winning_numbers = ",".join(map(str, main_numbers))
    round_obj.bonus_number = bonus_number
    round_obj.is_drawn = True
    round_obj.save()

    # 티켓 채점
    tickets = Ticket.objects.filter(round=round_obj)
    win_set = set(main_numbers)

    with transaction.atomic():
        for t in tickets:
            nums = [int(n) for n in t.numbers.split(",")]
            nset = set(nums)
            match_cnt = len(win_set & nset)
            bonus_match = bonus_number in nset

            rank = "-"
            prize = 0

            if match_cnt == 6:
                rank = "1등"
                prize = 2_000_000_000
            elif match_cnt == 5 and bonus_match:
                rank = "2등"
                prize = 50_000_000
            elif match_cnt == 5:
                rank = "3등"
                prize = 1_500_000
            elif match_cnt == 4:
                rank = "4등"
                prize = 50_000
            elif match_cnt == 3:
                rank = "5등"
                prize = 5_000

            t.rank = rank
            t.prize = prize
            t.save()

    return round_obj