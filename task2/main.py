from decimal import Decimal
import re


def generator_numbers(text):
    for number in re.findall(r"([\d.]+)\s", text):
        yield Decimal(number)


def sum_profit(text, func):
    result = 0
    for n in func(text):
        result += n
    return result
