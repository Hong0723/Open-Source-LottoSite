from django.db import models
from django.contrib.auth.models import User


class Round(models.Model):
    round_number = models.PositiveIntegerField(primary_key=True)
    draw_date = models.DateField()
    winning_numbers = models.CharField(max_length=50, blank=True)  # "1,5,10,23,34,45"
    bonus_number = models.PositiveIntegerField(null=True, blank=True)
    is_drawn = models.BooleanField(default=False)
    total_sales_amount = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ["-round_number"]

    def __str__(self):
        return f"{self.round_number}회차"

    def winning_numbers_list(self):
        if not self.winning_numbers:
            return []
        return [int(x) for x in self.winning_numbers.split(",")]


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    numbers = models.CharField(max_length=50)  # "3,7,15,29,32,41"
    is_auto = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # 추첨 후 계산되는 필드
    rank = models.PositiveIntegerField(null=True, blank=True)  # 1,2,3.. None=미당첨
    prize = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.round.round_number}회차 {self.user.username} 티켓"

    def numbers_list(self):
        return [int(x) for x in self.numbers.split(",")]
