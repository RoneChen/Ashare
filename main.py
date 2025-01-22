from Ashare import get_price
from MyTT import *
import matplotlib.pyplot as plt
from tabulate import tabulate
from read_bank import get_bank_code
import time

def MA_strategys(stock_id, df, count):
    '''
    This function calculates the MA strategy for a given stock and count of stocks.
    '''
    # get the close, open, high, low price
    close = df.close.values
    open = df.open.values
    high = df.high.values
    low = df.low.values

    MA5 = MA(close, 5)
    MA10 = MA(close, 10)
    MA20 = MA(close, 20)

    df['MA5'] = MA5
    df['MA10'] = MA10
    df['MA20'] = MA20

    # preprocessing the DataFrame, which reset the index to a column.
    df.index.name = 'date'
    df= df.reset_index()
    # print('中国平安\n', df.head(20))

    item_20th = df.iloc[19]
    last_MA5 = item_20th['MA5']
    last_MA10 = item_20th['MA10']
    last_MA20 = item_20th['MA20']

    cost = item_20th['close'] * count

    flag_MA5 = 1            # 0: above, 1: below
    flag_MA10 = 1           # 0: above, 1: below
    flag_MA20 = 1           # 0: above, 1: below
    total_income_MA20 = 0   # total income of MA20 strategy
    total_income_MA10 = 0   # total income of MA10 strategy
    total_income_MA5 = 0    # total income of MA5 strategy

    # Loop through each row
    for index, row in df.tail(days-20).iterrows():
        # print(f"{row['date']} {row['open']: >10.2f} {row['close']: >10.2f} {row['MA5']: >10.4f} {row['MA10']: >10.4f} {row['MA20']: >10.4f}")
        
        #------------------------- Strategy MA5-------------------------
        if strategy_5:
            if row['close'] > last_MA5 and flag_MA5 == 1:
                # print(f"{row['close']: >10.2f} is above {row['MA20']: >10.2f}")
                # print(f"MA5 buy: {row['date']}")
                total_income_MA5 += row['close'] * count
                flag_MA5 = 0
            
            if row['close'] < last_MA5 and flag_MA5 == 0:
                # print(f"{row['close']: >10.2f} is below {row['MA20']: >10.2f}")
                # print(f"MA5 sell: {row['date']}")
                total_income_MA5 -= row['close'] * count
                flag_MA5 = 1

            last_MA5 = row['MA5']

        #------------------------- Strategy MA10-------------------------
        if strategy_10:
            if row['close'] > last_MA10 and flag_MA10 == 1:
                # print(f"{row['close']: >10.2f} is above {row['MA20']: >10.2f}")
                # print(f"MA10 buy: {row['date']}")
                total_income_MA10 += row['close'] * count
                flag_MA10 = 0
            
            if row['close'] < last_MA10 and flag_MA10 == 0:
                # print(f"{row['close']: >10.2f} is below {row['MA20']: >10.2f}")
                # print(f"MA10 sell: {row['date']}")
                total_income_MA10 -= row['close'] * count
                flag_MA10 = 1

            last_MA10 = row['MA10']

        #------------------------- Strategy MA20-------------------------
        if strategy_20:
            if row['close'] > last_MA20 and flag_MA20 == 1:
                # print(f"{row['close']: >10.2f} is above {row['MA20']: >10.2f}")
                # print(f"MA20 buy: {row['date']}")
                total_income_MA20 -= row['close'] * count
                flag_MA20 = 0
            
            if row['close'] < last_MA20 and flag_MA20 == 0:
                # print(f"{row['close']: >10.2f} is below {row['MA20']: >10.2f}")
                # print(f"MA20 sell: {row['date']}")
                total_income_MA20 += row['close'] * count
                flag_MA20 = 1
            
            last_MA20 = row['MA20']
    
    return [f"{stock_id}", f"¥{total_income_MA5:.2f}",  f"¥{total_income_MA10:.2f}", f"¥{total_income_MA20:.2f}", f"{(total_income_MA5*100 / cost):.2f}%",  f"{(total_income_MA10*100 / cost):.2f}%", f"{(total_income_MA20*100 / cost):.2f}%"], cost

def get_market(code_string):
    '''
    get the market code of the given stock code.
    '''
    market_code_dict = {
        "600": "sh",  # 沪市A股
        "601": "sh",  # 沪市A股
        "603": "sh",  # 沪市A股
        "605": "sh",  # 沪市A股
        "000": "sz",  # 深市A股
        "001": "sz",  # 深市A股
        "003": "sz",  # 深市A股
        "688": "ib",  # 科创板
        "300": "sz",  # 创业板（旧）
        "301": "sz",  # 创业板
        "002": "sz",  # 中小板
    }
    return market_code_dict.get(code_string[:3], None) + code_string


# ------------------------- Main -------------------------
days = 320                      # the number of days to get the price, the income calculation is base on (days-20)
count = 100                     # the number of stocks to buy
strategy_5 = True               # enable the MA5 strategy
strategy_10 = True              # enable the MA10 strategy
strategy_20 = True              # enable the MA20 strategy

# get the stock code
stock_ids = get_bank_code()

# Data to be displayed in the table
values = []
rois = []

for stock_id in stock_ids:
    stock_id = get_market(stock_id)
    print(stock_id)

    # get the price
    df = get_price(stock_id, frequency='1d', count=days)

    # print(df.values[-1])          # used to check the stock correctness

    value, cost = MA_strategys(stock_id, df, count)
    values.append(value)

    time.sleep(1)

# Column headers
headers_values = ["Stock", "MA5", "MA10", "MA20", "MA5", "MA10", "MA20"]

# Create the markdown table
markdown_table_values = tabulate(values, headers_values, tablefmt="github", numalign="right", stralign="center")

# Print the markdown table
print(f"(days: {days}, count: {count}, cost: ¥{cost})")
print("\nValue-ROI")
print(markdown_table_values)



# ------------------------- Plotting the Data -------------------------

# # Apply a simple moving average to smooth the data (e.g., 3-day moving average)
# df['open_smooth'] = df['open'].rolling(window=3).mean()
# df['high_smooth'] = df['high'].rolling(window=3).mean()
# df['low_smooth'] = df['low'].rolling(window=3).mean()
# df['close_smooth'] = df['close'].rolling(window=3).mean()
# df['close'] = df['close']


# # Plot the smoothed data (without markers)
# plt.figure(figsize=(10, 6))

# # Plot each line for smoothed open, high, low, close
# # plt.plot(df['date'], df['open_smooth'], label='Smoothed Open')
# # plt.plot(df['date'], df['high_smooth'], label='Smoothed High')
# # plt.plot(df['date'], df['low_smooth'], label='Smoothed Low')
# # plt.plot(df['date'], df['close_smooth'], label='Smoothed Close')
# plt.plot(df['date'], df['close'], label='Close')
# # plt.plot(df['date'], df['MA5'], label='MA5')
# # plt.plot(df['date'], df['MA10'], label='MA10')
# plt.plot(df['date'], df['MA20'], label='MA20')

# # Add title and labels
# plt.title('Smoothed Stock Prices over Time')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.legend(loc='best')

# # Rotate date labels for better readability
# plt.xticks(rotation=45)

# # Display gridlines
# plt.grid(True)

# # Show the plot
# plt.tight_layout()
# plt.show()