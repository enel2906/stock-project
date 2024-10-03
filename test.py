import requests
import time

def get_stock_data(stock_symbol):
    url = f'https://finfo-api.vndirect.com.vn/v4/stock_prices?q=code:{stock_symbol}&fields=code,price,date'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data'][0]  # Assuming data comes in a list
    else:
        print(f"Error: {response.status_code}")
        return None

stock_symbol = "VND"  # VNDirect stock symbol (example)
while True:
    stock_data = get_stock_data(stock_symbol)
    if stock_data:
        print(f"Stock: {stock_data['code']}, Price: {stock_data['price']}, Date: {stock_data['date']}")
    time.sleep(5)  # Poll every 5 seconds
