from django.core.management.base import BaseCommand, CommandError
from lotto.models import LottoRound, LottoResult, LottoTicket
from lotto.services import generate_auto_numbers, parse_numbers, judge_ticket
import random

class Command(BaseCommand):
    help = "지정 회차를 추첨하고 해당 회차의 모든 티켓을 판정합니다."

    def add_arguments(self, parser):
        parser.add_argument("--round", type=int, required=True, help="추첨할 회차 번호")

    def handle(self, *args, **options):
        rno = options["round"]
        try:
            round_obj = LottoRound.objects.get(round=rno)
        except LottoRound.DoesNotExist:
            raise CommandError(f"{rno}회 라운드가 없습니다. 먼저 회차를 생성하세요.")

        # 이미 결과가 있으면 중복 방지
        if hasattr(round_obj, "result"):
            self.stdout.write(self.style.WARNING(f"{rno}회는 이미 추첨되었습니다."))
            return

        # 난수 추첨
        wins = sorted(random.sample(range(1,46), 6))
        bonus = random.choice([n for n in range(1,46) if n not in wins])

        result = LottoResult.objects.create(
            round=round_obj,
            winning_numbers=", ".join(map(str, wins)),
            bonus_number=bonus,
        )
        self.stdout.write(self.style.SUCCESS(f"{rno}회 결과: {result.winning_numbers} + ({bonus})"))

        # 해당 회차 모든 티켓 판정
        tickets = LottoTicket.objects.filter(round=round_obj)
        for t in tickets:
            matched, bonus_hit, rank = judge_ticket(t.numbers, result.winning_numbers, result.bonus_number)
            t.match_count = matched
            t.bonus_matched = bonus_hit
            t.rank = rank
            t.save(update_fields=["match_count", "bonus_matched", "rank"])

        self.stdout.write(self.style.SUCCESS(f"판정 완료: {tickets.count()}건"))
