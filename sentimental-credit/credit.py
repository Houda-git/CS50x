from cs50 import get_int

def main():
    number = get_int("Number: ")
    if number == 0:
        print("INVALID")
        return
    result = calculate(number)
    length = len(str(number))
    if result % 10 != 0:
        print("INVALID")
    else:
        while number >= 100:
            number = number // 10
        if length == 15 and (number == 34 or number == 37):
            print("AMEX")
        elif (length == 13 or length == 16) and number // 10 == 4:
            print("VISA")
        elif length == 16 and (number >= 51 and number <= 55):
            print("MASTERCARD")
        else:
            print("INVALID")

def calculate(number):
    multiply = False
    sum_mult = 0
    sum = 0
    while number != 0:
        if multiply:
            double = (number % 10) * 2
            sum_mult += (double % 10) + (double // 10)
        else:
            sum += number % 10
        multiply = not multiply
        number = number // 10
    total = sum + sum_mult
    return total

main()




