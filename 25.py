with open('25.txt') as f:
    numbers = f.read().splitlines()

def snafu_to_decimal(n:str) -> int:
    num = 0
    fac = 1
    for c in reversed(n):
        match c:
            case '2': dig = 2
            case '1': dig = 1
            case '-': dig = -1
            case '=': dig = -2
            case '0': dig = 0

        num += dig * fac
        fac *= 5
    return num

def decimal_to_snafu(d:int) -> str:
    n = ''
    carry = False
    while d > 0:
        dig = d % 5
        pre_carry = dig
        if carry:
            if dig == 4:
                dig = 0
                carry = True
            else:
                dig += 1
                carry = False
        match dig:
            case 0: n += '0'
            case 1: n += '1'
            case 2: n += '2'
            case 3: 
                n += '='
                carry = True
            case 4: 
                n += '-'
                carry = True
        d -= pre_carry
        d //= 5
    if carry:
        n += '1'
    return n[::-1]

p1 = sum((snafu_to_decimal(n) for n in numbers))
print('part1', decimal_to_snafu(p1))