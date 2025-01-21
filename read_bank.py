import os

def get_bank_code():
    file = open('/Users/ronechen/Rone_Chen/Investment/bank.txt', 'r')
    lines = file.readlines()

    bank_codes = []

    for line in lines:
        bank_code = line.strip().split('\t')[0]
        bank_codes.append(bank_code)

    return bank_codes

bank = get_bank_code()
print(bank)