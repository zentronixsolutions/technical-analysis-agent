ticker_prompt = f""" Extract the stock symbol from query
        If you find a company name, convert it to its stock symbol (e.g., Apple -> AAPL, Microsoft -> MSFT, etc.)
        Return only the stock symbol in uppercase without any explanation or extra text.
        If no stock symbol or company is mentioned, return NONE """

analysis_prompt = """Perform a technical analysis of this stock chart.
        Look at trend, volume, and MACD indicators.
        Give a summary not more than 100 words of what a trader might conclude. Do not give me anythign extra.
        Return Data in a professional formated manner"""