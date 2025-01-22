import os

def get_stock_code(path):
    file = open(path, 'r')
    lines = file.readlines()

    stock_codes = []

    for line in lines:
        stock_code = line.strip().split('\t')[0]
        if len(stock_code) > 6:
            stock_code = line.strip().split(' ')[0]
        stock_codes.append(stock_code)

    file.close()
    return stock_codes

stock_codes = get_stock_code('/Volumes/Rone_Chen/投资/Ashare/stocks/my_stocks.txt')
print(stock_codes)