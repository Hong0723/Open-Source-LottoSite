from django.contrib import admin
from .models import Round, Ticket


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("round_number", "draw_date", "is_drawn", "total_sales_amount")
    list_filter = ("is_drawn",)
    search_fields = ("round_number",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("user", "round", "numbers", "is_auto", "rank", "prize", "created_at")
    list_filter = ("round", "rank", "is_auto")
    search_fields = ("user__username", "numbers")
