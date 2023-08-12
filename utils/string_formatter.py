class StringFormatter:
    @staticmethod
    def formatter_number(number):
        if len(number) < 3:
            number = f"{number:03d}"
        return number
