def calc_rank(ticket_numbers, winning_numbers, bonus):
    ticket_set = set(ticket_numbers)
    win_set = set(winning_numbers)
    match_cnt = len(ticket_set & win_set)

    if match_cnt == 6:
        return 1
    elif match_cnt == 5 and bonus in ticket_set:
        return 2
    elif match_cnt == 5:
        return 3
    elif match_cnt == 4:
        return 4
    elif match_cnt == 3:
        return 5
    else:
        return None
