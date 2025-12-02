def shift_month(year: int, month: int, delta: int):
        m = month + delta
        y = year
        while m < 1:
            m += 12
            y -= 1
        while m > 12:
            m -= 12
            y += 1
        return y, m