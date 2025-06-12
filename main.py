from src.getchart import get_chart
from src.model import llm_model
from src.getnews import get_news
from utils.prompts import ticker_prompt, analysis_prompt

def main(query: str):
    symbol = llm_model(ticker_prompt, query, model="gemini-2.0-flash")
    if symbol == "NONE":
        return {"error": "Symbol is NONE"}
    chart = get_chart(symbol)
    output = llm_model(analysis_prompt, chart, model="gemini-1.5-pro")
    news = get_news(symbol)
    return {
        "analysis": output,
        "news": news,
        "chart": chart
    }

# if __name__ == "__main__":
#     query = input("Ask: ")
#     output = main(query)
#     print(output)
