import finnhub
finnhub_client = finnhub.Client(api_key="cs7317pr01qkeulibng0cs7317pr01qkeulibngg")

print(finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249))